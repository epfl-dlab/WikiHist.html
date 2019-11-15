# Downloading the data
The resulting dataset, along with Wikipedia's full history dump that we processed at the moment is hosted on Internet Archive inside the `enwiki_history_html` collection accessible [here](https://archive.org/details/enwiki_history_html). All the 560 Internet Archive items are part of the dataset we are providing. This directory contains scripts for downloading the dataset and metadata from the dataset locally.

* `download_data.py` - this is an interactive script for downloading the data from Internet Archive, in order to work it needs a metadata files which are also automatically fetched from IA by the script.
* `bulk_download_data.py` - this script is used to download pages in bulk, by specifying the page titles, or page ids in a file instead of typing them manually.
* `download_supplementary_data.py` - this script is used for downloading the supplementary datasets from IA.


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

Each of the JSON files is a newline-delimited JSON file which stores every element, in our case each HTML article revision with its metadata, as a new line. The format of the JSON lines is the followoing:

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
## Page creation timestamp
Because of technical reasons, all the links in the HTML pages, are rendered as red links. In order to be able to resolve which like was red or blue at the time of the creation of the revision, we provide a JSON file containing the information when a given page was created. The JSON files is a newline-delimited JSON file and the format of the JSON lines is the followoing:
```
{
    "page_id":"x",
    "title":"x",
    "timestamp":"x",
}
```
* page\_id - This is the id of the page.
* title - This is the title of the page.
* timestamp - This is the timestamp when the page was first created.

This information is extracted from the first revision of every page in the full history dump. It is important to note that this the best approximation we can get to resolve if a link was red or blue. This is because for example if some page was present in 2010, then the links in other pages that linked to it were blue links, but if this page was later deleted from Wikipedia, then the page will be missing in this JSON, because the page is also missing in the full history dump.

## Resolving redirects through time
Also, as a supplementary dataset, we provide a JSON file containing all the redirects in the full dump history, and how they changed over time. The JSON files is a newline-delimited JSON file and the format of the JSON lines is the followoing:
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
* redirect - This is the title where the redirect points to (destination of the redirect) in format (title, section).
