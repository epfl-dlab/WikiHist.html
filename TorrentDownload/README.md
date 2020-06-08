# Torrent-based download

This is the recommended way to download the full dataset. Check the [main documentation](https://github.com/epfl-dlab/WikiHist.html/blob/master/README.md) for mode details and alternative download methods.

***Important***: This script depends on Aria2. Get the binary (aria2c) for your system at: https://aria2.github.io/

Files in this folder:

* `download.sh`: main customizable download script. Please refer to Aria2 documentation to change the behavior (`aria2c -h` or [Online Manual](http://aria2.github.io/manual/en/html/README.html)). Run this script with `sh download.sh` to start the download of the full dataset.
* `files_list.txt`: list of the relative paths of the torrent files to download. One file per line, and refering to the local folder `torrent_files`.
* `torrent_files`: folder containing the _*.torrent_ files used to download the dataset.
