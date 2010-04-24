import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from sqlalchemy.orm import join
import re
from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.album import Album
from scatterbrainz.model.meta import Session
import urllib
from scatterbrainz.lib.base import BaseController, render
import os
import simplejson as sjson

from scatterbrainz.external import my_MB

log = logging.getLogger(__name__)

class GetlocalController(BaseController):

    def blah(self):
        return "HELLO"

    def alltracks(self):
        tracks = Session.query(Track)
        count = 0
        namefun = lambda x: x.id3title
        out = []
        this_artist_count = 0 
        last_artist = ''
        max_per_artist = 5
        for t in tracks:
            name = namefun(t)
            type = t.__class__.__name__

            this_artist = t.artistid
            if this_artist == last_artist:
                this_artist_count = this_artist_count + 1
            else:
                this_artist_count = 0
                last_artist = this_artist
            if this_artist_count < max_per_artist:
                json = {
                    'type':type,
                    'name':name,
                    'url':self.track_URL_from_id(t.id),
                    'id':t.id,
                    'albumid':t.albumid,
                    'artistid':t.artistid
                    }
                out.append(json)
                count = count + 1
                if count > 50: break

        return sjson.dumps(out)
    
    def trackArtistAlbumsLOCAL(self):
        trackid = request.params['trackid']

        #note that we can do this because there is 
        #only a single foreign key matched between 
        #tracks and albums.
        artistid=Session.query(Track).filter_by(id=trackid)[0].artistid
        joined=Session.query(Track).filter_by(artistid=artistid)

        aids = []
        out = []
        for t in joined:
            aid = t.albumid
            if not aid in aids:
                aids.append(aid)
                year_re = re.compile('[0-9]{4}')
                early_year = (re.search(year_re,t.id3date)).group()
                json = {
                    'aid':aid,
                    'mbid':t.mbalbumid,
                    'name':Session.query(Album).filter_by(id=aid)[0].name,   
                    'year':early_year
                    }
                out.append(json)
        return sjson.dumps(out)
    
    def trackArtistAlbumsMB(self):
        trackid = request.params['trackid']

        mbid=Session.query(Track).filter_by(id=trackid)[0].mbartistid
        results = my_MB.getAlbumsByArtist(mbid)
        out = []
        for r in results:
            json={
                'id':  r.id,
                'name':r.title 
                }
            out.append(json)

        return sjson.dumps(out)

    def trackRelationsMB(self):
        trackid=request.params['trackid']
        mbid=Session.query(Track).filter_by(id=trackid)[0].mbtrackid
        artist_mbid=Session.query(Track).filter_by(id=trackid)[0].mbartistid
        release_mbid=Session.query(Track).filter_by(id=trackid)[0].mbalbumid

        results = my_MB.getTrackRelations(mbid) 
        out = {}
        tresults = []
        for r in results:
            json = {
                'type':r.getType()
                }
            tresults.append(json);
        out['track_relations'] =tresults

        results =  my_MB.getArtistRelations(artist_mbid) 
        artist_relations=[]
        for r in results:
            json = {
                'type':r.getType()
                }
            artist_relations.append(json);
        out['artist_relations'] =artist_relations

        results =  my_MB.getReleaseRelations(release_mbid) 
        album_relations=[]
        for r in results:
            json = {
                'type':r.getType()
                }
            album_relations.append(json);
        out['album_relations'] =album_relations

        return sjson.dumps(out);

    def track_URL_from_id(self,id):
        track = Session.query(Track).filter_by(id=id)[0]
        path = os.path.join('.music',track.filepath)
        url = self._path_url(path)
        return url

    def _path_url(self, path):         
        return os.path.join('http://localhost:5000',urllib.pathname2url(path))
        

    

