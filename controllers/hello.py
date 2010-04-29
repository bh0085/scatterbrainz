import os
import time

import logging

import simplejson

from sqlalchemy.sql.functions import random
from sqlalchemy.orm import contains_eager

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

from scatterbrainz.external.my_MB import getRelease, searchRelease

log = logging.getLogger(__name__)

from scatterbrainz.model.meta import Session
from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.album import Album

class HelloController(BaseController):
    
    def index(self):
        return render('/hello.html')

    def treeBrowseAJAX(self):
        idStr = request.params['id']
        if idStr == 'init':
            return self._allArtistsTreeJSON()
        else:
            [type, id] = idStr.split('/',1)
            if type == 'Artist':
                return self._albumsForArtistTreeJSON(id)
            elif type == 'Album':
                return self._tracksForAlbumTreeJSON(id)
            else:
                raise Exception('bad type '+type)
    
    def _allArtistsTreeJSON(self):
        artists = Session.query(Artist).join(Album)
        return self._dumpFlatJSON(artists, self._compareTreeFloatVA)
    
    def _albumsForArtistTreeJSON(self, artistid):
        albums = Session.query(Album).join(Artist).filter_by(id=artistid)
        return self._dumpFlatJSON(albums)
    
    def _tracksForAlbumTreeJSON(self, albumid):
        tracks = Session.query(Track).filter_by(albumid=albumid)
        return self._dumpFlatJSON(tracks)
    
    def _dumpFlatJSON(self, results, sortfun=cmp):
        json = map(lambda x: x.toTreeJSON(), results)
        json.sort(sortfun)
        return simplejson.dumps(json)
    
    def getTracksAJAX(self):
        idStr = request.params['id']
        [type, id] = idStr.split('/',1)
        if type == 'Track':
            return self._trackPlaylistJSON(id)
        elif type == 'Artist':
            return self._tracksForArtistPlaylistJSON(id)
        elif type == 'Album':
            return self._tracksForAlbumPlaylistJSON(id)
        else:
            raise Exception('bad type '+type)
    
    def randomTrackAJAX(self):
        track = Session.query(Track).order_by(random())[0]
        return simplejson.dumps([track.toPlaylistJSON()])
    
    def randomAlbumAJAX(self):
        album = Session.query(Album).order_by(random())[0]
        tracks = Session.query(Track) \
                        .filter_by(albumid=album.id)
        json = map(lambda x: x.toPlaylistJSON(), tracks)
        return simplejson.dumps(json)
    
    def _trackPlaylistJSON(self, trackid):
        tracks = Session.query(Track).filter_by(id=trackid)
        return self._playlistJSON(tracks)
    
    def _tracksForAlbumPlaylistJSON(self, albumid):
        tracks = Session.query(Track).filter_by(albumid=albumid)
        return self._playlistJSON(tracks)
    
    def _tracksForArtistPlaylistJSON(self, artistid):
        tracks = Session.query(Track).filter_by(artistid=artistid)
        return self._playlistJSON(tracks)

    def _playlistJSON(self, tracks):
        json = map(lambda x: x.toPlaylistJSON(), tracks)
        return simplejson.dumps(json)
    
    def searchAJAX(self):
        search = request.params['search']
        maxResults = 50
        artists = Session.query(Artist). \
                          filter(Artist.name.like('%'+search+'%')). \
                          join(Album) \
                          [0:maxResults]
        albums = Session.query(Album). \
                         filter(Album.name.like('%'+search+'%')) \
                         [0:maxResults]
        tracks = Session.query(Track). \
                         filter(Track.id3title.like('%'+search+'%')) \
                         [0:maxResults]
        if len(artists) == maxResults or len(tracks) == maxResults or len(albums) == maxResults:
            truncated = True
        else:
            truncated = False
        artistIdToJSON = {}
        albumsIdToJSON = {}
        for artist in artists:
            if artist.id not in artistIdToJSON:
                artistJSON = artist.toTreeJSON()
                artistIdToJSON[artist.id] = artistJSON
        for album in albums:
            if album.artist and album.artist.id not in artistIdToJSON:
                artistJSON = album.artist.toTreeJSON(children=[])
                artistIdToJSON[album.artist.id] = artistJSON
                albumJSON = album.toTreeJSON()
                artistJSON['children'].append(albumJSON)
            else:
                continue
        for track in tracks:
            if track.album and \
               track.album.artist and \
               track.album.artist.id not in artistIdToJSON:
                artistJSON = track.album.artist.toTreeJSON(children=[])
                artistIdToJSON[track.album.artist.id] = artistJSON
            else:
                continue
            if track.album and track.album.id not in albumsIdToJSON:
                albumJSON = track.album.toTreeJSON(children=[])
                artistJSON['children'].append(albumJSON)
                albumsIdToJSON[track.album.id] = albumJSON
            else:
                continue
            albumJSON['children'].append(track.toTreeJSON())
        json = artistIdToJSON.values()
        json.sort(self._compareTreeFloatVA)
        return simplejson.dumps(json)

    def _compareTreeFloatVA(self, a,b):
        if a['data'] == 'Various Artists':
            return -1
        elif b['data'] == 'Various Artists':
            return 1
        else:
            return cmp(a['data'], b['data'])
    
    def getPlayingTrackInfoAJAX(self):
        trackid = request.params['trackid'].split('_')[1]
        track = Session.query(Track).filter_by(id=trackid).one()
        albumArtURL = None
        (artistName, albumName, trackName) = (track.id3artist, track.id3album, track.id3title)
        if track.album and track.album and track.album.artist:
            album = track.album
            artist = album.artist
            release = None
            if album.albumArtURL:
                albumArtURL = album.albumArtURL
            elif album.mbid:
                release = getRelease(album.mbid)
            else:
                if artist.name == 'Various Artists':
                    release = searchRelease(None, album.name)
                else:
                    release = searchRelease(artist.name, album.name)
                if release and not album.mbid:
                    album.mbid = release.id.split('/')[-1]
                if release and not artist.mbid:
                    artist.mbid = release.artist.id.split('/')[-1]
            if release:
                artistName = release.artist.name
                albumName = release.title
                if not albumArtURL:
                    asin = release.getAsin()
                    if asin:
                        albumArtURL = 'http://ecx.images-amazon.com/images/P/%s.jpg' % (asin)
                        album.albumArtURL = albumArtURL
            Session.commit()
        json = {}
        if albumArtURL:
            json['albumArtURL'] = albumArtURL
        json['artist'] = artistName
        json['album'] = albumName
        json['track'] = trackName
        return simplejson.dumps(json)
