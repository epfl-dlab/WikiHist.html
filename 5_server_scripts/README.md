# Running the process on server

All the previous directories contain the instructions and codes to generate the datasets and Docker images in order the whole system to be distributed and run concurrently on multiple servers. This folder contains the scripts for preparing one server, moving the compressed Wikipedia dump from where they are stored (the NFS in our case) to the local drive of the server, running the processing, copying the results back somewhere safe (to the NFS in our case) before uploading them to the Internet Archive and cleaning the server after the computation for a given file is done.

First, using the following commands we can setup a given server, these commands copy the needed scripts and the data for MySQL dataset:
```
cp /dlabdata1/mitrevsk/scripts/copy_script.py .
cp /dlabdata1/mitrevsk/scripts/run_script.sh . 
cp /dlabdata1/mitrevsk/scripts/run_script.py .
cp /dlabdata1/mitrevsk/scripts/upload_locally.py .
cp /dlabdata1/mitrevsk/binary_db_bck/* .
```

These commands create and start the docker container which will contain the MySQL database.
```
sudo docker network create my_network
docker run --name=mysql1 --network my_network -v $(pwd)/my.cnf:/etc/my.cnf -v $(pwd)/mysql_datadir_20190301:/var/lib/mysql -d ic-registry.epfl.ch/mediawiki_docker/mysql-server
```

After the server is setup, with the `copy_script.py` we need to copy and uncompress data from the Wikipedia dump in order to process it.
The copy script can copy multiple files from the dump starting either from the biggest file or from the smallest which are next in the queue for processing, and also using the `copy_script.py` in `count` mode we can check how much space a given number of files from the dump will occupy. For example, to check how much space 5 files will occupy starting from the big files we should run the copy script with the following arguments:

```
python copy_script.py count big 5
('74G', 'enwiki-20190301-pages-meta-history1.xml-p17675p19356')
('72G', 'enwiki-20190301-pages-meta-history1.xml-p9231p11002')
('69G', 'enwiki-20190301-pages-meta-history1.xml-p15923p17674')
('68G', 'enwiki-20190301-pages-meta-history1.xml-p19357p21035')
('67G', 'enwiki-20190301-pages-meta-history1.xml-p7425p9230')
Total GB: 350.0
```

From the output, we can see that if we uncompress the biggest 5 files which are next to be processed in the queue, they will occupy 350 GB. To copy and uncompress them we should just change the `count` argument to `unzip`:

```
python copy_script.py unzip big 5
```

When the files are successfully uncompressed, we can just start processing them with the `run_script.sh` in run mode:
```
bash run_script.sh
```

After some time, when some of the files are done processing, we can use the `upload_locally.py` script to transfer the results from the server to the NFS before uploading it to the Internet Archive and also to remove from the server the results after they are transferred and the data copied with the `copy_script.py`.
```
python upload_locally.py
```
