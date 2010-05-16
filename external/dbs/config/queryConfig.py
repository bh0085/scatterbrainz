import sqliteWrapper as swrap
import os
def query(prefname):
    dbfile = os.path.join(os.environ['SCATTERBRAINZ_DIR'],'external/dbs/config/config.sqlite')
    sqw = swrap.sqliteWrapper(dbfile)
    d = sqw.queryToDict('''
SELECT name, value FROM global;
''')
    d = sqw.queryToDict("""
SELECT
 name, value 
FROM
 global 
WHERE
 name = '"""+prefname+"""';
""")
    return d[0]['value']
