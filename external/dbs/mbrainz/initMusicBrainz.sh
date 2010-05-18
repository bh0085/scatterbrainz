#!/bin/bash

function usage(){
	  echo 'Usage:'
	  echo 'initMusicbrainz -hd'
	  echo '  h: help'
	  echo '  d: downlooad musicbrainz'
	  echo '  p "port": set postgres port'
}

#define progrname for calls to error_exit...
#PROGNAME=$(basename $0)

#option flags.
doDL=0
doInit=0
PGPORT=5432
mbserve_dir=`pwd`/mb_server

while getopts "hdip:" flag
do
  case $flag in
      h)
	  usage;;
      d)
          doDL=1;;
      p)
          PGPORT=$OPTARG;;
      i)
	  doInit=1;;
      *) 
          echo 'unhandled'
      
  esac
done

if (( doDL ))
then
    echo "Downloading musicbrainz database files."
    if [ -d mb_server ]
    then
	echo "MBrainz appears to already be downloaded"
    fi
    svn co http://svn.musicbrainz.org/mb_server/branches/RELEASE_20090524-BRANCH/ mb_server
fi

cd $mbserve_dir 

if (( doInit ))
then 
    echo "Initializing the musicbrainz db......"
    echo

    echo "Checking perl modules..."
    which -s perl    
    if (( $? != 0 ))
    then
	error_exit "Line $LINENO perl binary not found"
    fi
    #silently test for perl modules
    required="DBD::Pg DBI String::ShellQuote LWP::UserAgent"
    for mod in $required
    do
	perl -M"${mod}" -e 1 >/dev/null 2>&1 
	if (( $? != 0 ))
	then
	    error_exit "Line $LINENO missing perl module $mod"
	fi
    done
    echo "Success: All perl modules are installed"

    echo


    echo "Creating DBDefs and putting a secret checksum into the config"
    cp cgi-bin/DBDefs.pm.default  cgi-bin/DBDefs.pm
    rndnum=014501
    dbd=cgi-bin/DBDefs.pm
    var="`cat $dbd | sed 's|sub SMTP_SECRET_CHECKSUM { "" }|sub SMTP_SECRET_CHECKSUM { "'${rndnum}'" }|'`"
    echo "Success"
    echo
    echo "$var" > $dbd
    echo "Setting DBDefs port"
    var="`cat $dbd | sed 's|port	=> ""|port	=> "'${PGPORT}'"|'`"
    echo "Success"
    echo "$var" > $dbd
    echo

    dumpname=20100515-000002
    echo "Getting the MB dumps: "
    echo "Input a dumpname, (check:ftp://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport for LATEST)"
    echo default: "${dumpname}"
    read -p "dump name:" dumpname
    echo $dumpname
    if [ "$dumpname" == "" ]
    then
	dumpname=20100515-000002
    fi
    
    files="mbdump-derived.tar.bz2 mbdump.tar.bz2 mbdump-artistrelation.tar.bz2"
    for f in $files
    do
	if [ -e $f ]
	then
	    echo "$f: dump already downloaded"
	else
	    wget "ftp://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/${dumpname}/$f"
	fi
    done
    echo "Success: Dumps downloaded."
    echo
    
    echo "Switching to postgres user for database config"
    su postgres -c "./admin/InitDb.pl --createdb --empty-database"
    echo "Success: Created empty musicbrainz database"
    echo
    echo "Importing database tables from mbrainz dumps"
    ./admin/InitDB.pl --import mbdump*.tar.bz2
    echo "Success, configured database"
    echo

    #Trigram indexing for tagger lookups.
    echo "Adding pg_trgm support"
    echo "Note: "
    echo "  at this point, initialization requires that the current user has a role in the db."
    trgmfile=`pg_config --sharedir`"/contrib/pg_trgm.sql"
    psql -p $PGPORT -d musicbrainz_db -f "$trgmfile"
    psql -p $PGPORT -d musicbrainz_db -c "CREATE INDEX art_trgm_idx ON artist USING gist (name gist_trgm_ops);"
    psql -p $PGPORT -d musicbrainz_db -c "CREATE INDEX album_trgm_idx ON artist USING gist (name gist_trgm_ops);"
    echo "Success: added trigram indexing to the musicbrainz DB!"


    echo 
    echo "Setting up the crontab for slave server"
    #Create crontab for the slave server
    if [ ! -d ~/.cron ]
    then
	mkdir ~/.cron
    fi

    cp admin/cron/slave.sh ~/.cron/slave.sh
    echo "Calling sudo to change execution mode"
    sudo chmod 777 ~/.cron/slave.sh
    echo "To enable cron server updating, add ~/.cron/slave.sh to your crontab as:"
    echo "---"
    echo "10 1,7 * * * ~/.cron/slave.sh" 
    echo "---"
    echo "For twice daily execution"
    echo
    read -p "hit enter to continue"
    echo 'Pointing cron job to: '$mbserve_dir
    cat ~/.cron/slave.sh | sed 's|cd.*|cd '$mbserve_dir'|' > ~/.cron/slave.sh
    echo "Success: copied slave cron scripts"
    echo
    echo 
    echo "Done setting up the DB!"   


else
    echo "Not setting up mbrainz db..."
    echo "To set up postgres, run initMusicBrainz with the -i option."	
    
fi 

exit 0