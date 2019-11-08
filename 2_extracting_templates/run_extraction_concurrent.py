"""This scripts runs the extraction process of the templates and modules in parallel.

The script starts by copying a XML file to the working directory, uncompressing it and
running the extraction process for that file in the background. At the start 10 such
processes are started for 10 different files, and whenever the script detects that a
given extraction process is finished, it starts the extraction process for a new file,
making sure that at least 10 extraction processes are run concurrently.

Important variables
---------
DATA_DIR : string
   The directory where the compressed XML files are stored.
SAVE_UNZIP_DIR: string
   The directory where to save the uncompressed XML files.
SAVE_RESULTS_DIR : string
   The directory where to save the resulting MySQL insertion files.
RUN_CONCURRENTLY : int
   The number of processes to be run concurrently.
LOG_FILE : string, default SAVE_RESULTS_DIR + "log.txt"
    The log file which is used to communicate between the run script and the extraction
    scripts. Don't change the default value.

Examples
-------
Before running the extraction process change and check the important variables in the code.
python run_extraction_concurrent.py

"""


import os
import subprocess
import time

# Change here
DATA_DIR = "/datasets/tmp/downloading_20190301/all_files/"
SAVE_UNZIP_DIR = "/dlabdata1/mitrevsk/extract_templates_and_modules/"
SAVE_RESULTS_DIR = "/dlabdata1/mitrevsk/extract_templates_and_modules/results/"
RUN_CONCURRENTLY = 10
LOG_FILE = os.path.join(SAVE_RESULTS_DIR, "log.txt")

with open(LOG_FILE, "w") as myfile:
    myfile.write("")
    
all_files = os.listdir(DATA_DIR)
all_files = [x for x in all_files if x.startswith("enwiki-")]

def count_running(index):
    with open(LOG_FILE, 'r') as myfile:
        content = myfile.readlines()
    return index - len(content)


already_started = 0

for file in all_files:
    while count_running(already_started) >= RUN_CONCURRENTLY:
        time.sleep(20)
    
    # Start
    print("Processing file: " + str(already_started+1))
    # Copy the file
    cmd = ["cp", os.path.join(DATA_DIR, file), SAVE_UNZIP_DIR]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        print(line.decode())

    # Unzip the file
    cmd = ["lbzip2", "-dv", "-n 40", os.path.join(SAVE_UNZIP_DIR, file)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
       print(line.decode())

    # Run the script
    file = file[:-4]
    os.system("python extract_templates_and_modules.py " + os.path.join(SAVE_UNZIP_DIR, file) + " " + SAVE_RESULTS_DIR +" &")

    already_started += 1
