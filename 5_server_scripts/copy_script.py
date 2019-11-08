"""This script is used for copying and uncompressing the data from the NFS to the local drive of the server.

The compressed data in our case is stored in a NFS, from where it needs to be copied to the local drive of
the server, and uncompress in order to be able to process it. This script encapsulates all these steps in
one single step. It as two modes of running, the first one is "count" mode which will only print the space
the files will take when they are uncompressed, and the second one is "uncompress" which actually caries
the copying and the uncompressing of the files. To uncompress the data in parallel using 40 cores, it uses
the "lbzip2" program with the argument "-n 40". It is important to mention that this script communicates
with all the servers, and copies automatically the XML files which need to be executed next. To achieve this,
the script communicates using the "running_log.txt" files which is stored on NFS and shared across multiple
servers.

Arguments
---------
mode : string, it can be either "count" or "uncompress"
   The mode to run the script in. If it is "count", the script only prints the size of the files to be copied
   and extracted, it is useful to check not to overload the local drive of the server. And if it is "uncompress",
   then the script carries out with the copying and uncompressing of the data.
start_from: string, it can be either "big" or "small"
   This argument tells the script either to start copying and uncompressing the data from the big files or small files.
no_of_files: int
    This argument tells the script how many files to copy and uncompress.

Important variables
---------
DATA_DIR : string
   The directory where the compressed XML files are stored.
LOG_FILES_DIR: string
   This is the directory where the two logs, running_log and all_files_20190301 are stored, they must be shared across all the servers!
SAVE_TO_DIR : string
   The directory where to save the uncompressed XML files, this should be on the local drive.

Example
-------
The following commands runs the script in "count" mode, starting from the next biggest XML file and including 5 files.
python copy_script.py count big 5
Output:
('74G', 'enwiki-20190301-pages-meta-history1.xml-p17675p19356')
('72G', 'enwiki-20190301-pages-meta-history1.xml-p9231p11002')
('69G', 'enwiki-20190301-pages-meta-history1.xml-p15923p17674')
('68G', 'enwiki-20190301-pages-meta-history1.xml-p19357p21035')
('67G', 'enwiki-20190301-pages-meta-history1.xml-p7425p9230')
Total GB: 350.0

Once we are sure we have enough space on the disk (350.0 GB in this case), we can run the command in "uncompress" mode.
python copy_script.py uncompress big 5

"""
import sys
import subprocess

if len(sys.argv) != 4:
    print("Please provide the arguments: mode, start_from, no_of_files")
    exit(1)

# count or uncompress
mode = sys.argv[1]
# small or big
start_from = sys.argv[2]
# no of files
no_of_files = int(sys.argv[3])

DATA_DIR = "/dlabdata1/mitrevsk/downloading_20190301/all_files/"
LOG_FILES_DIR = "/dlabdata1/mitrevsk/"
SAVE_TO_DIR = "/scratch/mediawiki/data/"

with open(os.path.join(LOG_FILES_DIR, "running_log.txt")) as f:
  running = f.readlines()
running = [line.rstrip('\n') for line in running]

with open(os.path.join(LOG_FILES_DIR, "all_files_20190301.txt")) as f:
  all_files_tmp = f.readlines()
all_files_tmp = [line.rstrip('\n') for line in all_files_tmp][1:]

all_files_from_big = []
for line in all_files_tmp:
    parts = line.split()
    all_files_from_big.append((parts[4], parts[8]))

all_files_from_small = all_files_from_big[::-1]


not_runned_from_big = [file for file in all_files_from_big if file[1] not in running]
not_runned_from_small = [file for file in all_files_from_small if file[1] not in running]

if len(not_runned_from_big) == 0:
    print("Every file is processed.")
    exit(1)
    
if start_from == "small":
    sub_list = not_runned_from_small[:no_of_files]
elif start_from == "big":
    sub_list = not_runned_from_big[:no_of_files]
else:
    print("Something wrong with the start_from argument!")
    exit(1)


if mode == "count":
    count = 0
    for f in sub_list:
        print(f)
        count += float(f[0][:-1].replace(',','.'))
    print("Total GB: " + str(count))

if mode == "uncompress":
    for f in sub_list:
        with open(os.path.join(LOG_FILES_DIR + "running_log.txt", 'a')) as file:
            file.write(f[1] + "\n")

    for f in sub_list:
        print(f)
        # First copy the file
        cmd = ["cp", DATA_DIR + f[1] + ".bz2", SAVE_TO_DIR]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
           print(line.decode())

        # Than uncompress the file
        cmd = ["lbzip2", "-dv", "-n 40", SAVE_TO_DIR + f[1] + ".bz2"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
           print(line.decode())
