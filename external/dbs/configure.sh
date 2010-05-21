#!/bin/bash

function writeval
{
    vname=$1
    eval vval="$"$vname
    echo export "$vname"="$vval" >> $dbfile
}

function echoval
{
    vname=$1
    eval vval="$"$vname
    echo "   $vname"="$vval"
}


function usage
{
    echo "Usage: configure.sh [options]"
    echo "  --mb-port=[5432]"
    echo "  --mb-host=[localhost]"
    echo "  --mb-local"
}

PG_PORT=5432
PG_HOST=localhost
MB_LOCAL=1
SB_PORT=5000
SB_ADDRESS=''
for i in $* ; do
  case "$i" in
      --mb-host* ) PG_HOST=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;;
      --mb-port* ) PG_PORT=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;; 
      --no-mb-local ) MB_LOCAL=0 ;; 
      --sb-port* ) SB_PORT=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;;
      --sb-address* ) SB_ADDRESS=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;;
      --sb-user* ) SB_USER=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;;
      --sb-password* ) SB_PASS=`echo $i | sed 's/^.*=\(.*\)/\1/'` ;;
      --help ) usage; exit 0 ;;
      * ) usage; error_exit "$LINENO unhandled option: $i" ;;
  esac
done


[[ -n "$SB_DIR" ]] || error_exit "$LINENO no sbdir"

dbfile=${SB_DIR}/dbs.conf
echo '#This is an automatically generated config file from configure.sh' > $dbfile
echo '' >> $dbfile

echo "...Writing SB Defaults"
writeval SB_DIR
SB_CONF_DIR=${SB_DIR}/external/dbs/config
SB_CONF_DB=${SB_CONF_DIR}/config.sqlite
SB_MUSIC_DIR=${SB_DIR}/external/dbs/music
SB_MUSIC_DB=${SB_MUSIC_DIR}/music.sqlite
SB_FRIENDS_DIR=${SB_DIR}/external/dbs/friends
SB_FRIENDS_DB=${SB_FRIENDS_DIR}/friends.sqlite
SB_DOCUMENT_ROOT=${SB_DIR}/public
SB_MUSIC_LIB_ABS=${SB_DOCUMENT_ROOT}/.music
SB_MUSIC_LIB=.music


writeval SB_CONF_DIR
writeval SB_CONF_DB
writeval SB_MUSIC_DIR
writeval SB_MUSIC_DB
writeval SB_DOCUMENT_ROOT
writeval SB_MUSIC_LIB_ABS
writeval SB_MUSIC_LIB
writeval SB_FRIENDS_DIR
writeval SB_FRIENDS_DB
writeval SB_ADDRESS
writeval SB_PORT
writeval SB_USER
writeval SB_PASS

echo "...Writing MBrainz prefs"

writeval MB_LOCAL
writeval PG_PORT
writeval PG_HOST
MB_PORT=$PG_PORT
MB_HOST=$PG_HOST
writeval MB_HOST
writeval MB_PORT

echoval MB_LOCAL
echoval MB_HOST
echoval MB_PORT
echoval SB_USER

MB_DIR=${SB_DIR}/external/dbs/mbrainz
writeval MB_DIR
exit 0