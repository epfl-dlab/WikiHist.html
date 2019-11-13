# Downloading the data

This directory contains scripts for downloading the dataset and metadata from the dataset locally.

* `download_script.py` - this is an interactive script for downloading the data from Internet Archive, in order to work it needs a metadata files which are also automatically fetched from IA by the script.
* `bulk_download_script.py` - this script is used to download pages in bulk, by specifying the page titles, or page ids in a file instead of typing them manually.
* `created_timestamp_and_redirects.py` - this script is an example of how to use the additional metadata that we provided on Internet Archive: `page_id_to_redirect_title.pickle` a directory that can be used to resolve the redirects and `page_id_to_timestamp.pickle` a directory that contains the timestamp when a page was created, it can be used to resolve the red links.

### Dependencies
* Internet Archive Command-Line Interface, [installation guide]( https://archive.org/services/docs/api/internetarchive/installation.html)

### Running the `bulk_download_script.py`
* Download the `bulk_download_script.py` script and the `titles_to_download.txt` example file.
* Run the script with the command `python bulk_download_script.py`.
* If the metadata is not downloaded, you will be asked if the script should download it, type `Yes`.
* When asked about the search mode type `page_title` to search for the pages by title.
* Give the path to the file containing the search terms `titles_to_download.txt` when the script asks for it.
* The data will be saved in `downloaded_data` directory.
