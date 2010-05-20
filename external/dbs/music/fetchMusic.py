#FETCH TRACKS FROM THE LOCAL DBS GIVEN PARAMETERS DICT.
import sqliteWrapper as sw
import dbs.config.queryConfig as qc

def fetchWithParams(params):
    sqw = sw.sqliteWrapper(qc.query('music_dbfile'))
    d = sqw.queryToDict("select * from tracklist")
    sqw.close()
    return d


def getMBIDAlbumInfo(gid):
    d = sw.queryOnce(qc.query("music_dbfile"),"""
SELECT 
   album.gid as album_mbid,
   album.name as album_name,
   artist.name as artist_name
FROM artist, album
WHERE album.gid = :gid 
AND   album.artist = artist.id 
""",params={'gid':gid})    
    for item in d:
        item['name'] = item['album_name']
    return d


def getAllArtists():
    d = sw.queryOnce(qc.query("music_dbfile"),"""
SELECT 
   artist.name as artist_name, artist.gid as artist_gid
FROM artist
""")
    for item in d: 
        item['name'] = item['artist_name']
        item['artist_mbid']= item['artist_gid']
    return d


def getMBIDArtistAlbums(gid):
    d = sw.queryOnce(qc.query("music_dbfile"),"""
SELECT 
   album.gid as album_mbid,
   album.name as album_name,
   artist.name as artist_name
FROM artist, album 
WHERE artist.gid = :gid
AND   album.artist = artist.id 
""",params={"gid":gid})
    for item in d: 
        item['name']= item['album_name']
    return d
def getMBIDArtistTracks(gid):
    d = sw.queryOnce(qc.query("music_dbfile"),"""
SELECT 
   track.gid as track_mbid,
   track.name as track_name,
   artist.name as artist_name
FROM artist, track 
WHERE artist.gid = :gid 
AND   track.artist = artist.id 
LIMIT 20;
""",params = {"gid":gid})
    for item in d: 
        item['name']= item['track_name']
    return d 

def getMBIDArtistMembers(gid):
    return []

def getAllAlbums():
    d = sw.queryOnce(qc.query("music_dbfile"),"""
SELECT 
   album.gid as album_mbid,
   album.name as album_name
FROM  album
LIMIT 20;
""")
    for item in d: item['name']= item['album_name']
    return d

def getMBIDAlbumMembers(gid):
    d = sw.queryOnce(qc.query("music_dbfile"),"""SELECT
track.name as track_name, artist2.name as artist_name
from album,albumjoin , artist as artist2, track, l_artist_track as art_track
where album.gid = :gid
AND albumjoin.album = album.id
AND albumjoin.track = track.id
AND art_track.link0 = artist2.id
AND art_track.link1 = track.id
LIMIT 20;
""",params = {'gid':gid})
    for item in d: item['name']= item['artist_name']
    return d


def getMBIDAlbumTracks(gid):
    d = sw.queryOnce(qc.query("music_dbfile"),"""
SELECT 
   track.gid as track_mbid,
   track.name as track_name,
   album.name as album_name,
   track.number as track_number,
   track.length as track_length
FROM  album, albumjoin, track 
WHERE album.gid = :gid 
AND   albumjoin.album = album.id 
AND   track.id = albumjoin.track
ORDER BY track_number
""",params = {"gid":gid})
    for item in d: item['name']= item['track_name']
    return d
  




def getAllTracks():
    d = sw.queryOnce(qc.query("music_dbfile"),"""
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
