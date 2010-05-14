from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.album import Album
from scatterbrainz.model.meta import Session
import os
import urllib

def getAllArtists():
    artists = Session.query(Artist)
    return parseLocalArtists(artists)
    
def getMBIDArtistAlbums(mbid):
    artist = Session.query(Artist).filter_by(mbid=mbid)
    try:
        artist_id = artist[0].id;
        albums = Session.query(Album).filter_by(artistid=artist_id);
    except:
        return [];
    return parseLocalAlbums(albums);
def getMBIDArtistTracks(mbid):
    try:
        artistid = Session.query(Artist).filter_by(mbid=mbid)[0].id
        tracks = Session.query(Track).filter_by(artistid = artistid)
    except:
        return [];
    return parseLocalTracks(tracks);
        
def getMBIDArtistMembers(artist):
    return [];


def getAllAlbums():
    albums = Session.query(Album)
    return parseLocalAlbums(albums)

def getMBIDAlbumTracks(mbid):
    try:
        albumid =  Session.query(Album).filter_by(mbid=mbid)[0].id
        tracks = Session.query(Track).filter_by(albumid = albumid)
    except:
        return []
    return parseLocalTracks(tracks);

def getMBIDAlbumMembers(mbid):
    return [];



def getAllTracks():
    pass




def getAllMembers():
    return []

def parseLocalAlbums(albums):
    out = []
    for  a in albums:
        name = a.name
        mbid = a.mbid
        out.append({'name':name,
                    'album_mbid':mbid})
    return out

def parseLocalArtists(artists):
    out = []
    for  a in artists:
        name = a.name
        mbid = a.mbid
        out.append({'name':name,
                    'artist_mbid':mbid})
    return out

def parseLocalTracks(tracks):
    out = []
    namefun = lambda x: x.id3title
    for t in tracks:
        name = namefun(t)
        json = {
            'name':name,
            'url':track_URL_from_id(t.id),
            'track_mbid':t.mbid,
            'track_id':t.id,
            'album_id':t.albumid,
            'artist_id':t.artistid
            }
        out.append(json)
    return out




def track_URL_from_id(id):
    track = Session.query(Track).filter_by(id=id)[0]
    path = os.path.join('.music',track.filepath)
    url = _path_url(path)
    return url

def _path_url( path): 
    return os.path.join('http://localhost:5000',urllib.pathname2url(path))
