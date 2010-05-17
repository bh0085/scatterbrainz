import pgdb
from pg import OperationalError




class PyGWrapper():
    cxn = None
    #Query the centralized scatterbrainz DB
    #For now, should call _cursor and close the cursor manually when done.

    def _openCXN(self):
        PyGWrapper.cxn = pgdb.connect(host = "rosa.feralhosting.com:64077",
                            database = "musicbrainz_db",
                            user = "bh0085")
    def _closeCXN(self):
        print "CLOSING"
        self._cxn().close()
    def _cxn(self):
        return PyGWrapper.cxn
    def _cursor(self):
        if not self._cxn():
            self._openCXN()
            print "Initializing connection"

        while True:
            try:
                cursor = self._cxn().cursor()
                break
            except OperationalError, e:
                self._openCXN()
                print "Refreshing connection"
        return cursor

    def queryToDict(self,query):
        cursor = self._cursor()
        try:
            cursor.execute(query)
        except OperationalError, e:
            print "There was a problem Querying the current cursor, retrying."
            try:
                self._closeCXN()
                cursor = self._cursor()
                cursor.execute(query)
                print "retry successful"
            except OperationalError, e:
                print "retry failed"
                return
            
        d = self.fetchDict(cursor)
        return d
    
    def fetchDict(self,cursor):
        fetched = cursor.fetchall()
        desc = cursor.description
        
        dicts = []
        for f in fetched:
            fdict = {}
            for i in range(len(desc)):
                key = unicode(desc[i][0],'utf-8')
                val =f[i]
                if val.__class__ == str:
                    val = unicode(val,'utf-8')
                fdict[key] = val 
            dicts.append(fdict)
        return dicts

