# Downloading the data

This directory contains scripts for downloading the dataset and metadata from the dataset locally.

* `download_script.py` - this is an interactive script for downloading the data from Internet Archive, in order to work it needs a metadata files which are also automatically fetched from IA by the script.
* `bulk_download_script.py` - this script is used to download pages in bulk, by specifying the page titles, or page ids in a file instead of typing them manually.
* `created_timestamp_and_redirects.py` - this script is an example of how to use the additional metadata that we provided on Internet Archive (for more info, check the script).
