import os
import time

import logging

from copy import deepcopy

from couchdb.client import Server, Database

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

import simplejson as sjson

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

db = Database('http://localhost:5984/scatterbrainz')

def utf8(s):
    return s.decode('utf-8')
    
def mp3info(mp3):
    s = "MPEG %s layer %d, %d bps, %s Hz, %.2f seconds" % (
        mp3.version, mp3.layer, mp3.bitrate, mp3.sample_rate,
        mp3.length)
    if mp3.sketchy:
        s += " (sketchy)"
    return s
    
def uniqify(seq, idfun=None):
    # http://www.peterbe.com/plog/uniqifiers-benchmark
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

librarysizemap = \
'''function(doc) {
    if (doc.type == 'Track') {
      emit("size", doc.size);
    }
}'''

librarysizereduce = \
'''function(keys, values) {
    return sum(values);
}'''

allartistsmap = \
'''function(doc) {
    if (doc.type == 'Track') {
        emit(doc['id3']['artist'], 1);
    }
}'''

allartistsreduce = \
'''function(keys, values) {
    return sum(values);
}'''

artistalbummap = \
'''function(doc) {
    if (doc.type == 'Track') {
        emit(doc['id3']['artist'], doc['id3']['album']);
    }
}'''

albumtrackmap = \
'''function(doc) {
    if (doc.type == 'Track') {
        emit(doc['id3']['album'], doc['id3']['title']);
    }
}'''

def create_views(db):
    db['_design/scatterbrainz'] = {'views': {
        'librarysize': {'map': librarysizemap, 'reduce': librarysizereduce},
        'allartists': {'map': allartistsmap, 'reduce': allartistsreduce},
        'artistalbum': {'map': artistalbummap},
        'albumtrack': {'map': albumtrackmap},
    }}

class HelloController(BaseController):

    def load(self):

        server = Server('http://localhost:5984/')
        log.info('established database connection')

        # create a database, if it already exists, delete and recreate it
        try:
            db2 = server.create('scatterbrainz')
            log.info('database created')
        except:
            del server['scatterbrainz']
            db2 = server.create('scatterbrainz')
            log.info('database deleted and created')
        
        create_views(db2)
        
        now = time.time()

        id = 0
        numFiles = 0
        numLoaded = 0
        numInserts = 0
        numBad = 0
        tracks = []
        for dirname, dirnames, filenames in os.walk('/media/data/music/[Funny]'):
            for filename in filenames:

                try:
                
                    numFiles = numFiles + 1
                    idStr = str(id).rjust(10,'0')
                    
                    # get path, size, date
                    reldir = os.path.relpath(dirname, '/media/data/music') \
                                    .strip('/').split('/')
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
                        log.warn('sketchy MP3: ' + filename)
    
                    # id3
                    # keys: ['album', 'date', 'version', 'composer', 'title'
                    #        'genre', 'tracknumber', 'lyricist', 'artist']
                    id3 = {}
                    for key in mutagen:
                        if mutagen[key]:
                            id3[key] = mutagen[key][0]
                    track = {
                        '_id'      : idStr,
                        'type'  : 'Track',
                        'filepath' : map(utf8, reldir),
                        'filename' : utf8(filename),
                        'size'     : size,
                        'added'    : int(round(now)),
                        'mtime'    : int(round(mtime)),
                        'id3'      : id3,
                        'mp3'      : mp3,
                    }
                    tracks.append(track)
                    id = id + 1
                    if len(tracks) == 1000:
                        db2.update(tracks)
                        numInserts = numInserts + 1
                        numLoaded = numLoaded + len(tracks)
                        tracks = []
                
                except Exception as e:
                    
                    numBad = numBad + 1
                    log.error('Could not load file "' + filename + '" due to exception: '
                              + e.__class__.__name__ + ': ' + str(e))

        if tracks:
            db2.update(tracks)
            numInserts = numInserts + 1
            numLoaded = numLoaded + len(tracks)

        return """Saw %(numFiles)d files, loaded %(numLoaded)d in %(numInserts)d inserts, %(numBad)d failed.""" \
               % {'numFiles':numFiles,'numLoaded':numLoaded, 'numInserts':numInserts,
                  'numBad':numBad}

    def index(self):
        tracks = []
        for key in db:
            track = db[key]
            if track.get('type') == 'Track':
                tracks.append(db[key])
        c.tracks = tracks
        return render('/hello.html')
    
    def treebrowse(self):
        id = request.params['id']
        if id == '0':
            return self._allartists()
        else:
            [type, name] = id.split('/',1)
            if type == 'artist':
                return self._albumsforartist(name)
            elif type == 'album':
                return self._tracksforalbum(name)
    
    def _makeJSON(self, results, type, leaf, namefun):
        alljson = []
        for result in results:
            name = namefun(result)
            json = {
                'attributes': {'id' : type + '/' + name}, 
                'data': name
            }
            if not leaf:
                json['state'] = 'closed'
            alljson.append(json)
        return sjson.dumps(alljson)
    
    def _allartists(self):
        results = db.view('scatterbrainz/allartists', group=True)
        namefun = lambda x: x['key']
        return self._makeJSON(results, 'artist', False, namefun)
    
    def _albumsforartist(self, artist):
        results = db.view('scatterbrainz/artistalbum', key=artist)
        namefun = lambda x: x['value']
        results = uniqify(results, idfun=namefun)
        return self._makeJSON(results, 'album', False, namefun)
    
    def _tracksforalbum(self, album):
        results = db.view('scatterbrainz/albumtrack', key=album)
        namefun = lambda x: x['value']
        return self._makeJSON(results, 'track', True, namefun)
