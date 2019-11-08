#!/bin/bash

# This script uploads one folder of results to IA as IA item.
# This script first generates the metadata csv file, then creates the item on IA,
# then uploads every file in the result folder. If a failure happens, it saves the
# name of the file in a log, so later it can be uploaded.

cd $1

python ../generate_metadata_csv.py

# all the needed variables...
files=`ls`
identifier=`cat metadata.csv | grep ^en | awk -F',' '{ print $1 }'`
directory=`basename $1`

ia upload --spreadsheet=metadata.csv

sleep 10

for f in $files
do
    if [ $f != "_SUCESS" ] && [ $f != "metadata.csv" ] && [ $f != "page_id_count.txt" ] && [ $f != "failed.json" ]
    then
        echo $f
        ia upload $identifier $f --retries 10
        
        if [ $? != 0 ]
        then
        # save this one, because something failed...
            echo $directory/$f >> /dlabdata1/mitrevsk/ERRORS_TO_IA.txt
        fi
    fi
done

echo $directory >> /dlabdata1/mitrevsk/UPLOADED_TO_IA.txt

rm metadata.csv
