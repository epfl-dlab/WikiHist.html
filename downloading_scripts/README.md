# Downloading the data
The resulting dataset, along with Wikipedia's full history dump that we processed at the moment is hosted on Internet Archive inside the `enwiki_history_html` collection accessible [here](https://archive.org/details/enwiki_history_html). All the 559 Internet Archive items are part of the dataset we are providing. This directory contains scripts for downloading the dataset locally.

* `download_subset.py` - this interactive script is used to download pages in bulk, by specifying the page titles, or page ids in a config file, in order to work it needs a metadata files which are also automatically fetched from Zenodo.
* `download_whole_dataset.py` - this script is used for downloading the whole dataset from IA which is around **7TB**.

#### Step 1: Install dependencies

* Install the _internetarchive_ dependency with `pip install internetarchive`
* Install the _wget_ dependency with `pip install wget`

#### Step 2: Download the metadata and the script
The scripts can be found in the [`downloading_scripts`](https://github.com/epfl-dlab/WikiHist.html/tree/master/downloading_scripts) directory. The scripts automatically download the needed metadata, which is hosted on [Zenodo](https://zenodo.org/record/3605388#.Xh9bEHVKi0k).

#### Step 3.1: Run the script to download the whole dataset (~7 TB)
This script downloads the whole dataset from IA:
```
python download_whole_dataset.py
```

#### Step 3.2: Run the script to download subset of the dataset
This script downloads a subset of the dataset from IA, and its dependency is the metadata found on Zenodo. The script automatically downloads the metadata first, it is an interactive script and it guides the user through the process and depending on the action of the user it asks for different inputs, for example:
1. Download the `download_subset.py` script and the `titles_to_download.txt` example file.
2. Run the script with the command `python download_subset.py`.
3. If the metadata is not downloaded, you will be asked if the script should download it, type `Yes`.
4. When asked about the search mode type `page_title` to search for the pages by title.
5. Give the path to the file containing the search terms `titles_to_download.txt` when the script asks for it.
6. The data will be saved in `downloaded_data` directory.


# Data format
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

# Supplementary data format
In addition to the dataset, we provide two more supplementary datasets:
## Page creation timestamp
Because of technical reasons, all the links in the HTML pages, are rendered as red links. In order to be able to resolve which like was red or blue at the time of the creation of the revision, we provide a JSON file containing the information when a given page was created. The JSON files is a newline-delimited JSON file and the format of the JSON lines is the following:
```
{
    "page_id":"x",
    "title":"x",
    "ns":"x",
    "timestamp":"x",
}
```
* page\_id - This is the id of the page.
* title - This is the title of the page.
* ns - This is the namespace of the page.
* timestamp - This is the timestamp when the page was first created.

This information is extracted from the first revision of every page in the full history dump. It is important to note that this the best approximation we can get to resolve if a link was red or blue. This is because for example if some page was present in 2010, then the links in other pages that linked to it were blue links, but if this page was later deleted from Wikipedia, then the page will be missing in this JSON, because the page is also missing in the full history dump.

## Resolving redirects through time
Also, as a supplementary dataset, we provide a JSON file containing all the redirects in the full dump history, and how they changed over time. The JSON files is a newline-delimited JSON file and the format of the JSON lines is the following:
```
{
    "title":"x"
    "timestamp":"x"
    "ns":"x"
    "page_id":"x"
    "revision_id":"x"
    "redirect":"x"
}
```
* title - This is the title of the redirect page (the source of the redirect).
* timestamp - This is the timestamp when the revision for this redirect was created.
* ns - This is the namespace of the revision.
* page\_id - This is the id of the redirect page.
* revision_id - This is the id of the revision.
* redirect - This is the title where the redirect points to (destination of the redirect) in format \["title", "section"\].
