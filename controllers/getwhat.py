import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

class GetwhatController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/getwhat.mako')
        # or, return a response
        return 'Hello World'
