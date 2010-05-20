#!/bin/bash
host='94.100.21.250'
port='64077'
dbname='whatstuff'
psql -h $host -d 'template1' -p $port -c 'CREATE DATABASE '$dbname';'
psql -h $host -d $dbname -p $port --file='initwhat.sql'

exit 1