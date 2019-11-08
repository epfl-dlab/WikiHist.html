"""With this script is an example of how to use the additional meta-data provided on Internet Archive.

The additional meta-data that is provided on Internet Archive are the page id to time stamp
mappings, which can be used to find when a given page was first created. And the page id to 
redirect title which can be used to resolve the redirects, if a given page is a redirect page
using this mapping we can find where this page redirects to. This script is an example of how
to use this meta-data.

Example
-------
python created_timestamp_and_redirects.py

"""

import os
from internetarchive import download
import pickle

if not os.path.isfile("metadata/page_id_to_timestamp.pickle") or not os.path.isfile("metadata/page_id_to_redirect_title.pickle") or not os.path.isfile("metadata/title_to_page_id.pickle"):
    print("The metadata files are missing...")
    answer = input("Do you want to download them? (Type: Yes/No)\n")
    
    if answer.lower() == "yes":
        print("Downloading the metadata, please wait...")
        if not os.path.exists("metadata"):
            os.mkdir("metadata")
        flag = download('enwiki-20190301-scripts-and-metadata_dlab', verbose=True, files=['metadata/page_id_to_timestamp.pickle', 'metadata/page_id_to_redirect_title.pickle', 'metadata/title_to_page_id.pickle'], no_directory=True)
        if flag == False:
            print("Error occurred while downloading the metadata! Please rerun the script.")
            exit(1)
    else:
        print("This script can't work without the metadata, please download the metadata.")
        exit(1)


print("Please wait, the metadata is loading...")

with open('metadata/page_id_to_timestamp.pickle', 'rb') as handle:
    PAGE_ID_TO_TIMESTAMP = pickle.load(handle)

with open('metadata/page_id_to_redirect_title.pickle', 'rb') as handle:
    PAGE_ID_TO_REDIRECT_TITLE = pickle.load(handle)
    
with open('metadata/title_to_page_id.pickle', 'rb') as handle:
    TITLE_TO_PAGE_ID = pickle.load(handle)
    

def get_page_created_timestamp(page_id):
    if page_id not in PAGE_ID_TO_TIMESTAMP.keys():
        print("This page_id doesn't exist! - " + str(page_id))
        return None
    return PAGE_ID_TO_TIMESTAMP[page_id]

def get_page_redirect(page_id):
    if page_id not in PAGE_ID_TO_REDIRECT_TITLE.keys():
        print("This page_id doesn't exist! - " + str(page_id))
        return None
    return PAGE_ID_TO_REDIRECT_TITLE[page_id]

def get_page_created_timestamp_by_page_title(page_title):
    if page_title not in TITLE_TO_PAGE_ID.keys():
        print("This page_title doesn't exist! - " + page_title)
        return None
    return get_page_created_timestamp(str(TITLE_TO_PAGE_ID[page_title]))

def get_page_redirect_by_page_title(page_title):
    if page_title not in TITLE_TO_PAGE_ID.keys():
        print("This page_title doesn't exist! - " + page_title)
        return None
    return get_page_redirect(str(TITLE_TO_PAGE_ID[page_title]))


mode = input("Enter the mode: created_timestamp/redirects\n")
mode = mode.lower().replace(" ", "_")

if mode != "created_timestamp" and mode != "redirects":
    print("Wrong mode entered!")
    exit(1)
    
search_by = input("Enter the search by term: page_id/page_title\n")
search_by = search_by.lower().replace(" ", "_")

if search_by != "page_id" and search_by != "page_title":
    print("Wrong search by term entered!")
    exit(1)

search_term = input("Enter the " + search_by + " to search the metadata or 'EXIT' to exit the script:\n")

while search_term != "EXIT":
    if mode == "created_timestamp" and search_by == "page_id":
        print(get_page_created_timestamp(search_term))
    
    if mode == "created_timestamp" and search_by == "page_title":
        print(get_page_created_timestamp_by_page_title(search_term))
        
    if mode == "redirects" and search_by == "page_id":
        print(get_page_redirect(search_term))
    
    if mode == "redirects" and search_by == "page_title":
        print(get_page_redirect_by_page_title(search_term))
        
    search_term = input("Enter the " + search_by + " to search the metadata or 'EXIT' to exit the script:\n")
