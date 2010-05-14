import remote_sql.PyGWrapper as pw

def artistGID(name = "Black Sabbath"):
    cxn = pw.PyGWrapper()
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

def getMBIDArtistMembers(gid):
    cxn = pw.PyGWrapper()
    cursor = cxn._cursor()
    cursor.execute("""SELECT
track.name as track_name, artist.name as orig_name, artist2.name as artist_name
from artist , artist as artist2, track, l_artist_track as art_track
where artist.gid = '"""+gid+"""'
AND artist.id = track.artist
AND art_track.link0 = artist2.id
AND art_track.link1 = track.id
LIMIT 10;
""")
    d =cxn.fetchDict(cursor)  
    for item in d: item['name']= item['artist_name']
    return d

def getMBIDAlbumMembers(gid):
    pass


def getMBIDAlbumTracks(gid):
    cxn = pw.PyGWrapper()
    cursor = cxn._cursor()
    cursor.execute("""
SELECT 
   track.gid as track_mbid,
   track.name as track_name,
   album.name as album_name,
   albumjoin.sequence as track_number
FROM  album, albumjoin, track 
WHERE album.gid = '"""+gid+"""' 
AND   albumjoin.album = album.id 
AND   track.id = albumjoin.track
GROUP BY track_name, album_name, track_mbid, track_number
ORDER BY track_number
""")
    d =cxn.fetchDict(cursor)  
    for item in d: item['name']= item['track_name']
    return d
  

def getMBIDArtistAlbums(gid):
    cxn = pw.PyGWrapper()
    cursor = cxn._cursor()
    cursor.execute("""
SELECT 
   min(substr(release.releasedate,1,4)) as earliest_release,
   album.gid as album_mbid,
   album.name as album_name,
   artist.name as artist_name
FROM artist, album, release 
WHERE artist.gid = '"""+gid+"""' 
AND   cast(substr(release.releasedate,1,4) as int) > 0
AND   album.artist = artist.id 
AND   release.album = album.id 
GROUP BY album_name, artist_name, album_mbid
ORDER BY earliest_release
""")
    d =cxn.fetchDict(cursor)  
    for item in d: 
        item['name']= item['album_name']
        item['year']= item['earliest_release']
    return d
  

def getArtistReleases(name = "Black Sabbath"):
    gid = artistGID(name)
    return getMBIDArtistAlbums(gid)



