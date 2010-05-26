import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/auth.mako')
        # or, return a response
        return 'Hello World'
    @authorize(RemoteUser())
    def private(self):
        return "You are authenticated!"

