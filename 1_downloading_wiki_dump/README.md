# Downloading Wikipedia's full history dump

This folder contains all the scripts needed to **fast** download the XML dump released from Wikipedia on March 01, 2019 compressed in a bz2 format.

The `dumpstatus.json` is a file containing meta data information about this dump. For example, it contains the number of files in the dump, and for every file it contains the URL from where it can be downloaded, information about the size of the file, the sha1 and md5sum which can be used to check if the downloaded files are not corrupted and other useful information. In this dump, there are a total of 558 files. The script logically divides the files into 4 groups, to be able to use 4 different mirrors to download them in parallel, increasing the bandwidth and thus the speed of the downloading process. The scripts can be reused for downloading any dump, as long as the `dumpstatus.json` file is replaced with the right `dumpstatus.json` file for the dump we want to download.

Before starting the download, the `total_size.py` script can be used to get the number of files the dump contains and the total size of the files to check and be sure that there is enough space to save the files.

`python total_size.py`

The following command will download the first group of files using the first mirror:

`python downloading_script.py 0 0`

After downloading the files, `check_files_integrity.py` script computes the md5sum of ever file and checks it with the md5sum stored in the `dumpstatus.json` file to make sure that the downloaded files are not corrupted. The script either should be in the directory where the files are stored, or the directory path can be given as an argument to the script:

`python check_files_integrity.py`
