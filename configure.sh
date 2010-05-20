#!/bin/bash

PG_HOST=localhost
PG_PORT=5432
MB_LOCAL=1
for i in $* ; do
  case "$i" in
    --mb-host* ) PG_HOST=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;;
    --mb-port* ) PG_PORT=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;; 
    --no-mb-local* ) MB_LOCAL=0 ;; 
    --help ) usage; exit 0 ;;
    * ) usage; error_exit "$LINENO unhandled option: $i" ;;
  esac
done

cd `dirname $0`
export SB_DIR=`pwd`
cd $SB_DIR
echo "Running dbs/configure.sh with no options"
echo
echo "$0 Running init scripts with Settings: "
echo "   PG_HOST = $PG_HOST"
echo "   PG_PORT = $PG_PORT"
echo "   MB_LOCAL= $MB_LOCAL"
echo
dbcflags="--mb-host=$PG_HOST --mb-port=$PG_PORT"
[[ $MB_LOCAL == 0 ]] && dbcflags=`echo "$dbcflags" --no-mb-local`
dbcfile="external/dbs/configure.sh `echo $dbcflags`"
$dbcfile
exit