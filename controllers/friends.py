import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

import dbs.config.queryConfig as qc
import sqliteWrapper as swrap
import simplejson as sjson

class FriendsController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/friends.mako')
        # or, return a response
        return 'Hello World'

    def addfriend(self):
        fdb = qc.query('friends_dbfile')
        sqw = swrap.sqliteWrapper(fdb)
        
        sqw.query("INSERT into friends(address, pg_port,sb_port) values('localhost','5432','5000');") 
        sqw.commit()

        sqw.close()
        return "added no friends"

    def list(self):
        fdb = qc.query('friends_dbfile')
        sqw = swrap.sqliteWrapper(fdb)
        d = sqw.queryToDict("select * from friends;")
        sqw.close()
        return sjson.dumps(d)
        
