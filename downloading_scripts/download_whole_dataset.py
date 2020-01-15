"""With this script users can download the final HTML dataset from Internet Archive.

This is a script for downloading whole HTML dataset which is
hosted on Internet Archive. Note that the whole dataset is 7TB
compressed. If the script fails while execution, it can be
safely restarted. The internetarchive doesn't re-download files
that have been already successfully downloaded.

Example
-------
python download_whole_dataset.py

"""

import os
from internetarchive import download

with open("file_names.txt") as f:
    file_names = f.readlines()
file_names = [x.strip() for x in file_names]

print("Starting the download process, this may take a while...")

for ia_item in file_names:
    if ia_item != "enwiki-20190301-original-full-history-dump_dlab":
        ia_item = ia_item + "_html_dlab"
    flag = download(ia_item)
    if flag == False:
        print("Error occurred while downloading the data! Please rerun the script.")
        exit(1)

print("The download process finished successfully!")