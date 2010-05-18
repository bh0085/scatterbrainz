#/bin/bash

function usage(){
	  echo 'Usage:'
	  echo 'initMusicbrainz -hd'
	  echo '  -p (port): specify a port for mbrainz db'
	  echo '  -d: set up postgres musicbrainz db'
	  echo '  -m: set up local music db'
	  echo '  -c: set up local configuration db'
}

doMB=0
doConfig=0
doMusic=0
PGPORT=5432
dbs_dir=`pwd`
while getopts "mp:cdh" flag
do
  case $flag in
      h)
	  usage;;
      m)
          doMusic=1;;
      p)
          PGPORT=$OPTARG;;
      c)
	  doConfig=1;;
      d)
	  doMB=1;;
      *) 
          echo 'unhandled'
  esac
done

if (( $doMB == 1 ))
then
    echo "INITDBS: Initializing MBrainz db with port: " $PGPORT
    cd ${dbs_dir}/mbrainz
    ./initMusicBrainz.sh -d -i
    echo
    echo
fi

if (( $doConfig == 1 ))
then
    echo "INITDBS: Initializing config"
    cd ${dbs_dir}/config
    python initConfig.py
    echo
    echo
    
fi

echo $dbs_dir
if (( $doMusic == 1 ))
then
    echo "INITDBS: Initializing local music db with reset-all"
    cd ${dbs_dir}/music
    python initMusic.py --reset-all

    echo
    echo
fi

exit 1