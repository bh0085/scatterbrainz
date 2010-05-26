import what.db as wdb
import what.parsers as parsers

class wdbElt():
    def __init__(self,plug,initid):
        self.uname = plug.whatUser()
        self.plug = plug
        self.id = initid 
    def soup(self):
        return wdb.db().soup(self.uname)
    def commit(self):
        wdb.db().commit()
    def whatID(self):
        return self.getElt().whatid
    def name(self):
        return self.getElt().name
    def setName(self,name):
        print self.getElt().name
        self.getElt().name = name
        print self.getElt().name
    

class Release(wdbElt):
    def getElt(self):
        return self.r()
    def r(self):
        return self.soup().release.filter_by(id = self.id).first()
    def releaseID(self):
        return self.r().id
    def html(self):
        s = self.soup()
        fname = s.release_html.filter_by(id = self.id).first().filename
        html = open(fname).read()
        return html
      
    def artists(self):
        s = self.soup()
        ids  = map(lambda x : x.artist,s.artist_release.filter_by(release = self.releaseID()).all())
        artists = []
        for i in ids: artists.append(s.artist.filter_by(id=i).first())
        return artists

    def refresh(self,title = None):
        if self.whatID() == None:
            raise Exception("no whatid")
        if self.releaseID() == None:
            raise Exception("no releaseid") 
        if self.artists() == None:
            raise Exception("no artists")
        if True : #self.name() == None:
            html =  self.html()
            if title == None: title = parsers.parseTorrentPageToTitle(html)
            self.setName(title)
            print self.name()
            

class Artist(wdbElt):
    def getElt(self):
        return self.a()
    def a(self):
        return self.soup().artist.filter_by(id = self.id).first()
    def refresh(self):
        print "no refresh methods yet implemented for artist..."
    def releases():
        s = self.soup()
        ids = map(lambda x : x.release,s.artist_release.filter_by(artist = self.artistID()).all())
        releases = []
        for i in ids: releases.append(s.release.filter_by(id=i).first())
        return releases
    def makeMBIDs(self):
        import tagger.matcher as matcher
        s = self.soup()
        name = s.artist.filter_by(id = self.id).first().name
        gids =  map(lambda x: x['gid'], matcher.matchArtistString(name))
        
        matches = s.artist_gids.filter_by(artist = self.id).all()
        for m in matches:
            s.delete(m)

        for g in gids: s.artist_gids.insert(artist=self.id,gid=g)
        s.commit()
        return map( lambda x: x.gid, s.artist_gids.all())

    def makeHTML(self):
        pass
