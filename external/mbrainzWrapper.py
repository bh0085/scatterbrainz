import postgresWrapper as pgw
import dbs.config.queryConfig as qc
class mbrainzWrapper(pgw.postgresWrapper):
    def __init__(self):
        self.port = int(qc.query('mbport'))
        self.host = str(qc.query('mbhost'))
        self.user = str(qc.query('mbuser'))
        self.db = qc.query('mbdb')
        self.cxn = None
        self._openCXN()
        print 'opened mbrainz cxn with host'+self.host
