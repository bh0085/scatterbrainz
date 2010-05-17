import sqlite3
from sqlite3 import OperationalError

class sqliteWrapper():
    #Query the centralized scatterbrainz DB
    #For now, should call _cursor and close the cursor manually when done.

    def __init__(self,dbfile):
        self.cxn = None
        self.dbfile = dbfile
        self._openCXN()
                
    def _openCXN(self):
        self.cxn = sqlite3.connect(self.dbfile)
    def _closeCXN(self):
        self.cxn.close()
    def _cxn(self):
        return self.cxn
    def _cursor(self):
        if not self._cxn():
            self._openCXN()
            print "Initializing connection"
        return self._cxn().cursor()

    def commit(self):
        self._cxn().commit()
    def query(self, query):
        cursor = self._cursor()
        cursor.execute(query)

    def queryToDict(self,query):
        cursor = self._cursor()
        cursor.execute(query)
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

