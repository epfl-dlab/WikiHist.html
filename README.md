# Bulk-parse Wikipedia’s entire history from Wiki markup to HTML

This is a repo containing all code and steps taken to download, setup and convert the whole English Wikipedia history from Wikitext to HTML format.

The scripts are divided into directories, and every directory is a step in the process of converting the Wikitext to HTML, starting from downloading the files, extracting the templates etc…

* 1_downloading_wiki_dump
* 2_extracting_templates
* 3_create_mysql_db
* 4_docker_containers
* 5_server_scripts
* 6_dealing_with_failed
* 7_uploading_to_IA

The number in the directory name indicates the step number of the process.

## Downloading the dataset
To download the dataset locally and work with it, check the scripts inside the `downlading_the_final_data` directory.

### Dependencies
The downloading scripts have the following dependency:
* Internet Archive Command-Line Interface, [installation guide]( https://archive.org/services/docs/api/internetarchive/installation.html)

### Running the `bulk_download_script.py`
1. Download the `bulk_download_script.py` script and the `titles_to_download.txt` example file.
2. Run the script with the command `python bulk_download_script.py`.
3. If the metadata is not downloaded, you will be asked if the script should download it, type `Yes`.
4. When asked about the search mode type `page_title` to search for the pages by title.
5. Give the path to the file containing the search terms `titles_to_download.txt` when the script asks for it.
6. The data will be saved in `downloaded_data` directory.



## Quick run of the pipeline
The steps from 1 to 7 explain all the details of the process, from downloading the dump files, until uploading the data on Internet Archive, and it is useful for recreating the whole process.
Here, we show how to use the `quick_run.sh` script which automatically sets up and downloads everything that is needed to run the whole process on a sample XML file containing pages in Wikitext to obtain the pages in HTML format. Note that the script needs 101 GB of free hard drive space, because it downloads the MySQL database which is 11 GB compressed, then decompresses it to a 100 GB.

### Dependencies
The script assumes that the following libraries are installed:
* Internet Archive Command-Line Interface, [installation guide]( https://archive.org/services/docs/api/internetarchive/installation.html)
* Docker, [installation guide](https://docs.docker.com/v17.12/install/)

### Quick run
Run the script with the `quick_run.sh` following command:
```
bash quick_run.sh
```
When the processing is done:
- there will be a directory `data/results/sample.xml/_SUCCESS` indicating the successful finish of the processing 
- inside the `data/results` directory, there will be file named `log.txt` with the following content - `The job for file SUCCEEDED: sample.xml`
- there will be a directory `data/results/sample.xml` containing the resulting json files
