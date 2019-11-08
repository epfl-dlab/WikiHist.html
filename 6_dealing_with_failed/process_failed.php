<?php
"""This script reads 'failed.json' file, processes the pages from it,
and saves them to gzip compressed file named 'processed_failed.json.gz'.

"""

// Initialize stuff
ini_set('memory_limit', '-1');
ini_set('max_execution_time', 0); // unlimited

// Initialize everything for the parser to work
require_once 'Templates_modules_database_calls.php';
require dirname(__FILE__) . '/includes/WebStart.php';

$GLOBALS['php_database'] = new TMD_database("mysql1");
$file_to_read = $argv[1];

$file_lines = file('compress.zlib://' . $file_to_read . '/failed.json');
$result = array();

foreach ($file_lines as $line) {
	$data = json_decode($line, true);

	// Do the processing
	$timestamp = wfTimestamp(TS_UNIX, $data["timestamp"]);
	$GLOBALS['timestamp'] = $timestamp;

	$output = $wgParser->parse(
		$data["text"],
		Title::newFromText($data["title"]),
		new ParserOptions());

	unset($data['text']);
	$data["html"] = $output->getText();

	$result[] = $data;
}

$fp = gzopen($file_to_read . '/processed_failed.json.gz', 'w2');
// Compress the file
foreach ($result as $r) {
	gzwrite($fp, json_encode($r) . "\n");
}
// Close the gz file and done
gzclose($fp);
