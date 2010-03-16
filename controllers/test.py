from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from scatterbrainz.lib.base import BaseController, render

from scatterbrainz.model.meta import Session
from scatterbrainz.model.track import Track

class TestController(BaseController):
    
    def index(self):
        t = Track('asdf')
        Session.save(t)
        Session.commit()
