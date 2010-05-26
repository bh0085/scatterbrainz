import MultipartPostHandler, urllib2, cookielib
import urllib
import sqliteWrapper as sqw
import sb_helpers as sh
import dbs.config.pluginConfig as cfg
import dbs.config.prefs as prefs
import os
import re
import pickle
import what.parsers as parsers
import what.db as wdb
class soup():
    def __init__(self,plug):
        self._plug = plug
        self._s = self.wrap()

    def s(self):
        return self._s

    def wrap(self):
        from sqlalchemy.ext.sqlsoup import SqlSoup
        "A wrapper for a user's what db, at 'what_$user.sqlite'"
        dbfile = prefs.readPref('what_dbfile',self._plug.User())
        dbstr = 'sqlite:///'+dbfile
        print "Wrapping soup with dbfile: " + dbstr
        db = SqlSoup(dbstr)
        return db
    def commit(self):
        from sqlalchemy.exc import OperationError
        #:
        self.s().flush()
        #except OperationalError:
        #    raise Exception("sqlalchemy threw an exception on flush.... you're in trouble...")
        
        
    

class whatOpener():
    def __init__(self,uname, pw):
        self._opener = None
        self.uname = uname;
        self.pw = pw;
    def opener(self):
        if self._opener == None:
            self.reload()

        return self._opener

    def reload(self):
        o = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        self._opener = o
        
        
    def requestCookies(self):
        o = self.opener()
        for h in o.handlers:
            if h.__class__ == urllib2.HTTPCookieProcessor:
                h.cookiejar.clear()
                
        p = urllib.urlencode( { 'username' : self.uname,'password':self.pw })
        f = o.open( u'http://what.cd/login.php',  p )    
        f.close()
        print "Requesting new cookies from what.cd"

    def getCookies(self):
        o = self.opener()
        cookies = []
        for h in o.handlers:
            if h.__class__ == urllib2.HTTPCookieProcessor:
                cookies = list(h.cookiejar)
        return cookies

    def setCookies(self, cookies):
        o = self.opener()
        for h in o.handlers:
            if h.__class__ == urllib2.HTTPCookieProcessor:
                cj = h.cookiejar
                cj.clear
                for c in cookies:
                    cj.set_cookie(c)
                

class whatPlug():
    def __init__(self, user):
        self.user = user

        #query user preferences.
        self._whatuser = prefs.readPref('what_user',user)
        self._whatpass = prefs.readPref('what_pass',user)


        #query plugin config.
        db = self.wrap()
        self._dbfile = db.config.filter_by(name = 'db_file').first().value
        self._htmlpath =db.config.filter_by( name = 'db_filepath').first().value
        self._path = db.config.filter_by(name = 'db_path').first().value
        self._whatcookiepath = os.path.join(self.whatPath(),self.user+'.cookie')


    def cookiesToFile(self,cookies):
        cookiefile = open(self.whatCookieFile(),'w')
        pickle.dump(cookies,cookiefile)
        cookiefile.close()
        print "Saved cookies to: "  + str(cookiefile)
    
    def cookiesFromFile(self):
        cookiefile = open(self.whatCookieFile())
        cookies = pickle.load(cookiefile)
        cookiefile.close()        
        return cookies

    def User(self):
        return self.user
    def whatHTMLPath(self):
        return self._htmlpath
    def whatPath(self):
        return self._path    
    def whatUser(self):
        return self._whatuser
    def whatPass(self):
        return self._whatpass
    def whatCookieFile(self):
        return self._whatcookiepath
    def whatDBFile(self):
        return self._dbfile


    def refreshCookies(self):
        w = whatOpener(self.whatUser(),self.whatPass())
        w.requestCookies()
    
        f = w.opener().open('http://what.cd/torrents.php?id=243942')
        print "Refresh: opening url redirects to " + f.url

        cookies = w.getCookies()

        self.cookiesToFile(cookies)
        print 'Refresh: saving cookies to file'

    def wOpener(self):

        name =self.whatUser()
        pw =self.whatPass()
        whatdir = self.whatPath()
        import pickle

        if not os.path.isfile(self.whatCookieFile()):
            self.refreshCookies()

        w = whatOpener(name,pw)
        cookies = self.cookiesFromFile()
        w.setCookies(cookies)
        print 'loading cookies'
        
        return w


    
    def wrap(self):    
        return wdb.db().soup(self.User())


    #Some utils for query what.cd artists.
    def addArtistQueryWithHTML(self,strname, force_reload = False):
        query = self.convertQuery(strname)
        artid = self.getArtIDForQuery(query)
        if not artid:
            self.addArtistForQuery(query)
            artod = self.getArtIDForQuery(query)
    
        w = self.wrap()
        e = w.exists("""
select * from artist_html
where artist = :artid
""",{'artid':artid})
        w.close()
        
    
        if not e:
            q = self.fetchArtistQuery(query)
            html = q['html']
            url = q['url']
            self.addHTMLForArtist(html,artid)
            self.setWhatIDForArtistFromURL(artid,url)
        elif force_reload:
            q = self.fetchArtistQuery(query)
            html = q['html']
            url = q['url']                                    
            self.resetHTMLForArtist(html,artid) 
            self.setWhatIDForArtistFromURL(artid,url)        
        else:
            print 'sorry, artist already has html...'
            print 'not bothering to update'

    def refreshRelease(self, releaseid,force_reload_html = True):
        whatid = getWhatIDForReleaseID

    def addRelease(self, whatgrp, artistid,force_reload = False):
        whatid = re.search(re.compile('id=(\d+)'),whatgrp).group(1)
        w = self.wrap()
        try:
            releaseid = self.getReleaseIDForWhatID(whatid)
        except:
            w.query("""
insert into release(whatid)
values(:whatid)""",
                    {'whatid':whatid})
            w.commit()     
            releaseid = self.getReleaseIDForWhatID(whatid)

        w.query("""
insert into artist_release(artist, release)
values(:artid, :releaseid)""", {'artid':artistid,'releaseid':releaseid})


        f = self.fetchReleaseID(whatid)
        html = f['html']

        e = w.exists("""
select * from release_html
where release = :releaseid
""",{'releaseid':releaseid})
        w.commit()
        w.close()

        if not e:
            self.addHTMLForRelease(html,releaseid)
        elif force_reload:
            self.resetHTMLForRelease(html,releaseid)
        else:
            print 'HTML Exists for release and force_rest is unselected'

    def setWhatIDForArtistFromURL(self,artid,url):
        whatid = re.search(re.compile('id=(\d+)'),url).group(1)
        w = self.wrap()
        w.query('update artist set whatid = :whatid where id = :artid;',
                {'whatid':whatid,'artid':artid})
        w.commit()
        w.close()
    def setWhatIDForReleaseFromURL(self,releaseid,url):
        whatid = re.search(re.compile('id=(\d+)'),url).group(1)
        w = self.wrap()
        w.query('update release set whatid = :whatid where id = :releaseid;',
                {'whatid':whatid,'releaseid':releaseid})
        w.commit()
        w.close()        
    def getArtIDForQuery(self,strname):
        query = self.convertQuery(strname)
        db = self.wrap()
        
        e = db.exists(
            """
select id 
from artist 
where artist.name = :name
"""
            ,{'name':query})
        if not e:
            self.addArtistForQuery(query)

        d = db.queryToDict(
            """
select id 
from artist 
where artist.name = :name
"""
            ,{'name':query})   
        db.close()
        return d[0]['id']


    def getArtIDForWhatID(self,whatid):
        db = self.wrap()
        d = db.queryToDict("""
select id from artist
where whatid = :whatid
""",
                      {'whatid':whatid})
        db.close()
        if d == []:
            raise Exception("artIDForWhatID failed: no such artist with whatid");
        return d[0]['whatid']
        
            
                      
    def getReleaseIDForWhatID(self,whatid):
        db = self.wrap()
        d = db.queryToDict("""
select id from release
where whatid = :whatid
""",
                      {'whatid':whatid})
        db.close()
        if d == []:
            raise Exception("releaseIDForWhatID failed: no such release with whatid");        
        return d[0]['id']

    def getReleaseIDForWhatID(self,whatid):
        db = self.wrap()
        d = db.queryToDict("""
select id from release
where whatid = :whatid
""",
                      {'whatid':whatid})
        db.close()
        if d == []:
            raise Exception("releaseIDForWhatID failed: no such release with whatid");        
        return d[0]['id']


    def addArtistForQuery(self,strname):
        query = self.convertQuery(strname)
        db = self.wrap()
        d = db.query(
            """
INSERT INTO artist(name)
values(:strname)
"""
            ,{'strname':query})     
        db.commit()
        db.close()


    def resetHTMLForRelease(self,html,releaseid):
        db = self.wrap()

        d = db.queryToDict("""
select filename
from release_html
where release = :releaseid
""",{'releaseid':releaseid})
        db.close()
        fname = d[0]['filename']
        f = open(fname,'w')
        f.write(html)
        
        

    def resetHTMLForArtist(self,html,artid):
        db = self.wrap()

        d = db.queryToDict("""
select filename
from artist_html
where artist = :artid
""",{'artid':artid})
        db.close()
        fname = d[0]['filename']
        f = open(fname,'w')
        f.write(html)
        
        
    def resetCookies(self):
        cookiepath = self.whatCookieFile()
        

    def addHTMLForRelease(self, html,releaseid):
        hpath = self.whatHTMLPath()
        files = os.listdir(hpath)
        highest = 0
        for f in files:
            numre = re.compile("(\d+)\.html")
            match = re.search(numre,f)
            if match != None:
                num = int(match.group(1))
                if num > highest: highest = num
        namestring = str(highest + 1)+".html"
        fname = os.path.join(hpath,namestring)
        f = open(fname,'w')
        f.write(html)
        f.close()
        
        db = self.wrap()
        db.query("""
insert into release_html(release, filename)
values(:releaseid, :filename);
"""
                 ,{'releaseid':releaseid,'filename':fname})
        
        db.commit()
        db.close()
    

    def addHTMLForArtist(self,html,artid):
        hpath = self.whatHTMLPath()
        files = os.listdir(hpath)
        highest = 0
        for f in files:
            numre = re.compile("(\d+)\.html")
            match = re.search(numre,f)
            if match != None:
                num = int(match.group(1))
                if num > highest: highest = num
        namestring = str(highest + 1)+".html"
        fname = os.path.join(hpath,namestring)
        f = open(fname,'w')
        f.write(html)
        f.close()
        
        db = self.wrap()
        db.query("""
insert into artist_html(artist, filename)
values(:artid, :filename);
"""
                 ,{'artid':artid,'filename':fname})
        
        db.commit()
        db.close()

 
        
 
    def getMBIDsForArtist(self,artid):
        w = self.wrap()
        d = w.queryToDict("""
select gid from artist_gids
where artist = :artid
""",{'artid':artid})
        w.close()
        if len(d) == 0:
            return None
        else:
            return map(lambda x : x['gid'], d)
        
    def getMBIDsForArtistQuery(self,strname):
        "Wraps mbidsForArtist"
        query = self.convertQuery(strname)
        artid = self.getArtIDForQuery(query)
        self.mbidsForArtist(artid)

    def getHTMLForArtist(self,artid):
        db = self.wrap()
        d = db.queryToDict("""
select filename
from artist_html
where artist = :artid
""",{'artid':artid})
        db.close()
        if len(d) == 0:
            html = None
        else:
            fname = d[0]['filename']
            html = open(fname).read()
        return html
    def getHTMLForRelease(self,releaseid):
        db = self.wrap()
        d = db.queryToDict("""
select filename
from release_html
where release = :releaseid
""",{'releaseid':releaseid})
        db.close()
        if len(d) == 0:
            html = None
        else:
            fname = d[0]['filename']
            html = open(fname).read()
        return html


    def makeMBIDsForArtistQuery(self, strname):
        "Wraps mbidsForArtist"
        query = self.convertQuery(strname)
        artid = self.getArtIDForQuery(query)
        self.makeMBIDsForArtist(artid)


    def makeMBIDsForArtist(self,artid):
        import tagger.matcher as matcher
        w = self.wrap()
        name = w.queryToDict("select name from artist where id = :artid",
                             {'artid':artid})[0]['name']
        print name
        gids = map(lambda x: x['gid'], matcher.matchArtistString(name))

        w.query("""
delete from artist_gids
where artist = :artid
;""",
                {'artid':artid})
        for g in gids:
                       w.query("""
insert into artist_gids(artist, gid)
values(:artid,:gid)
;""",
                               {'artid':artid,'gid':g})
                   
        w.commit()
        w.close()
        
    def makeMBIDsForArtistReleases(self,artistid):
        w = self.wrap()

        d = w.queryToDict("select release.id from release, artist_release where artist_release.release = release.id and artist_release.artist = :artistid",{'artistid':artistid})

        releaseids = map(lambda x: x['id'],d)
        print releaseids
        for r in releaseids:
            self.makeMBIDsForRelease(r)
        
    def makeMBIDsForRelease(self,releaseid):
        pageHTML = self.getHTMLForRelease(releaseid)
        info = parsers.parseTorrentPage(pageHTML)
        raise Exception()

    def makeReleasesForArtist(self,artid):
        html = self.getHTMLForArtist(artid)
        grps = self.torrentGroupsFromArtistHTML(html)
        w = self.wrap()

        w.query("""
delete from artist_release
where artist = :artid
""",
                {'artid':artid})
        w.commit()
        w.close()
        for g in grps:
            self.addRelease(g,artid)

    def convertQuery(self,query):
        query = query.lower()
        return query

    

    def fetchReleaseID(self,whatid):
        url = 'http://what.cd/'+'torrents.php?id='+whatid
        o = self.wOpener().opener()
        f = o.open(url)
        redirect_url = f.url

        if redirect_url == 'http://what.cd/login.php':
            self.refreshCookies()
            o = self.wOpener().opener()
            f = o.open(url)
            redirect_url = f.url

        out = {'html':f.read(),'url':redirect_url}
        return out
        

    def fetchArtistQuery(self,query):
        o = self.wOpener().opener()
        url = "http://what.cd/artist.php?"+ urllib.urlencode({'artistname':query})
        f = o.open(url)
        redirect_url = f.url
        if redirect_url == 'http://what.cd/login.php':
            self.refreshCookies()
            o = self.wOpener().opener()
            f = o.open(url)
            redirect_url = f.url

            
        print "Artist query for: " + query + " redirected to "+redirect_url
        if not 'artist' in redirect_url:
            return None
        else:
            return {'url':redirect_url,'html':f.read()}

#artIDForQuery,
#artIDForWhatID,
#releaseIDForWhatID
#all are designed to access the local what db and write 
#a new entry if no what id is yet stored for the given #
#query/whatid.

    def loggedTorrentAlbumsFromHTML(self,html):
        from pyquery import PyQuery as pq
        d = pq(html);
        elts =  d("#torrents_album").find("td").find("a").filter(lambda i : pq(this).html() != None).filter(lambda i : re.search(relog,pq(this).html()) != None)
        elts.each(lambda x : (   logged.append((x))))
        for f in logged:
            s = f.attr('href');
            t_id = re.compile("[^t]id=([0-9]*)").search(s).group(1)
            t_grp_id = re.compile("torrentid=([0-9]*)").search(s).group(1)
            
    def torrentGroupsFromArtistHTML(self,html):
        from pyquery import PyQuery as pq
        d = pq(html);
        grps = []
        elts = d("#discog_table").find("td").find("a").filter(lambda i : pq(this).attr("title") == 'View Torrent')
        elts.each(lambda x: (grps.append(x.attr("href"))))
        return grps

    

    def logListFromTorrentGroupID(self,html):
        pass



    def initArtistQuery(self,query):
        #Establishes an artist in the db with html and a whatid.
        self.addArtistQueryWithHTML(query,True)
        self.makeMBIDsForArtistQuery(query)
        artid = self.getArtIDForQuery(query)
        self.makeReleasesForArtist(artid)
        
