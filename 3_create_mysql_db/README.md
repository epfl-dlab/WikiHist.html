# Creating the MySQL database

After extracting the template and module pages from the XML dump, a MySQL database needs to be created to store these templates and modules. To make the transfering and availability of this database on new servers easier, a MySQL Docker container is used. Also, because MediaWiki needs a connection to a back end database to work properly, the MySQL database also needs to have a running MediaWiki MySQL back end database. In order to have more than one MediaWiki instance on a machine and in order to avoid deadlocks when MediaWiki tries to access the MediaWiki MySQL back end database, every MediaWiki instance must have its own MediaWiki MySQL back end database. Because of this, additional 60 copies of the MediaWiki MySQL database are created and stored in the same MySQL Docker container.

The following commands are used to set up the MySQL database:

```
sudo docker network create my_network
sudo docker run --name=mysql1 --network my_network -v $(pwd)/my.cnf:/etc/my.cnf -v $(pwd)/mysql_datadir_20190301:/var/lib/mysql -d ic-registry.epfl.ch/mediawiki_docker/mysql-server
sudo docker exec -it mysql1 mysql
```

Once a MySQL shell inside the container is opened, the following commands can be used to setup the database:

```
CREATE USER 'mitrevsk'@'%' IDENTIFIED BY '123';
CREATE DATABASE mediawiki_tmd CHARACTER SET binary;
GRANT ALL ON mediawiki_tmd.* TO 'mitrevsk'@'%';
USE mediawiki_tmd;

CREATE TABLE tmtable ( id int(10) unsigned not null,
                   page_len int(10) unsigned not null,
                   redirect tinyint(3) unsigned not null,
                   model varbinary(32) not null,
                   timestamp int not null,
                   sha1 varbinary(32) not null,
                   ns int(11) not null,
                   title varbinary(255) not null, 
                   text mediumblob not null,
                   new_timestamp int not null,
                   valid_until_timestamp int ) CHARACTER SET binary;
```

Because the templates and modules insertion file is around 80 GB, the [this guide] (https://dba.stackexchange.com/questions/83125/mysql-any-way-to-import-a-huge-32-gb-sql-dump-faster) can be used to speed up the insertion process. Also max_allowed_packet should be at least 100 MB - set up `max_allowed_packet=100M` in the `my.cnf` setup file.

With the following command the data is inserted:
```
pv final_insert.sql | docker exec -i mysql1 mysql -uroot -proot --init-command="SET SQL_LOG_BIN = 0;" mediawiki_tmd
```
following
After the insertion is completed, few other things need to be done to create the final dataset:
* Creates the id field.
```
SELECT @i:=0;
UPDATE tmtable SET id = @i:=@i+1;
```


* Some of the templates and modules don't contain any text and they need to be removed.
```
CREATE TABLE deleted_null_text as (SELECT title, ns, COUNT(*)
FROM tmtable AS t
WHERE text=""
GROUP BY title, ns
HAVING COUNT(*)=(
    SELECT COUNT(*)
    FROM tmtable AS tmp
    WHERE tmp.title=t.title AND tmp.ns=t.ns
));

DELETE FROM tmtable WHERE text="";
```
11180828 - in total, 10915 - with null text, 11169913 - without null

The following steps make sure that the oldest template or module has timestamp 1 (more details in the report).
```
CREATE TABLE tmp_table2 as (SELECT ns, title, MIN(timestamp) as min_timestamp
FROM tmtable
GROUP BY ns, title);

CREATE TABLE tmp_table as (SELECT id FROM tmp_table2, tmtable WHERE tmtable.ns=tmp_table2.ns AND tmtable.title=tmp_table2.title AND tmtable.timestamp=tmp_table2.min_timestamp);

CREATE INDEX idx on tmp_table (id);
UPDATE tmtable SET new_timestamp=1 WHERE id IN (SELECT id FROM tmp_table);
```


The following two commands are for creating indexes on the templates and modules table:
```
CREATE INDEX idx_1 on tmtable (title, ns, new_timestamp);
CREATE INDEX id_ ON tmtable(id);
```

Lastly, the MediaWiki back end databases are created. The `my_wiki_bck` database file can be downloaded from [this link](https://archive.org/download/enwiki-20190301-scripts-and-metadata_dlab/mysql_database/), and its creation is explained in the 4th step.

```
for value in {1..60}
do
database="my_wiki"$value
docker exec -i mysql1 mysql -uroot -proot --execute="CREATE DATABASE $database;"
echo $database
done

for value in {1..60}
do
docker exec -i mysql1 mysql -uroot -proot my_wiki$value < my_wiki_bck
echo $value
done

for value in {1..60}
do
database="my_wiki"$value
docker exec -i mysql1 mysql -uroot -proot --execute="GRANT ALL ON $database.* TO 'mitrevsk'@'%';"
echo $database
done
```
