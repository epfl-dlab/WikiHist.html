#!/bin/bash

# This script copies the failed.json failed from the data to a failed directory
# inside the working directory.

prefix="/datasets/enwiki-20190301_html/"
files=`ls $prefix`

for f in $files
do
    if [ -f "$prefix$f/failed.json" ] && [ ! -d "failed/$f" ]
    then
        echo "$f"
        mkdir failed/$f
        cp $prefix$f/failed.json failed/$f/
    fi
done
