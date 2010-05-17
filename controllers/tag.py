import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

from tagger import tagger

log = logging.getLogger(__name__)

class TagController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/tag.mako')
        # or, return a response
        return 'Hello World'

    def tag(self):
        tagger.tagDir()
        return 'tagging successful!'
