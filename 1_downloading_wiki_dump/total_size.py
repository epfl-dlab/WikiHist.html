"""Script for computing the number of files and the total size of all files before downloading them.

This script uses the data in "dumpstatus.json" file to find the number of all XML files in the dump
we want to download and to compute their total size in GB. It is useful before downloading the data
to check if we have enough space to save the dump, in order to prevent filling the server and other
disk errors. The script doesn't take any arguments.

Examples
-------
How to execute the script.
python total_size.py

"""


import json

dumpstatus = []
with open("dumpstatus.json", 'r') as f:
    dumpstatus = json.load(f)

FILES = dumpstatus["jobs"]["metahistorybz2dump"]["files"]
KEYS = list(dumpstatus["jobs"]["metahistorybz2dump"]["files"].keys())

total_size = 0
for key in KEYS:
	total_size += FILES[key]["size"]

print("Number of files: %d" % (len(KEYS)))
print("The total size is: %.2f GB" % (total_size/1073741824))