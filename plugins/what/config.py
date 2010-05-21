import dbs.config.queryConfig as qc
import os.path
import dbs.config.prefs as prefs
import sqliteWrapper as sqw

def configure():
    sb_dir = qc.query('scatterbrainz_dir')
    what_dir =os.path.join(sb_dir,'external/dbs/what')
    print "Setup what.cd for which SB user?"
    sb_user = raw_input('username: ')
    print "\nWhat.cd username?"
    what_user = raw_input('username: ')
    print "\nWhat.cd password "
    what_pass = raw_input('password: ')
    what_dbfile=os.path.join(what_dir,'what_'+sb_user)
    prefs.writePref('what_sb_user',sb_user)
    prefs.writePref('what_user',what_user,sb_user)
    prefs.writePref('what_pass',what_pass,sb_user)
    prefs.writePref('what_dbfile',what_dbfile,sb_user)

def init():
    sb_user = prefs.readPref('what_sb_user')
    dbfile = prefs.readPref('what_dbfile',sb_user)
    db = sqw.sqliteWrapper(dbfile)
    d = db.queryToDict('''select name from sqlite_master where type = 'table';''')
    for table in d:
        db.query("""drop table '""" + table['name'] + """';""")
    
    
    db.query("""
CREATE TABLE artist(
id INTEGER PRIMARY KEY,
name TEXT
)""")
    db.query("""
CREATE TABLE release(
id INTEGER PRIMARY KEY,
name TEXT
)""")
    db.query("""
CREATE TABLE artist_gids(
id INTEGER PRIMARY KEY,
artist INTEGER,
gid TEXT,
FOREIGN KEY(artist) REFERENCES artist(id)
);""")
    db.query("""
CREATE TABLE release_gids(
id INTEGER PRIMARY KEY,
release INTEGER,
gid TEXT,
FOREIGN KEY(release) REFERENCES release(id)
);""")
    db.query("""
CREATE TABLE artist_html(
id INTEGER PRIMARY KEY,
artist INTEGER UNIQUE,
filename TEXT,
FOREIGN KEY(artist) REFERENCES artist(id)
)""")
    db.query("""
CREATE TABLE release_html(
id INTEGER PRIMARY KEY,
release INTEGER UNIQUE,
filename TEXT,
FOREIGN KEY(release) REFERENCES release(id)
)""")
    db.commit()
    db.close()
