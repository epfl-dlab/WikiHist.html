# WikiHist.html: English Wikipedia's Full Revision History Parsed to HTML

This is a repo containing all code and steps taken to download, setup the process and convert the whole English Wikipedia history from Wikitext to HTML format.


## Abstract
> Wikipedia is written in the wikitext markup language. When serving content, the MediaWiki software that powers Wikipedia parses wikitext to HTML, thereby inserting additional content by expanding macros (templates and modules). Hence, researchers who intend to analyze Wikipedia as seen by its readers should work with HTML, rather than wikitext. Since Wikipedia’s revision history is publicly available exclusively in wikitext format, researchers have had to produce HTML themselves, typically by using Wikipedia’s REST API for ad-hoc wikitext-to-HTML parsing. 
> This approach, however, (1) does not scale to very large amounts of data and (2) does not correctly expand macros in historical article revisions. We solve these problems by developing a parallelized architecture for parsing massive amounts of wikitext using local instances of MediaWiki, enhanced with the capacity of correct historical macro expansion. By deploying our system, we produce and release WikiHist.html, English Wikipedia’s full revision history in HTML format. 
> We highlight the advantages of WikiHist.html over raw wikitext in an empirical analysis of Wikipedia’s hyperlinks, showing that over half of the wiki links present in HTML are missing from raw wikitext, and that the missing links are important for user navigation. Data and code are publicly available at https://doi.org/10.5281/zenodo.3605388.

## Quick start - Data download

The resulting dataset, along with Wikipedia's full history dump that we processed is hosted on Internet Archive inside the `enwiki_history_html` collection accessible [here](https://archive.org/details/enwiki_history_html). All the 559 Internet Archive items are part of the HTML dataset.

The easier way to download the dataset is to use our custom download-manager in Python. Follow these steps to start:

#### Step 1: Install dependencies

* Install the _internetarchive_ dependency with `pip install internetarchive`
* Install the _wget_ dependency with `pip install wget`

#### Step 2: Download the metadata and the script
The scripts can be found in the `downloading_scripts` directory.
The metadata is hosted on [Zenodo](https://zenodo.org/record/3605388#.Xh9bEHVKi0k), but the scripts automatically download the needed metadata.

#### Step 3.1: Run the script to download the whole dataset (~7 TB)
This script downloads the whole dataset from IA, and its dependencies `file_names.txt`.
`python download_whole_dataset.py`

#### Step 3.2: Run the script to download subset of the dataset
This script downloads a subset of the dataset from IA, and its dependencies are the metadata found on Zenodo. The script automatically downloads the metadata first, then it is an interactive script, it guides the user through the process and depending on the action of the user it asks for different inputs.
`python download_subset.py`

More detailed steps:
1. Download the `bulk_download_data.py` script and the `titles_to_download.txt` example file.
2. Run the script with the command `python bulk_download_data.py`.
3. If the metadata is not downloaded, you will be asked if the script should download it, type `Yes`.
4. When asked about the search mode type `page_title` to search for the pages by title.
5. Give the path to the file containing the search terms `titles_to_download.txt` when the script asks for it.
6. The data will be saved in `downloaded_data` directory.


### Downloading the supplementary datasets
In addition to the main dataset, we provide two more supplementary datasets:
1. `page_creation_times.json.gz` - which can be used for resolving the red links in the pages.
2. `redirect_history.json.gz` - which can be used to resolve the redirect links.
For more information about these datasets, please refer [here](https://github.com/epfl-dlab/WikiHist.html/tree/master/downloading_scripts).

The supplementary datasets can be downloaded from [Zenodo](https://zenodo.org/record/3605388#.Xh9bEHVKi0k).


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
Attribution 3.0 Unported (CC BY 3.0)
