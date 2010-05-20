#!/bin/bash

function makemyconf(){
    echo "#Bind shell variables here to seed config." > my.conf
    echo "#e.g:" >> my.conf
    echo "" >> my.conf
    echo "#PG_PORT=5432" >> my.conf
    echo "#PG_HOST=localhost" >> my.conf
    echo "" >> my.conf
    echo "#Allowable variables:" >> my.conf
    echo "#  PG_PORT, PG_HOST, MB_LOCAL, SB_PORT, SB_ADDRESS" >> my.conf
    echo "
PG_HOST=localhost
PG_PORT=5432
MB_LOCAL=1
SB_ADDRESS=94.100.21.250
SB_PORT=5000
" >> my.conf
}

function usage(){
    echo "Usage: configure.sh [--opts]"
    echo "   Run with no arguments to create a my.conf file."
    echo "opts:"
    echo "   --config"
}



MAKE_CONF_ONLY=1
for i in $* ; do
    case "$i" in
	--help ) usage; exit 0 ;;
	--config ) MAKE_CONF_ONLY=0;;
	* ) usage; error_exit "$LINENO unhandled option: $i" ;;
    esac
done

if [[ ! -f my.conf ]] 
then
    echo "My.conf does not yet exist... creating with default values."
    echo "edit my.conf and then rerun ./configure."
    makemyconf
else
    echo "My.conf already exists... skipping."
fi

if [[ $MAKE_CONF_ONLY == 1 ]]
then
    echo
    echo "exiting..."
    exit 0
fi

source my.conf

cd `dirname $0`
export SB_DIR=`pwd`
cd $SB_DIR
echo
dbcflags="--mb-host=$PG_HOST --mb-port=$PG_PORT --sb-address=$SB_ADDRESS --sb-port=$SB_PORT"
[[ $MB_LOCAL == 0 ]] && dbcflags=`echo "$dbcflags" --no-mb-local`
dbcfile="external/dbs/configure.sh `echo $dbcflags`"
$dbcfile
exit