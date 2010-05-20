import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

import os
import sqliteWrapper as swrap
import dbs.config.queryConfig as qc
from mutagen.mp3 import MP3
import simplejson as sjson
import mbrainzWrapper as mbwrap

class MusicController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/music.mako')
        # or, return a response
        return 'Hello World'
    def addtracks(self):
        sb_dir = qc.query('scatterbrainz_dir')
        music_lib = qc.query('music_lib')
        tracks_dir = os.path.join(music_lib,'tracks')
        dbfile = qc.query('music_dbfile')
        sqw = swrap.sqliteWrapper(dbfile)
      
        gidlist = []
        if not os.path.isdir(tracks_dir): os.mkdir(tracks_dir)
        for (base, dirs, files) in os.walk(music_lib,followlinks = True):
            for f in files:
                ext = os.path.splitext(f)[-1]
                if ext == '.mp3':
                    f_abs = os.path.join(base,f)
                    mutagen = MP3(f_abs)

                    ##for some reason that nobody will probably ever
                    ##understand, this does not work with EasyID3
                    tkey = u'TXXX:MusicBrainz Track Id'
                    if tkey in mutagen.tags.keys():
                        gid =mutagen[tkey].text[0]

                        link = os.path.join(tracks_dir,gid)
                        if not gid in gidlist: gidlist.append(gid)
                        if not os.path.isfile(link):
                            os.link(f_abs,link)
                    else:
                        print 'no musicbrainz id for' + f_abs
    
        for gid in gidlist:
            sqw.query("""INSERT OR IGNORE INTO tracklist(gid) values('"""+gid+"""');""")
        sqw.commit()
        sqw.close()
        n = len(gidlist)
        return sjson.dumps('moved '+str(n)+' tracks to '+tracks_dir+' , indexed in '+dbfile)
    def addmeta(self):
        mdb = swrap.sqliteWrapper(qc.query('music_dbfile'))
        tracks = mdb.queryToDict("""
SELECT gid, id from tracklist
""")
        mbw = mbwrap.mbrainzWrapper()
        #meta fields:
        #list, gid, name, number, length, album, artist
        out =[]
        for t in tracks:


#METADATA GATHERING LOOP!

            d = mbw.queryToDict("""
SELECT 
 track.name as track_name,
 track.length as track_length,
 albumjoin.sequence as track_number,
 artist.name as artist_name,
 album.name as album_name,
 artist.gid as artist_gid,
 album.gid as album_gid
FROM
 album, artist, track, albumjoin
WHERE
 track.artist=artist.id AND
 albumjoin.track=track.id AND
 albumjoin.album=album.id AND
 track.gid= %(track_gid)s
LIMIT 1;
"""
                                , params={'track_gid':t['gid']} )
            r = d[0]
            mdb.query('INSERT OR IGNORE INTO artist(name,gid) values( :artist_name, :artist_gid);'
                      ,params = {'artist_name':r['artist_name'],
                                 'artist_gid':r['artist_gid']})
            mdb.query('INSERT OR IGNORE INTO album(name,gid) values( :album_name, :album_gid);'
                      ,params = {'album_name':r['album_name'],
                                 'album_gid':r['album_gid']})

            album_id = mdb.queryToDict('SELECT id FROM album WHERE gid = :album_gid',params = {'album_gid':r['album_gid']})[0]['id']
            artist_id = mdb.queryToDict('SELECT id FROM artist WHERE gid = :artist_gid',params = {'artist_gid':r['artist_gid']})[0]['id']

            mdb.query("""
INSERT OR IGNORE INTO 
 track(listing, gid, name, number, length, album, artist) 
 values(:track_id, :track_gid,:track_name, :track_number, :track_length, :album_id, :artist_id)"""
                      ,params={'album_id':album_id,
                                'artist_id':artist_id,
                                'track_number':r['track_number'],
                                'track_length':r['track_length'],
                                'track_name':r['track_name'],
                                'track_gid':t['gid'],
                                'track_id':t['id']})
                      
            
            mdb.query("""
INSERT OR IGNORE INTO 
albumjoin(track, album, artist)
values(:track_id, :album_id, :artist_id)
""",
                      params = {'album_id':album_id,
                                'artist_id':artist_id,
                                'track_id':t['id']})
            
        mdb.commit()
        d = mdb.queryToDict("SELECT name FROM artist")
        mdb.close()
        mbw.close()
        strout = ''
        for i in d:
            strout = strout + i['name']
        return sjson.dumps(strout)
