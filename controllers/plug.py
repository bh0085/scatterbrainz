import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render
from mako.template import Template as t

log = logging.getLogger(__name__)

import sb_helpers as sh
import simplejson as sjson

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn


class PlugController(BaseController):

    @authorize(RemoteUser())
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

    def serveMako(self,name):
        c.username  = sh.unameFromCookie(request.cookies['authkit'])
        return render(name+'.mako')
        
    def what(self):
        jsfiles = ['jquery']
        rendered0 = sh.sourced_js(jsfiles,True)
        c.jsfiles = rendered0
        c.whatUser = 'bh0085'
        c.albumnames = []
        c.artistnames = []

        uname = sh.unameFromCookie(request.cookies['authkit'])

        import dbs.requests.request as r
        params = {'action':'getArtists'}
        c.artistnames = r.requestWithParams(uname,'what',params,True)
        params = {'action':'getAlbums'}
        c.albumnames = r.requestWithParams(uname,'what',params,True)               


        return self.serveMako('what')
