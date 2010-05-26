import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

import sb_helpers as sh

class DbcacheRequestController(BaseController):

    @authorize(RemoteUser())
    def index(self):
        p = request.params()
        k = p['key']
        uname = sh.unameFromCookie(request.cookies['authkit'])

        print k

        # Return a rendered template
        #return render('/dbcache_request.mako')
        # or, return a response
        return 'authorization worked ok'
