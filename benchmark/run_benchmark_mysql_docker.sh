#!/bin/bash

docker run \
       --rm \
       -d \
       --name rp_mysql \
       -e MYSQL_ROOT_PASSWORD=root \
       --mount type=bind,source="$(pwd)/benchmark.sql",target="/docker-entrypoint-initdb.d/dump.sql" \
       mysql:5.7
