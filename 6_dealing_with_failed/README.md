# Dealing with failed pages

Sometimes it may happen the processing for some pages to fail because of different reasons as needed dependencies, some mistakes in the WikiText in the HTML pages, miscellaneous server failures, etc. To deal with these failures, whenever during the processing of a XML file a failure is detected, all the information about the failed page is saved to a json file. Later, the pages from this json files are read, run through the processing pipeline to detect where and why the failure happened, then fix the problems, run the processing again and at the end merge the processed failed pages with the results.

### The detailed steps
On one of the servers, a MySQL and MediaWiki docker containers are created to process the failed jsons.
```
docker exec -i mysql1 mysql -uroot -proot --execute="CREATE DATABASE my_wiki_failed;"
docker exec -i mysql1 mysql -uroot -proot my_wiki_failed < my_wiki_bck
docker exec -i mysql1 mysql -uroot -proot --execute="GRANT ALL ON my_wiki_failed.* TO 'mitrevsk'@'%';"
docker run --name mediawiki_failed --network my_network -v /scratch/mitrevsk/data:/var/www/html/data -dit ic-registry.epfl.ch/mediawiki_docker/mediawiki_final_3_cpu_server
```

The scripts are copied in the docker container.
```
docker cp process_failed.php mediawiki_failed:/var/www/html
docker cp run_failed.sh mediawiki_failed:/var/www/html
```

The MediaWiki local settings is generated inside the docker container.
```
docker exec -it mediawiki_failed /bin/bash
python3 generate_Local_Settings.py mysql1 my_wiki_failed
```

The failed json files are moved to the server
```
bash get_all_failed.sh
```

Processing every `failed.json` file.
```
docker exec -it mediawiki_failed /bin/bash
bash run_failed.sh
```

After the processing is done, the processed failed data needs to be merged with the other results so that the order of the pages in the dump XML files will be the same as the order in our results. This is done by the `merge_failed_and_results.py` script which merges the data, and also logs the edited original result files.
```
python merge_failed_and_results.py
```
