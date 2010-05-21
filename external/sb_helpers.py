import dbs.config.queryConfig as qc
import urllib2
import sqliteWrapper as sqw
def sb_root_url():
    addr = qc.query('sb_address')
    port = qc.query('sb_port')
    url ="http://"+str(addr)+":"+str(port)
    return url


def queryLocalSB(rel):
    address = sb_root_url()+rel
    o = urllib2.build_opener()
    data = o.open(address).read()
    return data
    

def getMyIP():
    import urllib2
    o = urllib2.build_opener()
    ip= o.open("http://www.whatismyip.org/").read()
    o.close()
    return ip

def listUsers():
    db = sqw.sqliteWrapper(qc.query('config_dbfile'))
    d = db.queryToDict('select name from user;');
    db.close
    return d

def userID(username):
    db = sqw.sqliteWrapper(qc.query('config_dbfile'))
    d = db.queryToDict('select id from user where name = :username;',params = {'username':username});
    db.close
    if len(d) == 0:
        return None
    else:
        return d[0]['id']

def listPrefs(username = None):
    db = sqw.sqliteWrapper(qc.query('config_dbfile'))
    if username:
        uid = userID(username);
        if not uid : return None
        d = db.queryToDict('select name, value from user_prefs where user = :uid;',params = {'uid':uid});
    else:
        d = db.queryToDict('select name, value from global;')
    db.close
    return d

