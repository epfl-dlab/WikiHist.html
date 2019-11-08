"""This script is used for merging the results from processing the failed pages and the results.

Because while processing the dump XML files, some of the pages may fail, the failed ones are saved and later
processed (this happens for ~0.01% of the pages). To preserve the order of the pages in our results as the
results from the XML dump, the failed pages are inserted in the results in the right order. This is why ~0.4% of
the result json files contain more than 1000 pages.

Important variables
---------
RESULTS_DIR : string
   The directory where the results are stored.
FAILED_DIR: string
   This is the directory where the 'process_failed.php' are stored.
SAFE : string
   The directory where the edited files will be saved before editing them, and also where the log file with the names
   of the edited files will be stored.

"""

import os
import gzip
import json

RESULTS_DIR = "/datasets/enwiki-20190301_html"
FAILED_DIR = "/dlabdata1/mitrevsk/RESULTS_2019/failed_for_IA"
SAFE  = "/dlabdata1/mitrevsk/RESULTS_2019/safe_place"

failed_dirs = [x for x in os.listdir(FAILED_DIR) if x.startswith("en")]


def read_data(file):
    DATA = []
    with gzip.open(file,'rb') as f:
        for line in f:
            DATA.append(line)
    return DATA

def write_to_file(file, articles):
    with gzip.open(file, mode='wb', compresslevel=2) as f:
        for article in articles:
            f.write(article.rstrip(b'\n') + b'\n')


for failed_dir in failed_dirs:
    # divide the failed into buckets
    failed_data = read_data(os.path.join(FAILED_DIR, failed_dir, "processed_failed.json.gz"))
    buckets = {}
    for page in failed_data:
        tmp = json.loads(page)
        count = tmp["count"]
        key = ((count // 1000) + 1) * 1000
        to_replace = b'"count":' + str.encode(str(count)) + b','
        page = page.replace(to_replace, b'')
        if key not in buckets:
            buckets[key] = []
        buckets[key].append((count, page))
    
    all_json_files = os.listdir(os.path.join(RESULTS_DIR, failed_dir))
    all_json_files = [int(x[:-8]) for x in all_json_files if x.endswith(".json.gz")]
    all_json_files = sorted(all_json_files)
    last_file = all_json_files[-1]

    for key, bucket in buckets.items():
        # check if it is biggest than the last file
        if key > last_file:
            key = last_file
        
        # find and read the right result file
        key = str(key) + ".json.gz"
        
        # check if the last file exists, if not exit
        if not os.path.isfile(os.path.join(RESULTS_DIR, failed_dir, key)):
            print("Error with file: " + os.path.join(RESULTS_DIR, failed_dir, key))
            exit(1)
        
        # before editing the original, save it somewhere safe
        if not os.path.isdir(os.path.join(SAFE, failed_dir)):
            os.mkdir(os.path.join(SAFE, failed_dir))
        os.system("cp " + os.path.join(RESULTS_DIR, failed_dir, key) + " " + os.path.join(SAFE, failed_dir))
        # and also save the file name to a log - used for uploading to IA
        with open(os.path.join(SAFE, "log.txt"), "a") as myfile:
            myfile.write(os.path.join(failed_dir, key) + "\n")
        # add the files from the bucket to the result_data
        result_data = read_data(os.path.join(RESULTS_DIR, failed_dir, key))
        last_count = -1
        offset = 0
        for count, page in bucket:
            if last_count != count:
                offset = 0
                last_count = count
            place = count % 1000
            result_data.insert(place + offset, page)
            offset += 1           
        
        #save the results
        write_to_file(os.path.join(RESULTS_DIR, failed_dir, key), result_data)
