#/bin/bash

function usage(){
	  echo 'Usage:'
	  echo 'initMusicbrainz -hd'
	  echo '  -p (port): specify a port for mbrainz db'
	  echo '  -d: set up postgres musicbrainz db'
	  echo '  -m: set up local music db'
	  echo '  -c: set up local configuration db'
}

dbcfile=$SB_DIR/dbs.conf
source $dbcfile


if (( $MB_LOCAL == 1 ))
then
    echo "INITDBS: Initializing MBrainz db with port: " $MB_PORT
    cd $MB_DIR
    ./initMusicBrainz.sh -d -i -p $MB_PORT
    echo
    echo
fi

echo "INITDBS: Initializing config"
cd ${SB_CONF_DIR}
python initConfig.py
echo
echo
    
echo "INITDBS: Initializing local music db with reset-all"
cd ${SB_MUSIC_DIR}
python initMusic.py --reset-all
echo
echo
    
echo "INITDBS: Initializing local friends db with reset-all"
cd ${SB_FRIENDS_DIR}
python initFriends.py --reset-all
echo
echo

exit 1