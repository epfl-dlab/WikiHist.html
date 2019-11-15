# Creating the docker containers

## Step 1
The `mediawiki_ext` Docker file contains the Docker instruction for creating the dockerized MediaWiki image which is needed to generate the MediaWiki MySQL database. There are numerous extensions and plug-ins for MediaWiki which are used to add features and improve MediaWiki, and Wikipedia uses these extensions. One example for these extensions is the extension Scribunto which enables for writing Lua scripts inside the Wikitext making the life easier for the editors. But when MediaWiki is first installed, it doesn't containing any of those extensions, and they need to be installed manually. Also, when MediaWiki is first installed, it needs a connection to MySQL server so it can create and setup the MediaWiki MySQL back end database.

The Docker file builds an Docker image containing these extensions. This image is then run with this command:
```
docker run --rm -p 8080:80 mediawiki_ext
```

After running this command, the MediaWiki server is accessible from http://localhost:8080/mediawiki.
Following the setup steps from the previous link, the `Local_Settings.php` file is generated and the MediaWiki MySQL back end database is generated.
The `Local_settings.php` file is automatically downloaded when the setup is finished, and the MySQL database can be obtained by running the following command:

```
docker exec -i mysql1 mysqldump -uroot -proot my_wiki > my_wiki_bck
```

## Step 2
After the first step, everything is ready for the final Docker image to be build. The `mediawiki_ready` directory contains all the necessary files for building the final image:
- `WebRequest.php` - this file is from MediaWiki, with just one line edited to enable to isolate the parser and run it from the command line
- `Parser.php` - this file is from MediaWiki, with one line edited to enable for following 3 redirects when parsing templates
- `Database.php` - this file is from MediaWiki, with `selectRow` function edited in order to intercept the calls when retrieving template and module pages
- `generate_Local_Settings.py` - this script is for generating `Local_Settings.php` file, it is used to specify which one of the 60 MediaWiki MySQL databases to be used
- `Templates_modules_database_calls.php` - here is defined the logic for retrieving the templates and modules (detailed information in the report)
- `main_parsing_process.php` and `child_parsing_process.php` - these scripts read a XML file, call the parser function on every page in the XML file and save the HTML output (detailed information in the report)

(The edited parts of original MediaWiki scripts are marked with the comment line `This is the edited part!`)

The entry point is the `main_parsing_process.php` script.

The image can be build with the following command:
```
docker build -t mediawiki_final .
```

## Testing the Docker image
After building the image, the following steps explain how it can be tested with a sample from the XML dump.

* Download a XML sample file from [here](https://ia601000.us.archive.org/0/items/enwiki-20190301-scripts-and-metadata_dlab/sample.xml) and store the file in directory called `data`, also inside the `data` directory create:
- a directory named `results` (`data/results`)
- a directory inside `results` named `sample.xml` (`data/results/sample.xml`)

* Run the MediaWiki image
```
docker run --name mediawiki --network my_network -v $(pwd)/data:/var/www/html/data -dit ic-registry.epfl.ch/mediawiki_docker/mediawiki_final
```

* Run the main process
```
docker exec -it mediawiki /bin/bash
```
(Note: Before running the command, the MySQL server created in the 3th step must be ready and running!)
```
php main_parsing_process.php /var/www/html/data/sample.xml /var/www/html/data/results/sample.xml/ 1
```

* When the processing is done:
- inside the `results/sample.xml` directory, there will be directory named `_SUCCESS`
- inside the `results` directory, there will be file named `log.txt` with the following content - `The job for file SUCCEEDED: sample.xml`
