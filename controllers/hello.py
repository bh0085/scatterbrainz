import os
import time

import logging

from couchdb.client import Server, Database

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

def getFullPath(track):
    return '/'.join(track['filepath']) + '/' + track['filename']

def utf8(s):
    return s.decode('utf-8')

def mp3info(mp3):
    s = "MPEG %s layer %d, %d bps, %s Hz, %.2f seconds" % (
        mp3.version, mp3.layer, mp3.bitrate, mp3.sample_rate,
        mp3.length)
    if mp3.sketchy:
        s += " (sketchy)"
    return s

def minsec(sec):
    return "%d:%02d" % (sec / 60, sec % 60)

def kbps(bps):
    return bps / 1000

def tracknum(trackstr):
    return int(trackstr.split('/')[0])

class HelloController(BaseController):

    def load(self):

        server = Server('http://localhost:5984/')
        log.info('established database connection')

        # create a database, if it already exists, delete and recreate it
        try:
            db = server.create('scatterbrainz')
            log.info('database created')
        except:
            del server['scatterbrainz']
            db = server.create('scatterbrainz')
            log.info('database deleted and created')
        
        now = time.time()

        id = 0
        numFiles = 0
        numLoaded = 0
        numInserts = 0
        numBad = 0
        tracks = []
        for dirname, dirnames, filenames in os.walk('/media/data/music/Joanna Newsom'):
            for filename in filenames:
                numFiles = numFiles + 1
                idStr = str(id).rjust(10,'0')
                
                # get path, size, date
                reldir = os.path.relpath(dirname, '/media/data/music').strip('/').split('/')
                filepath = os.path.join(dirname,filename)
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                
                # mp3 length, bitrate, etc.
                mutagen = MP3(filepath, ID3=EasyID3)
                info = mutagen.info
                mp3 = {
                    'version'    : info.version,
                    'layer'      : info.layer,
                    'bitrate'    : info.bitrate,
                    'samplerate' : info.sample_rate,
                    'length'     : info.length,
                }
                if info.sketchy:
                    mp3['sketchy'] = true

                # id3
                id3 = {}
                # keys: ['album', 'date', 'version', 'composer', 'title'
                #        'genre', 'tracknumber', 'lyricist', 'artist']
                for key in mutagen:
                    id3[key] = mutagen[key][0]
                
                try:
                    track = {
                        '_id'      : idStr,
                        'doctype'  : 'Track',
                        'filepath' : map(utf8, reldir),
                        'filename' : utf8(filename),
                        'size'     : size,
                        'added'    : round(now),
                        'mtime'    : round(mtime),
                        'id3'      : id3,
                        'mp3'      : mp3,
                    }
                    tracks.append(track)
                    id = id + 1
                except UnicodeDecodeError:
                    numBad = numBad + 1
                if len(tracks) == 1000:
                    db.update(tracks)
                    numInserts = numInserts + 1
                    numLoaded = numLoaded + len(tracks)
                    tracks = []
        if tracks:
            db.update(tracks)
            numInserts = numInserts + 1
            numLoaded = numLoaded + len(tracks)

        return """Saw %(numFiles)d files, loaded %(numLoaded)d in %(numInserts)d inserts, %(numBad)d failed
              due to encoding problems.""" \
               % {'numFiles':numFiles,'numLoaded':numLoaded, 'numInserts':numInserts, \
                  'numBad':numBad}

    def index(self):
        db = Database('http://localhost:5984/scatterbrainz')
        tracks = []
        for key in db:
            tracks.append(db[key])
        c.tracks = tracks
        c.getFullPath = getFullPath
        c.minsec = minsec
        c.kbps = kbps
        c.tracknum = tracknum
        return render('/hello.html')

