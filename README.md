# WikiHist.html: English Wikipedia's Full Revision History Parsed to HTML

This is a repo containing all code and steps taken to download, setup the process and convert the whole English Wikipedia history from Wikitext to HTML format.


## Abstract
Abstract goes here.


## Github repository structure
The scripts are divided into directories, and every directory is a step in the process of converting the Wikitext to HTML, starting from downloading the files, extracting the templates etc… In every step directory, there is a readme file which gives the details about that step.

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

### Data format
The final dataset contains more than 580 million of revision pages from more than 5 800 000 articles. Since the full history dump from Wikipedia is divided in 558 XML files and the processing is done for every file, the results are saved into 558 Internet Archive items which can be viewed as directories, every IA item (directory) named as the input XML file. In these IA items (directories), the HTML pages are stored in JSON files, and every JSON file contains 1000 pages. The IA item (directory) tree structure looks like this:

    .
    ├── enwiki-20190301-pages-meta-history1.xml-p10p2062/
    │   ├── 1000.json.gz
    │   ├── 2000.json.gz
    │   ├── 3000.json.gz
    │   ├── ...
    │   └── 1100000.json.gz
    ├── ...
    ├── ...
    ├── enwiki-20190301-pages-meta-history27.xml-pxxxpxxx/
    │   ├── 1000.json.gz
    │   ├── 2000.json.gz
    │   ├── 3000.json.gz
    │   ├── ...
    │   └── 1100000.json.gz
    └── ...

Each of the JSON files is a newline-delimited JSON file which stores every element, in our case each HTML article revision with its metadata, as a new line. The format of the JSON lines is the following:

```
{
    "parentid":"x",
    "id":"x",
    "timestamp":"x",
    "cont_username":"x",
    "cont_ip":"x",
    "cont_id":"x",
    "comment":"x",
    "model":"x",
    "format":"x",
    "sha1":"x",
    "title":"x",
    "ns":0,
    "page_id":"x",
    "redirect_title":"x",
    "html":"x"
}
```
* parentid - This is the id of the parent revision of this revision.
* id - This is the id of this revisions.
* timestamp - This is the timestamp when the revision was created.
* cont\_username - this is the username of the contributor who created this revisions.
* cont\_ip - This is the ip address of the contributor who created this revision.
* comment - This is the comment left by the user  who created this revision.
* model - The model of this revision.
* format - The format of this revision.
* sha1 - The sha1 of this revision.
* title - This is the title of this revision.
* ns - This is the namespace of this revision and is always 0, because only the main pages/articles are processed.
* page\_id - This is the id of the page of this revision.
* redirect\_title - If the page of this revision is redirect, this is the title where it redirects to.
* html - The revision in HTML format.

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

### Downloading the supplementary datasets
In addition to the main dataset, we provide two more supplementary datasets:
1. `page_creation_timestamp.json.gz` - which can be used for resolving the red links in the pages.
2. `redirects_thorugh_history.json.gz` - which can be used to resolve the redirect links.
For more information about these datasets, please refer [here](https://github.com/epfl-dlab/enwiki_history_to_html/tree/master/downloading_the_data_and_supplementary_data#supplementary-data-format).

To download the supplementary dataset just run the following script from the `downloading_the_data_and_supplementary_data` directory:

`python download_supplementary_data.py`

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
