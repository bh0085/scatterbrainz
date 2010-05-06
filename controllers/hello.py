import os
import re
import time
import urllib
import simplejson
import htmlentitydefs

from datetime import datetime, timedelta

import logging

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

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

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

    def getAlbumArtAJAX(self):
        trackid = request.params['trackid'].split('_')[1]
        track = Session.query(Track).filter_by(id=trackid).one()
        if not track.album.albumArtFilename and ( \
            track.album.lastHitAlbumArtExchange is None \
            or datetime.now() > track.album.lastHitAlbumArtExchange + timedelta(days=10)):
            
            track.album.lastHitAlbumArtExchange = datetime.now()
            
            album = track.album.name
            artist = track.artist.name
            q = artist + ' ' + album

            site = 'http://www.albumartexchange.com'

            params = {
                'grid' : '2x7',
                'sort' : 7,
                'q'    : q,
            }

            url = site + '/covers.php?%s' % urllib.urlencode(params)
            
            html = urllib.urlopen(url).read()
            
            search = re.search('src="/phputil/scale_image.php\?size=150&amp;src=(?P<src>.*?)"',html)
            
            if search:
                image = site + urllib.unquote(search.group('src'))
                extension = image.rsplit('.', 1)[1]
                delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
                delchars = delchars.translate(None," ()'&!-+_.")
                filename = (artist + ' - ' + album).encode('utf-8').translate(None, delchars) + '.' + extension
                urllib.urlretrieve(image, 'scatterbrainz/public/art/' + filename)
                albumArt = '/art/' + filename
                track.album.albumArtFilename = albumArt
            Session.begin()
            Session.commit()
        json = {}
        if track.album.albumArtFilename:
            json['albumArtURL'] = track.album.albumArtFilename
        return simplejson.dumps(json)

    def getLyricsAJAX(self):
        trackid = request.params['trackid'].split('_')[1]
        track = Session.query(Track).filter_by(id=trackid).one()
        if not track.lyrics and \
           (track.lastHitLyricWiki is None or \
            datetime.now() > track.lastHitLyricWiki + timedelta(days=10)):
            
            track.lastHitLyricWiki = datetime.now()
            
            title = track.id3title
            artist = track.id3artist
            params = {
                'artist' : artist,
                'song'   : title,
                'fmt'    : 'json',
            }
            
            url = 'http://lyrics.wikia.com/api.php?%s' % urllib.urlencode(params)
            
            html = urllib.urlopen(url).read()
            
            if not "'lyrics':'Not found'" in html:
                search = re.search("'url':'(?P<url>.*?)'",html)
                lyricurl = urllib.unquote(search.group('url'))
                lyrichtml = urllib.urlopen(lyricurl).read()
                lyrics = re.search("<div class='lyricbox'>.*?</div>(?P<lyrics>.*?)<!-- \n", lyrichtml).group('lyrics')
                lyrics = unescape(lyrics)
                track.lyrics = lyrics
            Session.begin()
            Session.commit()
        json = {}
        if track.lyrics:
            json['lyrics'] = track.lyrics
        return simplejson.dumps(json)
    
    def getTrackInfoAJAX(self):
        trackid = request.params['trackid'].split('_')[1]
        track = Session.query(Track).filter_by(id=trackid).one()
        (artistName, albumName, trackName) = (track.id3artist, track.id3album, track.id3title)
        if (not track.artist.mbid or not track.album.mbid or not track.album.asin) and \
           (track.album.lastHitMusicbrainz is None \
             or datetime.now() > track.album.lastHitMusicbrainz + timedelta(days=10)):

            track.album.lastHitMusicbrainz = datetime.now()
            
            album = track.album
            artist = album.artist
            release = None
            if album.mbid:
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
                albumName = release.title
                asin = release.getAsin()
                if asin:
                    track.album.asin = asin
                if release.artist:
                    artistName = release.artist.name
            Session.begin()
            Session.commit()
        json = {}
        json['artist'] = artistName
        json['album'] = albumName
        json['track'] = trackName
        if track.album.asin:
            json['asin'] = track.album.asin
        return simplejson.dumps(json)
