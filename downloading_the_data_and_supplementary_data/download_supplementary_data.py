"""With this script is an example of how to download the additional meta-data provided on Internet Archive.

The additional meta-data that is provided on Internet Archive are the page id to time stamp mappings
"page_creation_timestamp.json.gz", which can be used to find when a given page was first created, helping
to resolve if a link is a red or blue link, and the "redirects_thorugh_history.json.gz" title which
can be used to resolve the redirects and study how the redirects changed through time.

Example
-------
python download_supplementary_data.py

"""

import os
from internetarchive import download
import pickle

if not os.path.isdir("metadata"):
    os.mkdir("metadata")

if not os.path.isfile("metadata/page_creation_timestamp.json.gz") or not os.path.isfile("metadata/redirects_thorugh_history.json.gz"):
    print("The metadata files are missing...")
    answer = input("Do you want to download them? (Type: Yes/No)\n")
    
    if answer.lower() == "yes":
        print("Downloading the metadata, please wait...")
        flag = download('enwiki-20190301-scripts-and-metadata_dlab', verbose=True, files=['metadata/page_creation_timestamp.json.gz', 'metadata/redirects_thorugh_history.json.gz'], no_directory=True)
        if flag == False:
            print("Error occurred while downloading the metadata! Please rerun the script.")
            exit(1)
