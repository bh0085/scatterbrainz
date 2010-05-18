import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from scatterbrainz.lib.base import BaseController, render

import os
from mutagen.mp3 import MP3
import dbs.config.queryConfig as qc
import sqliteWrapper as swrap


log = logging.getLogger(__name__)

class Load2Controller(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/load2.mako')
        # or, return a response
        return 'Hello World'

    def addtracks(self):
        sb_dir = qc.query('scatterbrainz_dir')
        music_dir = qc.query('music_dir')
        tracks_dir = os.path.join(music_dir,'tracks')
        dbfile = qc.query('music_dbfile')
        sqw = swrap.sqliteWrapper(dbfile)
      
        gidlist = []
        if not os.path.isdir(tracks_dir): os.mkdir(tracks_dir)
        for (base, dirs, files) in os.walk(music_dir,followlinks = True):
            for f in files:
                ext = os.path.splitext(f)[-1]
                if ext == '.mp3':
                    f_abs = os.path.join(base,f)
                    mutagen = MP3(f_abs)

                    ##for some reason that nobody will probably ever
                    ##understand, this does not work with EasyID3
                    tkey = u'TXXX:MusicBrainz Track Id'
                    if tkey in mutagen.tags.keys():
                        gid =mutagen[tkey].text[0]

                        link = os.path.join(tracks_dir,gid)
                        if not gid in gidlist: gidlist.append(gid)
                        if not os.path.isfile(link):
                            os.link(f_abs,link)
                    else:
                        print 'no musicbrainz id for' + f_abs
    
        for gid in gidlist:
            sqw.query("""INSERT OR REPLACE INTO track(gid) values('"""+gid+"""');""")
        sqw.commit()
        n = len(gidlist)
        return 'moved '+str(n)+' tracks to '+tracks_dir+' , indexed in '+dbfile


    def addextra(self):
        pass
        
