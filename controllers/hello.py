import os
import time

import logging

import couchdb

from couchdb.client import Server, Database
from couchdb.schema import Document, TextField

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

class Track(Document):
   dirname = TextField()
   filename = TextField()

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

        numFiles = 0
        numLoaded = 0
        numInserts = 0
        numBad = 0
        tracks = []
        for dirname, dirnames, filenames in os.walk('/media/data/music/Bob Dylan'):
            for filename in filenames:
                numFiles = numFiles + 1
                id = str(numLoaded).rjust(10,'0')
                reldir = os.path.relpath(dirname, '/media/data/music')
                try:
                    tracks.append(Track(id=id, dirname=reldir, filename=filename))
                    numLoaded = numLoaded + 1
                except UnicodeDecodeError:
                    log.info('UnicodeDecodeError  '+reldir+' '+filename)
                    numBad = numBad + 1
                if numLoaded % 1000 == 0:
                    db.update(tracks)
                    numInserts = numInserts + 1
                    tracks = []
        if tracks:
            db.update(tracks)
            numInserts = numInserts + 1

        return """Saw %(numFiles)d files, loaded %(numLoaded)d in %(numInserts)d inserts, %(numBad)d failed
                  due to encoding problems.""" \
               % {'numFiles':numFiles,'numLoaded':numLoaded, 'numInserts':numInserts, \
                  'numBad':numBad}

    def index(self):
        db = couchdb.client.Database('http://localhost:5984/scatterbrainz')
        tracks = []
        for id in db:
            tracks.append(Track.load(db, id))
        c.tracks = tracks
        return render('/hello.html')

