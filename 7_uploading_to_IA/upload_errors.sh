#/bin/bash

# This script uploads the files which failed during the first uploading process.
# During the first uploading process ~0.2% of the uploading files failed and where
# uploading using this script.

prefix="/datasets/enwiki-20190301_html"
errors=`cat ERRORS_TO_IA.txt`

for error in $errors
do
    folder=`echo $error | awk -F/ '{ print $1 }'`
    file=`echo $error | awk -F/ '{ print $2 }'`
    identifier=$folder"_html_dlab"

    echo $identifier
    cd $prefix/$folder
    ia upload $identifier $file --retries 10
    if [ $? != 0 ]
    then
        echo "SOMETHING BAD HAPPENED!"
        exit 1
    fi
done
