# Bulk-parse Wikipedia’s entire history from Wiki markup to HTML

This is a repo containing all code and steps taken to download, setup the process and convert the whole English Wikipedia history from Wikitext to HTML format.


## Abstract
Abstract goes here.


## Github repository structure
The scripts are divided into directories, and every directory is a step in the process of converting the Wikitext to HTML, starting from downloading the files, extracting the templates etc… In every step directory, there is a read me file which gives the details about that step.

* 1_downloading_wiki_dump
* 2_extracting_templates
* 3_create_mysql_db
* 4_docker_containers
* 5_server_scripts
* 6_dealing_with_failed
* 7_uploading_to_IA

The number in the directory name indicates the step number of the project.


## Downloading the dataset
The resulting dataset, along with Wikipedia's full history dump that we processed at the moment is hosted on Internet Archive inside the `enwiki_history_html` collection accessible [here](https://archive.org/details/enwiki_history_html). All the 560 Internet Archive items are part of the dataset we are providing. To easily download the data from Internet Archive we provided python scripts. For more information about the scripts, check the read.me file and scripts in the `downloading_the_data_and_supplementary_data` directory. Here we describe how the `bulk_download_data.py` can be used to download the revision history of multiple pages in HTML format from the dataset based on their title.

### Dependencies
The downloading scripts have the following dependency:
* Internet Archive Command-Line Interface, [installation guide]( https://archive.org/services/docs/api/internetarchive/installation.html)

### Running the `bulk_download_data.py`
1. Download the `bulk_download_data.py` script and the `titles_to_download.txt` example file.
2. Run the script with the command `python bulk_download_data.py`.
3. If the metadata is not downloaded, you will be asked if the script should download it, type `Yes`.
4. When asked about the search mode type `page_title` to search for the pages by title.
5. Give the path to the file containing the search terms `titles_to_download.txt` when the script asks for it.
6. The data will be saved in `downloaded_data` directory.


## Example use case: extracting links
Here goes a short explanation on how to run the GO script for extracting the links, find the redlinks, and resolve redirects thoguh time.


## Quick run of the pipeline
The steps from 1 to 7 explain all the details of the process, from downloading the dump files, to uploading the data on Internet Archive, and it is useful for recreating the whole process.
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
- inside the `data/results` directory, there will be a file named `log.txt` with the following content - `The job for file SUCCEEDED: sample.xml`
- there will be a directory `data/results/sample.xml` containing the resulting json files


## License
License goes here.
