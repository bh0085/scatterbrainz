import remote_sql.PyGWrapper as pgw

def artistGID(name = "Black Sabbath"):
    cxn = pgw.PyGWrapper()
    cursor = cxn._cursor()
    cursor.execute("""
SELECT gid FROM artist WHERE name = '"""+name+"""';
""")
    out = cursor.fetchall()
    if len(out) == 0:
        raise Exception("Artist: "+name+" Not Found")
    if len(out) == 1:
        return out[0][0]
    if len(out) > 1:
        cursor.execute("""
select artist.gid as artist_gid, count(*) 
from artist, album 
where artist.id = album.artist 
and artist.name='Nirvana' 
group by artist_gid 
order by count desc 
limit 1;
""")
        out = cursor.fetchone() 
        print "Warning, artist selection not unique, Selecting the one with the most releases."
        return out[0]





def getArtistReleases(name = "Black Sabbath"):
    gid = artistGID(name)
    cxn = pgw.PyGWrapper()
    cursor = cxn._cursor()
    cursor.execute("""
SELECT 
   min(substr(release.releasedate,1,4)) as earliest_release,
   album.name as album_name,
   artist.name as artist_name
FROM artist, album, release 
WHERE artist.gid = '"""+gid+"""' 
AND   cast(substr(release.releasedate,1,4) as int) > 0
AND   album.artist = artist.id 
AND   release.album = album.id 
GROUP BY album_name, artist_name
ORDER BY earliest_release
""")
    d =cxn.fetchDict(cursor)
    return d


