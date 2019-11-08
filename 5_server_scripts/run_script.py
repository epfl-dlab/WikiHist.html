"""This is the actual run script, the bash "run_script.sh" is calling this script with all the needed arguments generated.

This script as an arguments gets all the information from the bash script such as the already running
docker containers, XML files and databases. Based on these information, it searches for files which
have been copied, but are not processed and starts docker containers to process these files. When the
processing of a file is done, the docker containers are left behind and are not used. To clean these
obsolete docker containers, run this script in "clean" mode.

Arguments - The arguments are generated from the main bash script and passed here.
---------
arg1 : int
    The first argument is the number of already running processes (which is the same as the number of already occupied databases by some process).
arg2: int
    The second argument is the number of already running MediaWiki docker containers, this number can be different from the
    number of running files, because when a file is done processing the MediaWiki docker container is left behind and should
    be removed.
arg3: list of strings
    The third argument is the ids of the already occupied MySQL back end databases by some process.
arg4:
    The fourth argument is the names of the XML files which are being already processed in some docker container.
arg5:
    The fifth argument is the names of the already running docker containers, some of them may be left behind after the processing
    is finished and should be removed (this is done when the script is run in "clean" mode).

Important variables
---------
DATA_DIR : string
   The directory where the uncompressed XML files are stored locally on the server.

"""

import os
import sys

DATA_DIR = "/scratch/mediawiki/data"

no_running_proc = int(sys.argv[1])
no_mediawiki_docker = int(sys.argv[2])
running_proc = []
running_files = []
for i in range(3, no_running_proc+3):
    running_proc.append(sys.argv[i])
    running_files.append(sys.argv[i+no_running_proc])
running_proc = [int(x) for x in running_proc]

running_docker = []
for i in range((2*no_running_proc)+3, (2*no_running_proc)+3+no_mediawiki_docker):
    running_docker.append(sys.argv[i])
running_docker = [int(x.replace("mediawiki", "")) for x in running_docker]

if len(running_proc) != len([x for x in running_files if x.startswith("enwiki")]):
    print("SOMETHING WRONG WITH THE RUNNING FILES/PROCESSES!")
    exit(1)

print("Number of running processes: " + str(no_running_proc))
print("Number of running files: " + str(len([x for x in running_files if x.startswith("enwiki")])))
print("Number of running docker containers: " + str(len(running_docker)))
print("Running processes: " + str(running_proc))
print("Running files: " + str(running_files))
print("Running docker containers: " + str(running_docker))


logged_files = [line.rstrip('\n').split("/")[1] for line in open(os.path.join(DATA_DIR, "results/log.txt"))]
print("Files in log.txt " + str(logged_files))

data_files = [x for x in os.listdir(DATA_DIR) if x.startswith("en")]
print("Files in data directory: " + str(data_files))
print("\n")

# logged_files - the file which are processed and logged
# data_files - the files which are in the data folder (some may be done, some are being processed, and some should start with processing)
# running_proc - the ids of the running processes (database ids number)
# running_docker - names of the running docker containers, some are obsolete

# Choose mode
g = input("For cleaning docker containers type 'clean', for running files type 'run':\n")
# Clean up docker from MediaWiki containers which are obsolete
if g == "clean":
    for i in range(1, 61):
        if i not in running_proc and i in running_docker:
            print(i)
            g = input("Should I remove container number " + str(i) + ": ")
            if g == "yes":
                os.system("docker stop mediawiki" + str(i))
                os.system("docker rm mediawiki" + str(i))
            else:
                print("Not removing anything!")
                exit(1)
    print("Cleaning done!")
    exit(0)

# Find files to run them
def find_free_db():
    for i in range(1, 61):
        if i not in running_proc:
            return i

if g == "run":
    for d in data_files:
        if d not in running_files and d not in logged_files:
            free_db = find_free_db()
            print("Running container 'mediawiki%d' with file '%s'!" % (free_db, d))
            os.system("sudo mkdir " + DATA_DIR + "/results/" + d)
            os.system("docker run --name mediawiki%d --network my_network -v %s:/var/www/html/data -dit ic-registry.epfl.ch/mediawiki_docker/mediawiki_final_3" % (free_db, DATA_DIR))
            os.system("screen -d -m docker exec -it mediawiki%d php main_parsing_process.php data/%s data/results/%s/ %d" % (free_db, d, d, free_db))
            running_proc.append(free_db)
