import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render
from mako.template import Template as t

log = logging.getLogger(__name__)

import sb_helpers as sh
import simplejson as sjson

class PlugController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/plug.mako')
        # or, return a responsels t
        
        w = sh.wrap('config')
        d = w.queryToDict('select plugin.name  as name, user.name as uname from plugin, user where user.id = plugin.user;')
        
        print d

        c.pluglist =map(lambda x : str(x['name']),d)
        c.plugnames =map(lambda x : str(x['uname']),d)
        c.cname = 'plug'
        c.cdesc = 'Plugin html interface'
        c.methods = [{'n':'blank','d':'none yet'}]
        jsfiles = ['jquery']
        rendered0 = sh.sourced_js(jsfiles,True)
        rendered = rendered0 + render('/plug_list.mako')
        rendered = rendered + render('/describe_controller.mako')
        return rendered

