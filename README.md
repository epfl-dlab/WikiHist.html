# Bulk-parse Wikipedia’s entire history from Wiki markup to HTML

This is a repo containing all code and steps taken to download, setup and convert the whole English Wikipedia history from Wikitext to HTML format.

The scripts are divided into directories, and every directory is a step in the process of converting the Wikitext to HTML, starting from downloading the files, extracting the templates etc…

* 1_downloading_wiki_dump
* 2_extracting_templates
* 3_create_mysql_db
* 4_docker_containers
* 5_server_scripts
* 6_dealing_with_failed
* 7_uploading_to_IA

The number in the directory name indicates the step number of the process.

## Downloading the dataset
To download the dataset locally and work with it, check the scripts inside the `downlading_the_final_data` directory.
