import os
import sqliteWrapper as swrap
import pprint as pr

print 'Initializing the config db'

scatterbrainz_dir = os.environ['SB_DIR']
media_dir = os.environ['SB_MUSIC_LIB_ABS']
music_dir = os.environ['SB_MUSIC_DIR']
music_dbfile = os.environ['SB_MUSIC_DB']
config_dir = os.environ['SB_CONF_DIR']
config_dbfile = os.environ['SB_CONF_DB']
mb_port = os.environ['MB_PORT']
mb_host = os.environ['MB_HOST']
friends_dir = os.environ['SB_FRIENDS_DIR']
friends_dbfile=os.environ['SB_FRIENDS_DB']
sb_address=os.environ['SB_ADDRESS']
sb_port=os.environ['SB_PORT']

sqw = swrap.sqliteWrapper(config_dbfile)
d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
if not 'global' in map(lambda x: x['name'],d):
    sqw.query('''
CREATE TABLE global(
  id INTEGER PRIMARY KEY,
  name TEXT,
  value);
''')

##delete any global prefs that exist
sqw.query("""DELETE FROM global""")

names =  sqw.queryToDict("SELECT name FROM global")

init_prefs = {
    'mbhost' : mb_host,
    'mbport' : mb_port,
    'mbdb' : 'musicbrainz_db',
    'mbuser' : 'bh0085',
    'scatterbrainz_dir':scatterbrainz_dir,
    'music_lib':media_dir,
    'music_dir':music_dir,
    'music_dbfile':music_dbfile,
    'friends_dir':friends_dir,
    'friends_dbfile':friends_dbfile,
    'config_dir':config_dir,
    'config_dbfile':config_dbfile,
    'sb_address':sb_address,
    'sb_port':sb_port
}
for k, item in init_prefs.iteritems():
    sqw.query("""
INSERT INTO global(name,value) values('"""+k+"""','"""+item+"""');
""")

d = sqw.queryToDict('''
SELECT name, value FROM global;
''')
print "Configs set in Python DB: "
sqw.commit();
for entry in d:
    print "   "+entry['name'] + ':    '+entry['value']
exit(1)
