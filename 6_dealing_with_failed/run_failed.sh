#!/bin/bash

# This script is wrapper for the 'process_failed.php' script calling
# it for every 'failed.json' file.

files=`ls data/failed/ | grep ^en`

for f in $files
do
	if [ ! -f "data/failed/$f/processed_failed.json.gz" ]
	then
		echo $f
		php process_failed.php data/failed/$f
	fi
done
