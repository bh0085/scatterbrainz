import remote_sql.PyGWrapper as pw

def getMBIDAlbumInfo(gid):
    d = pw.PyGWrapper().queryToDict("""
SELECT 
   album.gid as album_mbid,
   album.name as album_name,
   artist.name as artist_name
FROM artist, album
WHERE album.gid = '"""+gid+"""' 
AND   album.artist = artist.id 
""")    
    for item in d:
        item['name'] = item['album_name']
    return d


def getAllArtists():
    d = pw.PyGWrapper().queryToDict("""
SELECT 
   artist.name as artist_name, artist.gid as artist_gid
FROM artist, album
WHERE artist.id = album.artist
LIMIT 20;
""")
    for item in d: 
        item['name'] = item['artist_name']
        item['artist_mbid']= item['artist_gid']
    return d


def getMBIDArtistAlbums(gid):
    d = pw.PyGWrapper().queryToDict("""
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
    for item in d: 
        item['name']= item['album_name']
        item['year']= item['earliest_release']
    return d
def getMBIDArtistTracks(gid):
    d = pw.PyGWrapper().queryToDict("""
SELECT 
   track.gid as track_mbid,
   track.name as track_name,
   artist.name as artist_name
FROM artist, track 
WHERE artist.gid = '"""+gid+"""' 
AND   track.artist = artist.id 
LIMIT 20;
""")
    for item in d: 
        item['name']= item['track_name']
    return d 

def getMBIDArtistMembers(gid):


    d = pw.PyGWrapper().queryToDict("""SELECT
artist2.name as artist_name,
artist2.gid as artist_mbid,
album.name as album_name,
min(substr(release.releasedate,1,4)) as earliest_release
FROM
artist , artist as artist2, 
track, 
l_artist_track as art_track,
release,
albumjoin,
album
WHERE artist.gid = '"""+gid+"""'
AND   cast(substr(release.releasedate,1,4) as int) > 0
AND artist.id = track.artist
AND art_track.link0 = artist2.id
AND art_track.link1 = track.id
AND albumjoin.track = track.id
AND albumjoin.album = album.id
AND release.album = album.id
GROUP BY  artist_name, album_name, artist_mbid
ORDER BY earliest_release
LIMIT 500;
""")
    for item in d: item['name']= item['artist_name']
    for item in d: item['year']= item['earliest_release']
    return d




def getAllAlbums():
    d = pw.PyGWrapper().queryToDict("""
SELECT 
   album.gid as album_mbid,
   album.name as album_name
FROM  album
LIMIT 20;
""")
    for item in d: item['name']= item['album_name']
    return d

def getMBIDAlbumMembers(gid):
    d = pw.PyGWrapper().queryToDict("""SELECT
track.name as track_name, artist2.name as artist_name
from album,albumjoin , artist as artist2, track, l_artist_track as art_track
where album.gid = '"""+gid+"""'
AND albumjoin.album = album.id
AND albumjoin.track = track.id
AND art_track.link0 = artist2.id
AND art_track.link1 = track.id
LIMIT 20;
""")
    for item in d: item['name']= item['artist_name']
    return d


def getMBIDAlbumTracks(gid):
    d = pw.PyGWrapper().queryToDict("""
SELECT 
   track.gid as track_mbid,
   track.name as track_name,
   album.name as album_name,
   albumjoin.sequence as track_number,
   track.length as track_length
FROM  album, albumjoin, track 
WHERE album.gid = '"""+gid+"""' 
AND   albumjoin.album = album.id 
AND   track.id = albumjoin.track
ORDER BY track_number
""")
    for item in d: item['name']= item['track_name']
    return d
  




def getAllTracks():
    d = pw.PyGWrapper().queryToDict("""
SELECT 
   track.gid as track_mbid,
   track.name as track_name
FROM  track 
LIMIT 20;
""")
    for item in d: item['name']= item['track_name']
    return d


    
def getAllMembers():
    return []
