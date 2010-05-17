import os
import sqliteWrapper as swrap
import pprint as pr

print 'Initializing the config db'

scatterbrainz_dir = os.environ['SCATTERBRAINZ_DIR']
music_dir = os.path.join(scatterbrainz_dir,'public/.music')
conf_dir = os.getcwd()

dbfile = os.path.join(conf_dir,'config.sqlite')
sqw = swrap.sqliteWrapper(dbfile)
d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
if not 'global' in map(lambda x: x['name'],d):
    sqw.query('''
CREATE TABLE global(
  id INTEGER PRIMARY KEY,
  name TEXT,
  value);
''')

##delete any global prefs that exist
print  'WIPING PREFERENCES TO DEFAULT VALUES'
sqw.query("""DELETE FROM global""")

names =  sqw.queryToDict("SELECT name FROM global")
print names
if names == None:
    names_set = []
else:
    names_set = map(lambda x: ( x['name']) ,names )

init_prefs = {
    'mbhost' : 'rosa.feralhosting.com',
    'mbport' : '64077',
    'mbdb' : 'musicbrainz_db',
    'mbuser' : 'bh0085',
    'scatterbrainz_dir':scatterbrainz_dir,
    'music_dir':music_dir,
    'music_dbfile':os.path.join(scatterbrainz_dir,'external/dbs/music/music.sqlite'),
    'config_dbfile':os.path.join(scatterbrainz_dir,'external/dbs/config/config.sqlite')
}
for k, item in init_prefs.iteritems():
    sqw.query("""
INSERT INTO global(name,value) values('"""+k+"""','"""+item+"""');
""")

d = sqw.queryToDict('''
SELECT name, value FROM global;
''')
sqw.commit();
for entry in d:
    print entry['name'] + ':    '+entry['value']
exit(1)
