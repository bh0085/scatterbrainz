import MultipartPostHandler, urllib2, cookielib
import urllib

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
                

