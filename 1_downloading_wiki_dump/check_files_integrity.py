"""Script for checking the files integrity.

This script computes the md5sum of every downloaded XML file and compares it with the md5sum stored in the
"dumpstatus.json" file to check the integrity of the downloaded XML files. If it is run without argument, than 
the  script assumes the XML files are stored in the same directory where the script is stored. Otherwise, you 
can specify the directory containing the XML files as the first argument to the script.

Arguments
---------
DIRECTORY_PATH : string, optional, default: "."
	The directory path where the downloaded XML data is stored.
	
"""


import os
import json
import hashlib
import sys

DIRECTORY_PATH = "."
if len(sys.argv) == 2:
	DIRECTORY_PATH = sys.argv[1]

dumpstatus = []
with open("dumpstatus.json", 'r') as f:
    dumpstatus = json.load(f)

FILES = dumpstatus["jobs"]["metahistorybz2dump"]["files"]


count = 0
for file in os.listdir(DIRECTORY_PATH):
	if file.endswith("bz2"):
		md5_file = hashlib.md5(open(DIRECTORY_PATH + "/" + file,'rb').read()).hexdigest()
		md5_true = FILES[file]['md5']
		if md5_file != md5_true:
			print("FILE CORRUPTED: " + file)
		else:
			print("File okey")
			count += 1

print("Files that check: %s" % str(count))
