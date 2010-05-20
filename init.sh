#!/bin/bash
cd `dirname $0`
export SB_DIR=`pwd`
cd $SB_DIR
echo "Running dbs/initDBS.sh with no options"
echo
dbifile=external/dbs/initDBS.sh
echo ${dbifile}:
$dbifile
exit