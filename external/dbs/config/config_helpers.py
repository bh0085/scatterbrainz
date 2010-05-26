import dbs.config.queryConfig as qc
import sqliteWrapper as sqw
def userExists(uname):
    dbf = qc.query('config_dbfile')
    e = sqw.sqliteWrapper(dbf).exists("select * from user where user.name = :uname",{'uname':uname})
    return e


def userPassword(uname):
    dbf =  qc.query('config_dbfile')
    pw = sqw.sqliteWrapper(dbf).queryToDict("select password from user where user.name = :uname",{'uname':uname})[0]['password']
    return pw
