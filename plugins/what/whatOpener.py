import MultipartPostHandler, urllib2, cookielib
import urllib

class whatOpener():
    o = None;
    def opener(self):
        if whatOpener.o == None:
            self.reload()

        return whatOpener.o
    def reload(self):
        print "Opening new connection to what.cd"
        # build opener with HTTPCookieProcessor
        o = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        urllib2.install_opener( o)
        
        # assuming the site expects 'user' and 'pass' as query params
        p = urllib.urlencode( { 'username' : 'bh0085','password':'dinobot1w' })
        
        # perform login with params
        f = o.open( u'http://what.cd/login.php',  p )
        f.close()
        whatOpener.o = o
