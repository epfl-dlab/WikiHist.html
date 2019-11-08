"""Script for downloading the XML Wikipedia dump files containing the full Wikipedia revision history.

This script is used to speed up the download of the full Wikipeida revision history using different mirrors.
The script reads the "dumpstatus.json" file to find all the files which need to be downloaded, it divides the
files into n groups, and then uses one of the n different mirrors to download one of the n groups of files.
The number n is the number of mirrors which are given in the script - the "url_mirror" variable. The group of
files to be downloaded and the mirror are given as arguments to the script when it is executed. When downloading
the dump from March 1, 2019 there were four mirrors available and total of 558 to be downloaded, the script was
used to divided the files into four groups of ~140 files and downloaded each group through different mirror.
For downloading a different dump, just change the "dumpstatus.json" file and "url_mirror" directory to add or
remove mirrors.

Arguments
---------
FILES_ : int
	The group of files to be downloaded - should be in the interval [0, n-1], n being the number of mirrors.
MIRROR : int
	The mirror from where the files will be downloaded - should be in the interval [0, n-1], n being the number of mirrors.

Examples
-------
Download the files in group 2 using the mirror 1.
python downloading_script.py 2 1

"""


import json
import sys
import wget
import math

if len(sys.argv) != 3:
	print("Enter which group of files to download and which mirror to use! files, mirror in [0, 1, 2, 3]")
	exit()

FILES_ = int(sys.argv[1])
if FILES_ not in [0, 1, 2, 3]:
	print("Wrong group of files given!")
	exit(1)

MIRROR = int(sys.argv[2])
if MIRROR not in [0, 1, 2, 3]:
	print("Wrong mirror given!")
	exit(1)

url_mirror = {}
url_mirror[0] = "https://dumps.wikimedia.org"
url_mirror[1] = "http://dumps.wikimedia.your.org"
url_mirror[2] = "http://wikimedia.bytemark.co.uk"
url_mirror[3] = "http://ftp.acc.umu.se/mirror/wikimedia.org/dumps"


dumpstatus = []
with open("dumpstatus.json", 'r') as f:
    dumpstatus = json.load(f)

FILES = dumpstatus["jobs"]["metahistorybz2dump"]["files"]
KEYS = list(dumpstatus["jobs"]["metahistorybz2dump"]["files"].keys())
files_per_mirror = math.ceil(len(FILES)/len(url_mirror))

# Divide the files into n groups, so they can be downloaded in parallel
KEYS_PER_MIRROR = {}
m = 0
count = 0
for i, key in enumerate(KEYS):
	if count == 0:
		KEYS_PER_MIRROR[m] = []
	KEYS_PER_MIRROR[m].append(key)
	count += 1
	if count == files_per_mirror:
		m += 1
		count = 0

for key in KEYS_PER_MIRROR[FILES_]:
	full_url = url_mirror[MIRROR] + FILES[key]['url']
	print(full_url)
	wget.download(full_url)
