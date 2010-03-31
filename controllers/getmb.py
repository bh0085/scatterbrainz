import logging

from scatterbrainz.model.track import Track
from scatterbrainz.model.artist import Artist
from scatterbrainz.model.album import Album
from scatterbrainz.model.meta import Session
from scatterbrainz.model.rdf import RDFTriple

import simplejson as sjson
from rdflib.Graph import Graph
from scatterbrainz.external.sparql.my_rdf import getURILabel

import scatterbrainz.external.sparql.sparqlDBs as sDB

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

import re

log = logging.getLogger(__name__)

class GetmbController(BaseController):

    def currentMembersForTrackArtist(self):
        trackid = request.params['trackid']
        track = Session.query(Track).filter_by(id=trackid).one()
        
        #search for triples with subject matching current artist
        db_uri=u""
        for triple in Session.query(RDFTriple).filter_by(artistid=track.artistid):
            if triple.subject==":artist":
                if triple.predicate=="hasdbpedia":
                    db_uri = triple.obj
                    
        if db_uri =="":
            art_mbid = track.artist.mbid
            db_uri = sDB.dbpedia_from_MBID(art_mbid)
            db_unicode = unicode(db_uri.__str__())
            artist = track.artist
            triple = RDFTriple(subject=u":artist",
                               predicate=u"hasdbpedia",
                               obj=db_unicode,
                               artist=artist,
                               track=None,
                               album=None)   
            Session.save(triple)
            Session.commit()

        g = Graph()
        g.parse(db_uri)
        pmem_re = re.compile("pastmember",re.I)
        cmem_re = re.compile("currentmember",re.I)

        out={}
        past_members = []
        current_members = []

        for s,p,o in g.triples((None,None,None)):
            if re.search(pmem_re,p):
                past_members.append(getURILabel(o))
            if re.search(cmem_re,p):
                current_members.append(getURILabel(o))
                
        out['past_members'] = past_members
        out['current_members'] = current_members
        return sjson.dumps(out)
