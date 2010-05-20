import sys
def usage():
    print 'acceptable args: help, reset-all, reset-meta'

def main(argv):
    import os
    from mutagen.easyid3 import EasyID3
    import dbs.config.queryConfig as qc
    import sqliteWrapper as swrap
    import getopt
    do_reset = False
    do_reset_meta = False
    try:  
        opts, args = getopt.getopt(argv, '',['reset-all','reset-meta','help'])
    except getopt.GetoptError, e:
        print e
        usage()                         
        sys.exit(2)      
    for opt, arg in opts:  
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit()                  
        elif opt == '--reset-all':
            do_reset = True
        elif opt == '--reset-meta':
            do_reset_meta = True
    
    sb_dir = qc.query('scatterbrainz_dir')
    music_dir = qc.query('music_dir')
    tracks_dir = os.path.join(music_dir,'tracks')
    dbfile = qc.query('music_dbfile')

    
    sqw = swrap.sqliteWrapper(dbfile)

    if do_reset:
        d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
        print 'Resetting all music tables'
        for table in d:
            sqw.query("""drop table '""" + table['name'] + """';""")
    if do_reset_meta:
        d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
        print 'Resetting music meta tables'
        for table in d:
            if table['name'][-4:] == 'meta':
                sqw.query("""drop table '""" + table['name'] + """';""")


    d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
    if not 'tracklist' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE tracklist(
      id INTEGER PRIMARY KEY,
      gid TEXT UNIQUE);
    ''')
    if not 'album' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE album(
      id INTEGER PRIMARY KEY,
      gid TEXT UNIQUE,
      artist INT,
      name TEXT,
      FOREIGN KEY(artist) REFERENCES artist(id)
); 

    ''')
    if not 'artist' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE artist(
      id INTEGER PRIMARY KEY,
      gid TEXT UNIQUE,
      name TEXT UNIQUE);
    ''')
    if not 'track' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE track(
      id INTEGER PRIMARY KEY,
      listing INTEGER UNIQUE,
      gid TEXT UNIQUE,
      name TEXT,
      number INTEGER,
      length INTEGER,
      album INTEGER,
      artist INTEGER,
      FOREIGN KEY(listing) REFERENCES tracklist(id),
      FOREIGN KEY(album) REFERENCES album(id),
      FOREIGN KEY(artist) REFERENCES artist(id)
    );
    ''')
    if not 'artist_meta' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE artist_meta(
      id INTEGER PRIMARY KEY,
      artist INTEGER UNIQUE,
      name TEXT,
      FOREIGN KEY(artist) REFERENCES artist(id)  
    );
    ''')
    if not 'album_meta' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE album_meta(
      id INTEGER PRIMARY KEY,
      gid TEXT UNIQUE);
    ''')
    if not 'albumjoin' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE albumjoin(
      id INTEGER PRIMARY KEY,
      track INTEGER UNIQUE,
      album INTEGER,
      artist INTEGER,
      FOREIGN KEY(track) REFERENCES track(id),
      FOREIGN KEY(album) REFERENCES album(id),
      FOREIGN KEY(artist) REFERENCES artist(id)
    );
    ''')

if __name__ == "__main__":
    exit(main(sys.argv[1:]))

exit(1)

                                   
