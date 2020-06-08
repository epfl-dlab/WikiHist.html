# WikiHist.html: English Wikipedia's Full Revision History Parsed to HTML

This repository contains all code related to the WikiHist.html data release.

The dataset itself is not described here. For a description of the dataset, please refer to these resources:

* Dataset website: [https://doi.org/10.5281/zenodo.3605388](https://doi.org/10.5281/zenodo.3605388)
* Dataset paper: [https://arxiv.org/abs/2001.10256](https://arxiv.org/abs/2001.10256)


## Quick start: Data download

As described on the [dataset website](https://doi.org/10.5281/zenodo.3605388), the HTML revision history is hosted at the [Internet Archive](https://archive.org/details/WikiHist_html).
To facilitate downloading the data, we provide two alternative ways to get the data:

1. a torrent-based solution (recommended)
2. a Python scripts in the `downloading_scripts` directory of this repo.
**Note:** Using the scripts, you can download either all data or only revisions for specific Wikipedia articles.

### Option 1: Torrent-based solution

Pros: _fast, automatic retry and restore_

Cons: _intented only for full download_

This method is the recommended way to download the full dataset. If you are interested in a partial download (i.e., only some articles), please consider Option 2.
This solution requires the command-line utility Aria2 available at https://aria2.github.io/

Once the repository is cloned, the download requires 2 steps:

1. Download the utility `aria2c` from the Github repository.
2. Run the script `download.sh` in the folder `TorrentDownload`

This script starts the download of the Torrent files listed in `files_list.txt`. The parameters in the file `download.sh` can be adapted to your connection specifics. Please refer to Aria2 documentation (`aria2c -h` and [Online Manual](http://aria2.github.io/manual/en/html/README.html)).

By default, the script uses 16 parallel connections and saves the downloaded dataset in the folder WikiHist_html.


### Option 2: Custom script

Pros: _allows "lookup" partial download_

Cons: _slower, retry with max value_

This solution allows both the full dowload and the partial download of the dataset based in the article ID(s).

#### Install dependencies

The scripts require the [_internetarchive_](https://archive.org/services/docs/api/internetarchive/installation.html) and [_wget_](http://bitbucket.org/techtonik/python-wget/) packages. First you need to install those:
```
pip install internetarchive
pip install wget
```

#### Download the full dataset of all historical HTML revisions (7TB)

To download the full dataset, go to the `downloading_scripts` directory and run
```
python download_whole_dataset.py
```
_Caveat emptor:_ the dataset is 7TB large, so make sure you have enough disk space before starting the download. Given the size, downloading the data will take a while.


#### Download historical HTML revisions for specific Wikipedia articles only

If, rather than downloading the full dataset, you want to download revisions for specific Wikipedia articles only, proceed as follows:

1. Go to the `downloading_scripts` directory.
2. In the file `titles_to_download.txt`, list the titles of the articles whose HTML revision history you would like to download.
3. Run `python download_subset.py`.
4. The script requires some metadata. If you don't have it yet, you will be asked if the script should download it. Type `Yes`.
5. When asked about the search mode, type `page_title` or `page_id`. (If you choose `page_id` then `titles_to_download.txt` should contain page ids, rather than page titles.)
6. When prompted, provide the path to `titles_to_download.txt`.
7. The data will be saved in the `downloaded_data` directory.



## Data extraction pipeline

Most users will need only the above scripts for downloading the ready-made WikiHist.html dataset.
The remainder of this README refers to the code for producing the dataset from scratch.

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

To run the pipeline on a small sample (mostly for debugging), run
```
bash quick_run.sh
```

The above script processes the small input file `data/sample.xml`. Note that, even in this setting, the script needs 111GB of free disk space, as it downloads an 11GB MySQL database that decompresses to 100GB.


If the processing completes successfully, a directory `data/results/sample.xml/_SUCCESS` will be created, and the resulting JSON files will be placed in a directory `data/results/sample.xml`.


## License
Attribution 3.0 Unported (CC BY 3.0)
