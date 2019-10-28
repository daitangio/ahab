#!/bin/bash

export PING_HOST=127.0.0.1
docker-compose -f slow-pinger.yml  build && (
 docker stack up --compose-file slow-pinger.yml pinger1
)
docker service logs -f pinger1_slow_ping
