"""With this script users can download the final HTML dataset in bulk, by providing the page ids or page titles in a text file.

This is a  script for downloading chunks of the HTML dataset in bulk which
is hosted on Internet Archive. The data can be downloaded by providing the
title or the page id of the pages an user wants to download in a text file,
every title or page id in a new line, then the path to the text file is given
to the script. The script needs meta-data files in order to work, if the
meta-data is missing, the script will ask to download it automatically from
Internet Archive. Also, the script is interactive (when run checks if the
meta-data is present, asks the user for configurations, etc.) and doesn't
need any additional setup or arguments.

Example
-------
python download_script.py

"""

import os
from internetarchive import download
import pickle

if not os.path.isfile("metadata/lookup_data.pickle") or not os.path.isfile("metadata/title_to_page_id.pickle"):
    print("The metadata files are missing...")
    answer = input("Do you want to download them? (Type: Yes/No)\n")
    
    if answer.lower() == "yes":
        print("Downloading the metadata, please wait...")
        if not os.path.exists("metadata"):
            os.mkdir("metadata")
        flag = download('enwiki-20190301-scripts-and-metadata_dlab', verbose=True, files=['metadata/lookup_data.pickle', 'metadata/title_to_page_id.pickle'], no_directory=True)
        if flag == False:
            print("Error occurred while downloading the metadata! Please rerun the script.")
            exit(1)
    else:
        print("This script can't work without the metadata, please download the metadata.")
        exit(1)


print("Please wait, the metadata is loading...")

with open('metadata/lookup_data.pickle', 'rb') as handle:
    LOOKUP_DICT, FILES, LAST_FILE = pickle.load(handle)
FILES = [x + "_html_dlab" for x in FILES]

with open('metadata/title_to_page_id.pickle', 'rb') as handle:
    TITLE_TO_PAGE_ID = pickle.load(handle)
    

def lookup_by_page_id(page_id):
    if page_id not in LOOKUP_DICT.keys():
        print("This page_id doesn't exist! - " + str(page_id))
        return None
        
    file_count, count_from, count_to = LOOKUP_DICT[page_id]
    start_file = ((count_from-1) // 1000) + 1
    end_file = ((count_to-1) // 1000) + 1
    
    if end_file-1 == LAST_FILE[file_count]//1000:
        result = []
        for i in range(start_file, end_file + 1):
            if i-1 == LAST_FILE[file_count]//1000:
                result.append(FILES[file_count] + "/" + str(LAST_FILE[file_count]) + ".json.gz")
            else:
                result.append(FILES[file_count] + "/" + str(i*1000) + ".json.gz")
        return result


    else:
        result = []
        for i in range(start_file, end_file + 1):
            result.append(FILES[file_count] + "/" + str(i*1000) + ".json.gz")

        return result
    

def lookup_by_page_title(page_title):
    if page_title not in TITLE_TO_PAGE_ID.keys():
        print("This page_title doesn't exist! - " + page_title)
        return None
    
    return lookup_by_page_id(TITLE_TO_PAGE_ID[page_title])


mode = input("Choose the search mode of the script: page_title/page_id\n")
mode = mode.lower().replace(" ", "_")

if mode != "page_title" and mode != "page_id":
    print("You entered a wrong mode!")
    exit(1)

if mode == "page_title":
    print("Note: The words in the titles are separated by single space and not the '_' character")
    
search_terms_file = input("Enter the path to the file containing the search terms:\n")

if not os.path.isfile(search_terms_file):
    print("Please enter a valid path!")
    exit(1)


search_terms = []
with open(search_terms_file) as f:
    for line in f:
        if mode == "page_title":
            search_terms.append(line)
        else:
            search_terms.append(int(line))


already_downloaded = []
if os.path.isdir("downloaded_data"):
    for d in os.listdir("downloaded_data"):
        if os.path.isdir(os.path.join("downloaded_data", d)):
            for file in os.listdir(os.path.join("downloaded_data", d)):
                already_downloaded.append(d + "/" + file)


for search_term in search_terms:
    result = None

    if mode == "page_id":
        result = lookup_by_page_id(int(search_term))

    if mode == "page_title":
        result = lookup_by_page_title(search_term)
    
    if result != None:
        result = [x for x in result if x not in already_downloaded]
        if result == []:
            continue
        print("Downloading data...")
        identifier = result[0].split("/")[0]
        files = [x.split("/")[1] for x in result]
        flag = download(identifier, verbose=True, files=files, destdir="downloaded_data")
        if flag == False:
            print("This download was unsuccessful! Try again!")
            exit(1)
            
print("The downloading is done.")
