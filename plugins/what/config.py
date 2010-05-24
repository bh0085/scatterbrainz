import dbs.config.queryConfig as qc
import dbs.config.prefs as prefs
import sqliteWrapper as sqw

import os
def configure(what_user,what_pass,what_dir,sb_user):
    """
Configure user level preferences for the what.cd plugin.
Writes 'what_user', 'what_pass', 'what_dbfile'

To the user_prefs db for sb_user.      
    """
    #Write prefs to user preferences
    what_dbfile=os.path.join(what_dir,'what_'+sb_user+'.sqlite')
    prefs.writePref('what_user',what_user,sb_user)
    prefs.writePref('what_pass',what_pass,sb_user)
    prefs.writePref('what_dbfile',what_dbfile,sb_user)

def unconfigure(sb_user):
    #Write prefs to user preferences
    prefs.deletePref('what_user',sb_user)
    prefs.deletePref('what_pass',sb_user)
    prefs.deletePref('what_dbfile',sb_user)    

def insertPrefs(db,sb_user):
    """
Write preferences to the db database.
    """
    dbfile = prefs.readPref('what_dbfile',sb_user)
    dbpath = os.path.dirname(dbfile)
    db_filepath = os.path.join(dbpath,sb_user+'_files')
    if not os.path.isdir(db_filepath): os.mkdir(db_filepath)
    
    db.query("""
insert into config(name,value) values('db_path',:dbpath);
""",{'dbpath':dbpath})
    db.query("""
insert into config(name, value) values('db_file',:dbfile);
""",{'dbfile':dbfile})

    db.query("""
insert into config(name,value) values('db_filepath',:db_filepath);
""",{'db_filepath':db_filepath})


def init(sb_user):
    """
Initialize the plugin db.
    """
    dbfile = prefs.readPref('what_dbfile',sb_user)
    db = sqw.sqliteWrapper(dbfile)
    d = db.queryToDict('''select name from sqlite_master where type = 'table';''')
    for table in d:
        db.query("""drop table '""" + table['name'] + """';""")
    
    db.query("""
CREATE TABLE config(
id INTEGER PRIMARY KEY,
name TEXT UNIQUE,
value TEXT
)
""")

    insertPrefs(db,sb_user);

    db.query("""
CREATE TABLE artist(
id INTEGER PRIMARY KEY,
whatid INTEGER UNIQUE,
name TEXT
)""")
    db.query("""
CREATE TABLE release(
id INTEGER PRIMARY KEY,
whatid INTEGER UNIQUE,
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
CREATE TABLE artist_release(
id INTEGER PRIMARY KEY,
artist INTEGER,
release INTEGER UNIQUE,
FOREIGN KEY(release) REFERENCES release(id),
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
