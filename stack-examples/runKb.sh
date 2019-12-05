#!/bin/bash
# Try elastic press plugin
set -v 
export wordpress=$(pwd)/kbdir
export db=$(pwd)/kbdb
export elasticdata=$(pwd)/elasticdata
docker stack deploy  -c wordpress-kb.yml kb
# curl http://127.0.0.1:9200/_cat/healt
docker stack services kb
docker service logs kb_wordpress
docker service logs kb_elasticsearch