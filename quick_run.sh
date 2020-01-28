#/bin/bash

# Downloading the mysql database
if [ ! -d "mysql_database" ]
then
    echo "Downloading and uncompressing the mysql database..."
    wget https://zenodo.org/record/3605388/files/mysql_database.zip
    unzip mysql_database.zip
fi


# Pulling the Docker images
echo "Pulling the Docker images..."
docker pull epfldlab/mysql-server
docker pull epfldlab/mediawiki_final


# Initialize and start up the mysql database
echo "Starting the MySQL Docker container..."
docker network create my_network
cd mysql_database
docker run --name=mysql1 --network my_network -v $(pwd)/my.cnf:/etc/my.cnf -v $(pwd)/mysql_datadir_20190301:/var/lib/mysql -d epfldlab/mysql-server
cd ..


echo "Creating the directory structure and downloading the sample data..."
if [ ! -d "data" ]
then
    mkdir data
fi
cd data

if [ ! -d "results" ]
then
    mkdir results
fi
if [ ! -d "results/sample.xml" ]
then
    mkdir results/sample.xml
fi
cd ..


echo "Starting the MediaWiki container..."
docker run --name mediawiki --network my_network -v $(pwd)/data:/var/www/html/data -dit epfldlab/mediawiki_final


echo "Waiting for the containers to initialize"
sleep 10


echo "Running the main process..."
docker exec -it mediawiki php main_parsing_process.php /var/www/html/data/sample.xml /var/www/html/data/results/sample.xml/ 1


echo "Done..."
