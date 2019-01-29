#!/usr/bin/env bash


echo "Starting Influxdb Server under Docker..."

docker pull influxdb

docker run  --publish published=8086,target=8086 \
            --publish published=8089,target=8089,protocol=udp \
            -v -v $PWD/conf/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
            influxdb -config /etc/influxdb/influxdb.conf
