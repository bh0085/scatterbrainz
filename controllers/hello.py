import os
import time

import logging

from couchdb.client import Server, Database

from mutagen.easyid3 import EasyID3

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

def getFullPath(track):
    return '/' + '/'.join(track['filepath']) + '/' + track['filename']

def utf8(s):
    return s.decode('utf-8')

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
        for dirname, dirnames, filenames in os.walk('/media/data/music/Bob Dylan'):
            for filename in filenames:
                numFiles = numFiles + 1
                idStr = str(id).rjust(10,'0')
                
                # get path, size, date
                reldir = os.path.relpath(dirname, '/media/data/music').strip('/').split('/')
                filepath = os.path.join(dirname,filename)
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                
                # id3
                id3dumb = EasyID3(filepath)
                id3 = {}
                for key in id3dumb:
                    id3[key] = id3dumb[key][0]
                
                try:
                    track = {
                             '_id'      : idStr,
                             'doctype'  : 'Track',
                             'filepath' : map(utf8, reldir),
                             'filename' : utf8(filename),
                             'size'     : size,
                             'added'    : round(now),
                             'mtime'    : round(mtime),
                             'id3'      : id3
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
        return render('/hello.html')

