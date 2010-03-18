import os
from datetime import datetime

import logging

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

from scatterbrainz.model.meta import Session
from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.album import Album

log = logging.getLogger(__name__)

def getid3prop(mutagen, prop):
    if prop in mutagen:
        return mutagen[prop][0]
    else:
        return None

class LoadController(BaseController):

    def load(self):

        done = False
        now = datetime.now()
        numFilesSeen = 0
        numBadFiles = 0
        numSketchy = 0
        commitbuffer = []
        albums = {}
        artists = {}
        for dirname, dirnames, filenames in os.walk('scatterbrainz/public/.music/'):
            for filename in filenames:
                try:
                    numFilesSeen = numFilesSeen + 1
                    
                    # get path, size, date
                    fileabspath = os.path.join(dirname,filename)
                    filepath = os.path.join(os.path.relpath(dirname, 'scatterbrainz/public/.music/'), filename)
                    filesize = os.path.getsize(fileabspath)
                    filemtime = datetime.fromtimestamp(os.path.getmtime(fileabspath))
                    
                    ext = os.path.splitext(filename)[-1]
                    if not ext == '.mp3': continue
  
                    # mp3 length, bitrate, etc.
                    mutagen = MP3(fileabspath, ID3=EasyID3)
                    info = mutagen.info
                    mp3bitrate = info.bitrate
                    mp3samplerate = info.sample_rate
                    mp3length = int(round(info.length))
                    if info.sketchy:
                        mp3['sketchy'] = true
                        numSketchy = numSketchy + 1
                        log.warn('sketchy MP3: ' + filename)

                    # id3
                    # keys: ['album', 'date', 'version', 'composer', 'title'
                    #        'genre', 'tracknumber', 'lyricist', 'artist']
                    id3artist = getid3prop(mutagen, 'artist')
                    id3album = getid3prop(mutagen, 'album')
                    id3title = getid3prop(mutagen, 'title')
                    id3tracknum = getid3prop(mutagen, 'tracknumber')
                    id3date = getid3prop(mutagen, 'date')
                    id3composer = getid3prop(mutagen, 'composer')
                    id3genre = getid3prop(mutagen, 'genre')
                    id3lyricist = getid3prop(mutagen, 'lyricist')
                    
                    if not id3artist:
                        artist = None
                    elif id3artist in artists:
                        artist = artists[id3artist]
                    else:
                        artist = Artist(id3artist, now)
                        Session.save(artist)
                        artists[id3artist] = artist
                    
                    if not id3album:
                        album = None
                    elif id3album in albums:
                        album = albums[id3album]
                    else:
                        album = Album(id3album, now)
                        Session.save(album)
                        albums[id3album] = album
                    

                    track = Track(artist=artist,
                                  album=album,
                                  filepath=filepath.decode('utf-8'),
                                  filesize=filesize,
                                  filemtime=filemtime,
                                  mp3bitrate=mp3bitrate,
                                  mp3samplerate=mp3samplerate,
                                  mp3length=mp3length,
                                  id3artist=id3artist,
                                  id3album=id3album,
                                  id3title=id3title,
                                  id3tracknum=id3tracknum,
                                  id3date=id3date,
                                  id3composer=id3composer,
                                  id3genre=id3genre,
                                  id3lyricist=id3lyricist,
                                  added=now)
                    
                    Session.save(track)
                    
                    if numFilesSeen > 5000:
                        done = True
                        break
                
                except (UnicodeError) as e:
                    numBadFiles = numBadFiles + 1
                    log.error('Could not load file "' + filename + '" due to exception: '
                              + e.__class__.__name__ + ': ' + str(e))
            if done:
                break
        Session.commit()

        return """Saw %(numFilesSeen)d tracks, %(numArtists)d artists and %(numAlbums)d albums.
                  %(numBadFiles)d failed, %(numSketchy)d sketchy.""" \
               % {'numFilesSeen':numFilesSeen, 'numBadFiles':numBadFiles,
                  'numArtists': len(artists), 'numAlbums': len(albums),
                  'numSketchy' : numSketchy}
