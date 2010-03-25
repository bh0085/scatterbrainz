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

from scatterbrainz.external import getMB

log = logging.getLogger(__name__)

class GetlocalController(BaseController):

    def blah(self):
        return "HELLO"

    def alltracks(self):
        tracks = Session.query(Track)
        namefun = lambda x: x.id3title
        out = []
        for t in tracks:
            name = namefun(t)
            type = t.__class__.__name__
            json = {
                'type':type,
                'name':name,
                'url':self.track_URL_from_id(t.id),
                'id':t.id,
                'albumid':t.albumid,
                'artistid':t.artistid
                    }
            out.append(json)
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
        results = getMB.getAlbumsByArtist(mbid)
        out = []
        for r in results:
            json={
                'id':  r.id,
                'name':r.title 
                }
            out.append(json)

        return sjson.dumps(out)

    def trackRelationsMB(self):
        print "WHATTHSODIHJG"
        trackid=request.params['trackid']
        mbid=Session.query(Track).filter_by(id=trackid)[0].mbtrackid
        artist_mbid=Session.query(Track).filter_by(id=trackid)[0].mbartistid
        release_mbid=Session.query(Track).filter_by(id=trackid)[0].mbalbumid

        results = getMB.getTrackRelations(mbid) 
        out = {}
        tresults = []
        for r in results:
            json = {
                'type':r.getType()
                }
            tresults.append(json);
        out['track_relations'] =tresults

        results =  getMB.getArtistRelations(artist_mbid) 
        artist_relations=[]
        for r in results:
            json = {
                'type':r.getType()
                }
            artist_relations.append(json);
        out['artist_relations'] =artist_relations

        results =  getMB.getReleaseRelations(release_mbid) 
        album_relations=[]
        for r in results:
            json = {
                'type':r.getType()
                }
            album_relations.append(json);
        out['album_relations'] =album_relations

        print out
        return sjson.dumps(out);

    def track_URL_from_id(self,id):
        track = Session.query(Track).filter_by(id=id)[0]
        path = os.path.join('.music',track.filepath)
        url = self._path_url(path)
        return url

    def _path_url(self, path):         
        return os.path.join('http://localhost:5000',urllib.pathname2url(path))
        

    

