<?php
/*This is the script for the child process which is created by the main process.

A child process is created to convert the actual WikiText to HTML, because if for some
reason the conversion fails, the parse function from MediaWiki makes a call to exit
function which can't be caught and kills the whole script. To avoid this, whenever a
failure happens, the child process will fail and the main process will easily detect
the failure and also log it without losing the progress.
The child script needs to initialize the MediaWiki instance, wait for the data from
the main script, convert the WikiText to HTML and return the results to the main script.
The two scripts communicate through pipes.

 */

ini_set('memory_limit', '-1');
ini_set('max_execution_time', 0);
$file_to_read = $argv[1];
$directory_to_save = $argv[2];
$database_number = $argv[3];

// Initialize everything for the parser to work
require_once 'Templates_modules_database_calls.php';
require dirname(__FILE__) . '/includes/WebStart.php';

$db = "mysql1";

$GLOBALS['php_database'] = new TMD_database($db);

$fp = fopen("php://stdin", "r");

while ($line = fgets($fp, 15728640)) {
	// Decode data
	$data = json_decode($line, true);

	// Do the processing
	$timestamp = wfTimestamp(TS_UNIX, $data["timestamp"]);
	$GLOBALS['timestamp'] = $timestamp;

	$output = $wgParser->parse(
		$data["text"],
		Title::newFromText($data["title"]),
		new ParserOptions());

	// Tell the main process you are done processing the data
	$result = $output->getText();
	// Must write to stderr because MediaWiki needs the stdout
	fwrite(STDERR, "DONE\n");
	fwrite(STDERR, json_encode($result) . "\n");
}

fclose($fp);
?>
