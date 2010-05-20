import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

import urllib2

import dbs.config.queryConfig as qc
import sqliteWrapper as swrap
import simplejson as sjson
import dbs.music.fetchMusic as fm

import re
def toHTML(str_in):
    r = re.compile("\n",re.M)
    html_out = re.sub(r,"<br/>",str_in)
    print html_out
    return html_out

class QueriesController(BaseController):
    def index(self):
        c.cname = "queries"
        c.cdesc = "a collection of prepacked queries that will return json"
        c.methods = [{'n':'getFriends','d':'add tracks living in the music directory.'},
                     {'n':'getLocalMusic','d':'A list of tracks on this computer.'},
                     {'n':'getFriendsMusic','d':'A list of tracks on friends computers.'}
                     ]
        return render('describe_controller.mako')

    
    def getFriends(self):
        sqw = swrap.sqliteWrapper(qc.query('friends_dbfile'))
        d = sqw.queryToDict("select address, sb_port, pg_port from friends")
        sqw.close()
        return sjson.dumps(d)

    #returns sjson for all music in friends' networks.
    def getFriendsMusic(self):
        friends = self.getFriends()
        queries = []
        for f in friends:
            address = "http://"+f['address']+":"+str(f['sb_port'])
            q = address+"/queries/getLocalMusicJSON"
            o = urllib2.build_opener()
            d = sjson.loads(o.open(q).read())
            queries.append(d)       
        data = {}
        data['nq'] = len(queries)
        data['query0'] = queries[0][0]
        return sjson.dumps(data)
    def getLocalMusic(self):
        fetched = fm.getAllArtists()
        return sjson.dumps(fetched)
    
