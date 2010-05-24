import what.whathelpers as wh
import dbs.config.prefs as prefs
import urllib

def getArtist(name):
    strname=name.lower()
    user = prefs.readPref('what_sb_user')
    wo= wh.openerForUser(user)
    o = wo.opener()
    f = o.open("http://what.cd/artist.php",urllib.urlencode({'artistname':strname}))
    artist_html = f.read()

    db = dbConnect(user)
    if db.exists("select * from artist where artist.name = :name",{'name':strname}):
        artid = db.queryToDict(
"""
select id 
from artist 
where artist.name = :name
"""
                               ,{'name':strname})
        
    else:
        arthtml

    return d
