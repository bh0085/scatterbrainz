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
        c.cname = "friends"
        c.cdesc = "a collection of requests to manipulate, broadcast, and augment the 'friends' database"
        c.methods = [{'n':'addknown','d':'adds a seed friend at swiftway'},
                     {'n':'list','d':'list current friends'},
                     {'n':'friendallknown','d':'add currently known server to friends'},
                     {'n':'annoucetoall','d':'::stub::'},
                     {'n':'hearabout','d':'called by a remote serve to announce itself'}
                     ]
        return render('describe_controller.mako')

    def addknown(self):
        fdb = qc.query('friends_dbfile')
        sqw = swrap.sqliteWrapper(fdb)
        sw_address = "94.100.21.250"
        sw_port = "5554"
        sw_pg = "64077"
        
        sqw.query("INSERT OR IGNORE into known(address, pg_port,sb_port) values(:address,:pg_port,:sb_port);",params={'address':sw_address,'pg_port':sw_pg,'sb_port':sw_port}) 
        sqw.commit()
        sqw.close()
        return sjson.dumps("Added the default friend at swiftway")

    def list(self):
        fdb = qc.query('friends_dbfile')
        sqw = swrap.sqliteWrapper(fdb)
        d = sqw.queryToDict("select * from friends;")
        sqw.close()
        return sjson.dumps(d)

    def announcetoall(self):
        return sjson.dumps("report method not yet implemented... reporting nothing")
    def friendAddressesJSON(self):
        sqw = swrap.sqliteWrapper(qc.query('friends_dbfile'))
        knows = sqw.queryToDict("SELECT address, sb_port FROM known, friends WHERE known.id = friends.known")
        sqw.close
        urls = []
        for k in knows:
            urls.append("http://"+k['address']+':'+str(k['sb_port']))
        return sjson.dumps(urls)
    def announcetofriends(self):
        pass
    def friendallknown(self):
        sqw = swrap.sqliteWrapper(qc.query('friends_dbfile'))
        knows = sqw.queryToDict("SELECT id FROM known")
        for k in knows:
            sqw.query("""
INSERT OR IGNORE INTO friends(known) values(:kid);
"""
                      ,params={'kid':k['id']})
        sqw.commit()
        sqw.close()
        return sjson.dumps("friended each known server, Total: "+str(len(knows)))

    def hearabout(self):
        p = request.params;
        address = p['address']
        sb_port = p['sb_port']
        pg_port = p['pg_port']

        sqw = swrap.sqliteWrapper(qc.query('friends_dbfile'))
        sqw.query("""
INSERT OR IGNORE INTO 
known(address,pg_port,sb_port)
values(:address,:pg_port,:sb_port)
"""
                  ,params={'address':address,'sb_port':sb_port,'pg_port':pg_port})
        sqw.commit()
        sqw.close()
