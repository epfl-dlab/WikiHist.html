# WikiHist.html: English Wikipedia's Full Revision History Parsed to HTML

This repository contains all code related to the WikiHist.html data release.

The dataset itself is not described here. For a description of the dataset, please refer to [https://doi.org/10.5281/zenodo.3605388](https://doi.org/10.5281/zenodo.3605388).


## Quick start: Data download

As described at [https://doi.org/10.5281/zenodo.3605388](https://doi.org/10.5281/zenodo.3605388), the HTML revision history is hosted at the [Internet Archive](https://archive.org/details/enwiki_history_html).
To facilitate downloading the data, we provide handy Python scripts in the [`downloading_scripts`](tree/master/downloading_scripts) directory of this repo.

You can either download all data or only revisions for specific Wikipedia articles.


#### Install dependencies

The scripts require the [_internetarchive_](https://archive.org/services/docs/api/internetarchive/installation.html) and [_wget_](http://bitbucket.org/techtonik/python-wget/) packages. Install them:

* `pip install internetarchive`
* `pip install wget`


#### Download the full dataset of all historical HTML revisions (7TB)

To download the full dataset, run:
```
cd downloading_scripts
python download_whole_dataset.py
```
Caveat emptor: the dataset comprises 7TB, so make sure you have enough storage before starting the download. Given the size, downloading the data will take a while.


#### Download historical HTML revisions for specific Wikipedia articles only

1. `cd downloading_scripts`
2. In the file `titles_to_download.txt`, list the titles of the articles whose HTML revision history you would like to download.
3. `python download_subset.py`
4. The script requires some metadata. If you don't have it yet, you will be asked if the script should download it. Type `Yes`.
5. When asked about the search mode, type `page_title` or `page_id`. (If you choose `page_id` then `titles_to_download.txt` should contain page ids, rather than page titles.)
6. When prompted, provide the path to `titles_to_download.txt`.
7. The data will be saved in the `downloaded_data` directory.



## Data extraction pipeline

Most users will need only the above scripts for downloading the ready-made WikiHist.html dataset.
The remainder of this README refers to the code for producing dataset from scratch.

### Code structure

The scripts are divided into 7 directories:

* 1_downloading_wiki_dump
* 2_extracting_templates
* 3_create_mysql_db
* 4_docker_containers
* 5_server_scripts
* 6_dealing_with_failed
* 7_uploading_to_IA

Every directory represents a step in the process of converting wikitext to HTML, from downloading the raw wikitext dump, to extracting the templates, etc., all the way to uploading the data to the Internet Archive.
In each step's directory, there is a README with details about that step.


### Dependencies

The following libraries are required:
* Internet Archive Command-Line Tool ([installation guide](https://archive.org/services/docs/api/internetarchive/installation.html))
* Docker ([installation guide](https://docs.docker.com/v17.12/install/))


### Debugging the pipeline

To run the pipeline on a small sample (mostly for debugging), type:
```
bash quick_run.sh
```

The above script processes the small input file `data/sample.xml`. Note that, even in this setting, the script needs 111GB of free disk space, as it downloads an 11GB MySQL database that decompresses to 100GB.


If the processing completes successfully, a directory `data/results/sample.xml/_SUCCESS` will be created, and the resulting JSON files will be placed in a directory `data/results/sample.xml`.


## License
Attribution 3.0 Unported (CC BY 3.0)
