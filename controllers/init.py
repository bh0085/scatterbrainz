import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render


log = logging.getLogger(__name__)
from dbs.config import queryConfig as qc
import sb_helpers as shelp
class InitController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/init.mako')
        # or, return a response
        #qc.autoset('sb_address')
        c.sb_address=qc.query('sb_address')
        c.sb_port=qc.query('sb_port')
        return render('init_index.mako')

    def all(self):
        c.urls=['/music/addtracks',
                '/music/addmeta',
                '/friends/addknown',
                '/friends/friendallknown']
        return render('init_all.mako')
