#!/usr/bin/bash

docker rmi ic-registry.epfl.ch/mediawiki_docker/mediawiki_final
cd mediawiki_ready

docker build -t mediawiki_final .
docker tag mediawiki_final ic-registry.epfl.ch/mediawiki_docker/mediawiki_final
docker push ic-registry.epfl.ch/mediawiki_docker/mediawiki_final
