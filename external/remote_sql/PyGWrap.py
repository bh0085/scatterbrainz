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
