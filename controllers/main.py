import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

log = logging.getLogger(__name__)

class MainController(BaseController):

    def index(self):
        c.all_controllers=['/music',
                           '/friends',
                           '/init']
        return render('main_index.mako')
