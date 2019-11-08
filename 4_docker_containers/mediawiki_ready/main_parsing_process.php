<?php
/*This is the main entry script for the whole process inside a docker container.

This script initializes everything for MediaWiki to be able to process a XML file in
streaming mode. It generates a Local Settings for the MediaWiki, it creates a child
process which will actually initialize a MediaWiki instance and process pages, it
starts with reading the XML file in stream like fashion using SAX parser, and whenever
it gets a result from the child process, it saves the data in JSON format.
A child process is created to convert the actual WikiText to HTML, because if for some
reason the conversion fails, the parse function from MediaWiki makes a call to exit
function which can't be caught and kills the whole script. To avoid this, whenever a
failure happens, the child process will fail and the main process will easily detect
the failure and also log it without losing the progress.

 */

// Initialize stuff
ini_set('memory_limit', '-1');
ini_set('max_execution_time', 0);

$file_to_read = $argv[1];
$directory_to_save = $argv[2];
$database_number = $argv[3];

$time_start = time(true);

// Creating child process
$descriptors = array(
	0 => array("pipe", "r"),
	1 => array("pipe", "w"),
	2 => array("pipe", "w"),
);
$cmd = 'php child_parsing_process.php ' . $file_to_read . " " . $directory_to_save . " " . $database_number;

$db = "mysql1";

$command = escapeshellcmd('python3 generate_Local_Settings.py ' . $db . ' my_wiki' . $database_number);
$output = shell_exec($command);
echo $output;
$process = 0;
while (!is_resource($process)) {
	$process = proc_open($cmd, $descriptors, $pipes);
}
// Give a time for everything to initialize in the child process
sleep(15);

// Reading XML using the SAX(Simple API for XML) parser
$inside_contributor = false;
$inside_revision = false;

$title = null;
$ns = null;
$article = false;
$page_id = 0;
$last_page_id = -1;
$redirect_title = null;
$revision = null;

$tag = null;
$inside_data = false;

$count = 0;
$result = array();

// Call to this function when tags are opened
function start_tag($parser, $name, $attrs) {
	global $revision, $tag, $inside_data, $inside_contributor, $redirect_title, $inside_revision, $ns, $article;

	if (!empty($name)) {
		if ($name == 'revision') {
			$inside_revision = true;
			$revision = array();
			$revision["parentid"] = -1;
		} else if ($name == 'contributor') {
			$inside_contributor = true;
		} else if ($name == 'page') {
			$ns = null;
			$article = false;
		} else if ($name == 'redirect') {
			if (array_key_exists("title", $attrs)) {
				$redirect_title = $attrs["title"];
			}
		}
		$tag = $name;
		$inside_data = false;
	}
}

// Call to this function when tags are closed
function end_tag($parser, $name) {
	global $revision, $tag, $inside_data, $inside_contributor, $inside_revision, $title, $ns, $process, $pipes, $descriptors, $cmd, $count, $time_start, $directory_to_save, $result, $page_id, $redirect_title, $last_page_id, $article;

	if (!empty($name)) {
		$tag = null;
		$inside_data = false;
		// If the close tag is for a revision, than we have all the information for parsing the revision
		if ($name == "revision" && $article) {
			// Prepare data_ for sending to child process
			$data_ = array();
			$data_["title"] = $title;
			$data_["timestamp"] = $revision["timestamp"];
			$data_["text"] = $revision["text"];
			$json_encoded_data = json_encode($data_);
			fwrite($pipes[0], $json_encoded_data);
			fwrite($pipes[0], "\n");
			fflush($pipes[0]);

			$revision["title"] = $title;
			$revision["ns"] = $ns;
			$revision["page_id"] = $page_id;
			if ($redirect_title != null) {
				$revision["redirect_title"] = $redirect_title;
			}

			if (proc_get_status($process)['running'] == 1) {
				$line = fgets($pipes[2]);
				if ($line == "DONE\n") {
					$count += 1;
					$line = fgets($pipes[2]);

					if ($last_page_id != $page_id) {
						$last_page_id = $page_id;
						file_put_contents($directory_to_save . 'page_id_count.txt', $page_id . " " . $count . "\n", FILE_APPEND);
					}

					unset($revision['text']);
					$revision["html"] = json_decode($line);
					$result[] = $revision;

					if ($count % 1000 == 0) {
						$fp = gzopen($directory_to_save . $count . '.json.gz', 'w2');
						// Compress the file
						foreach ($result as $r) {
							gzwrite($fp, json_encode($r) . "\n");
						}
						// Close the gz file
						gzclose($fp);
						$result = array();

						$time_end = time(true);
						$time = $time_end - $time_start;
						echo "Did this in $time seconds\n";

						fclose($pipes[0]);
						fclose($pipes[1]);
						proc_close($process);
						while (!is_resource($process)) {
							file_put_contents("/var/www/html/log.txt", "RESTART " . $count . "\n", FILE_APPEND);
							$process = proc_open($cmd, $descriptors, $pipes);
						}
					}
				} else {
					$revision["count"] = $count;
					file_put_contents($directory_to_save . 'failed.json', json_encode($revision) . "\n", FILE_APPEND);
					// The process died, clean up, initialize a new one and exit!
					file_put_contents("/var/www/html/log_child_failed.txt", $line . "\n", FILE_APPEND);
					fclose($pipes[0]);
					fclose($pipes[1]);
					proc_close($process);
					while (!is_resource($process)) {
						file_put_contents("/var/www/html/log.txt", "STUCK in while1, child output is not DONE.\n", FILE_APPEND);
						$process = proc_open($cmd, $descriptors, $pipes);
					}
				}
			} else {
				$revision["count"] = $count;
				file_put_contents($directory_to_save . 'failed.json', json_encode($revision) . "\n", FILE_APPEND);
				// The process died, clean up, initialize a new one and exit!
				fclose($pipes[0]);
				fclose($pipes[1]);
				proc_close($process);
				while (!is_resource($process)) {
					file_put_contents("/var/www/html/log.txt", "STUCK in while2, child failed before processing this revision.\n", FILE_APPEND);
					$process = proc_open($cmd, $descriptors, $pipes);
				}
			}
		}
		if ($name == 'revision') {
			$inside_revision = false;
		} else if ($name == 'contributor') {
			$inside_contributor = false;
		}
	}
}

// Call on the text between the start and end of the tags
function content($parser, $data) {
	global $revision, $tag, $inside_data, $title, $inside_contributor, $inside_revision, $ns, $page_id, $article;

	if (!empty($data)) {
		// What to save for a given revision
		if ($ns == null || $ns == 0) {
			if ($inside_revision && $tag != 'revision' && $tag != '') {
				if (!$inside_contributor) {
					if ($inside_data) {
						$revision[$tag] .= $data;
					} else {
						$revision[$tag] = $data;
					}
				} else {
					if ($tag == 'username') {
						if ($inside_data) {
							$revision['cont_username'] .= $data;
						} else {
							$revision['cont_username'] = $data;
						}
					} else if ($tag == 'ip') {
						if ($inside_data) {
							$revision['cont_ip'] .= $data;
						} else {
							$revision['cont_ip'] = $data;
						}
					} else if ($tag == 'id') {
						if ($inside_data) {
							$revision['cont_id'] .= $data;
						} else {
							$revision['cont_id'] = $data;
						}
					}
				}
			} else if ($tag == 'title') {
				if ($inside_data) {
					$title .= $data;
				} else {
					$title = $data;
				}
			} else if ($tag == 'id' && !$inside_contributor && !$inside_revision) {
				if ($inside_data) {
					$page_id .= $data;
				} else {
					$page_id = $data;
				}
			}
		}

		$inside_data = true;
	} else {
		if ($tag == 'ns') {
			$article = true;
			$ns = 0;
		}
	}
}

// Creates a new XML parser and returns a resource handle referencing it to be used by the other XML functions
$parser = xml_parser_create();

xml_set_element_handler($parser, "start_tag", "end_tag");
xml_set_character_data_handler($parser, "content");
// Tag names as it is in the XML file(filename)
xml_parser_set_option($parser, XML_OPTION_CASE_FOLDING, false);

// Open xml file
if (!($handle = fopen($file_to_read, "rb"))) {
	die("Could not open XML input!");
}

while ($data = fread($handle, 4096)) {
	xml_parse($parser, $data);
}

mkdir($directory_to_save . "_SUCESS");
file_put_contents("/var/www/html/data/results/log.txt", "The job for file SUCCEEDED: " . $file_to_read . "\n", FILE_APPEND);
xml_parser_free($parser);
fclose($handle);

if ($count % 1000 != 0) {
	$fp = gzopen($directory_to_save . $count . '.json.gz', 'w2');
	// Compress the file
	foreach ($result as $r) {
		gzwrite($fp, json_encode($r) . "\n");
	}
	// Close the gz file
	gzclose($fp);
}

file_put_contents($directory_to_save . 'page_id_count.txt', $page_id . " " . $count . "\n", FILE_APPEND);

$time_end = time(true);
$time = $time_end - $time_start;

// Cleaning up the resources
fclose($pipes[0]);
fclose($pipes[1]);
$return_value = proc_close($process);

echo "Did everything in $time seconds\n";
?>
