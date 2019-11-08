#!/bin/bash

# This script is a wrapper for 'to_ia.sh' script, and calls it for every result directory.

files=`ls | grep ^en`

for f in $files
do
    if ! grep -Fxq "$f" /dlabdata1/mitrevsk/UPLOADED_TO_IA.txt
    then
        echo "Uploading file: "$f
        bash to_ia.sh $f
        if [ $? != 0 ]
        then
        # save this one, because something failed...
            echo "FATAL FAIL: "$f >> /dlabdata1/mitrevsk/ERRORS_TO_IA.txt
        fi
    fi
done
