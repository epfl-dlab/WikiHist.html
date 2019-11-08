#!/bin/bash

# This is the main run script, it is executed with the 'bash run_script.sh' command
# For more details on the run scripts, see the python 'run_script.py'

already_running_db=`ps -aux | grep "php main_parsing_process.php" | awk '{ print $12" "$15 }' | grep ^main | awk '{ print $2 }'`
already_running_files=`ps -aux | grep "php main_parsing_process.php" | awk '{ print $12" "$13 }' | grep ^main | awk '{split($0, a, "/"); print a[2]}'`
already_running_docker=`docker ps -a | grep -o mediawiki[0-9]*$`

no_db=`echo $already_running_db | wc -w`
no_files=`echo $already_running_files | wc -w`
no_docker=`echo $already_running_docker | wc -w`

if [ $no_db != $no_files ]
then
    echo "PROBLEM OCCURED"
    exit 1
fi

python run_script.py $no_db $no_docker $already_running_db $already_running_files $already_running_docker
