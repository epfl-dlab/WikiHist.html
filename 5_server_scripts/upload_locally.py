"""This is a script that copies the resulting data from the servers to a central point (in our case NFS).

When the processing of some XML file is done, this script removes the input XML file, copies the results to the central point
- the NFS in our case where the data is stored before uploading it to the Internet Archive, and removes the results from the
server to free up space for processing other XML files. Also, it logs the uploaded files to NFS. This script can be easily
modified to upload the results to a different destination or to upload them on a different service.

Important variables
---------
DATA_DIR : string
    The directory where the uncompressed XML files are stored locally on the server.
DESTINATION_DIR: string
    The directory where to upload the data to.
UPLOADED_LOG_FILE: string
    The log file where to save the names of the uploaded files.

"""

import os
import subprocess

DATA_DIR = "/scratch/mediawiki/data"
DESTINATION_DIR = "/dlabdata1/mitrevsk/RESULTS_2019/final_3/"
UPLOADED_LOG_FILE = "/dlabdata1/mitrevsk/UPLOADED.txt"


if not os.path.isdir(DESTINATION_DIR):
    print("DESTINATION DIRECTORY DOESN'T EXIT!")
    exit(1)

uploaded_files = [line.rstrip('\n') for line in open(UPLOADED_LOG_FILE)]
logged_files = [line.rstrip('\n').split("/")[1] for line in open(os.path.join(DATA_DIR, "results/log.txt"))]

to_upload = [x for x in logged_files if x not in uploaded_files and os.path.isdir(os.path.join(DATA_DIR, "results", x))]


# First remove all done file to free up memory...
print("Removing all done data files...")
for file in to_upload:
    print("    Removing the data file: " + file)
    cmd = ["rm", os.path.join(DATA_DIR, file)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        print("    " + line.decode())

    print("    Changing the ownership of the results directory: " + file)
    cmd = ["sudo", "chown", "-R", "mitrevsk:", os.path.join(DATA_DIR, "results", file)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        print(line.decode())
    # check if it was successful    
    proc.communicate()
    if proc.returncode != 0:
        print("SOMETHING WRONG WITH CHANGING THE OWNERSHIP!")
        exit(1)  


# Than divide the files, upload them, delete the results
for file in to_upload:
    print("Uploading directory: " + str(file))

    print("    Uploading the files...")
    # upload part
    # maybe move it locally than upload to IA, or smth like that
    cmd = ["cp", "-r", os.path.join(DATA_DIR, "results", file), DESTINATION_DIR]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        print(line.decode())
    # check if it was successful    
    proc.communicate()
    if proc.returncode != 0:
        print("SOMETHING WRONG WITH UPLOADING THE FILES!")
        exit(1)
    
    with open(UPLOADED_LOG_FILE, 'a') as f:
        f.write(file + "\n")


    print("    Deleting the result files...")
    cmd = ["rm", "-r", os.path.join(DATA_DIR, "results", file)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        print(line.decode())
    # check if it was successful    
    proc.communicate()
    if proc.returncode != 0:
        print("SOMETHING WRONG WITH DELETING THE FILES!")
        exit(1)
        
print("Uploading done successfully!")
