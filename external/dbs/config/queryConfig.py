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
    sqw.close()
    return d[0]['value']
def autoset(prefname):
    cdb = query('config_dbfile')
    sqw = swrap.sqliteWrapper(cdb)
    if prefname == 'sb_address':
        val = unicode(autogetip())
        sqw.query("""
UPDATE global SET value = :val WHERE name = :prefname;
""", params={'val':val,'prefname':prefname})
        sqw.commit()


def autogetip():
    import urllib2
    o = urllib2.build_opener()
    ip= o.open("http://www.whatismyip.org/").read()
    o.close()
    return ip
