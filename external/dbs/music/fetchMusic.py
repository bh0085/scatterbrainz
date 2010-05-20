#FETCH TRACKS FROM THE LOCAL DBS GIVEN PARAMETERS DICT.
import dbs.config.queryConfig as qc
import sqliteWrapper as sw
def fetchWithParams(params):
    sqw = sw.sqliteWrapper(qc.query('music_dbfile'))
    d = sqw.queryToDict("select * from tracklist")
    sqw.close()
    return d
