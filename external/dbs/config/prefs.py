import dbs.config.queryConfig as qc
import sqliteWrapper as sqw
def writePref(name, value, username = None):
    
    db = sqw.sqliteWrapper(qc.query('config_dbfile'))
    if not username:
        db.query("""
INSERT OR REPLACE INTO 
global(name, value)
values(:name,:value) ;
"""
                           ,params = {'name':name,
                                      'value':value})
    else:
        uid = db.queryToDict("""SELECT id FROM user WHERE name = :username;""",params={'username':username})[0]['id']
        d = db.query("""
INSERT OR REPLACE INTO 
user_prefs(name, value, user)
values(:name,:value,:user);
"""
                           ,params = {'name':name,
                                      'value':value,
                                      'user':uid})
    db.commit()
    db.close()

def deletePref(name, username = None):
    
    db = sqw.sqliteWrapper(qc.query('config_dbfile'))
    if not username:
        db.query("""
DELETE FROM global
WHERE name =:name;
"""
                           ,params = {'name':name})
    else:
        uid = db.queryToDict("""SELECT id FROM user WHERE name = :username;""",params={'username':username})[0]['id']
        d = db.query("""
DELETE FROM user_prefs
WHERE  name = :name
AND user = :user;
"""
                           ,params = {'name':name,
                                      'user':uid})
    db.commit()
    db.close()

def readPref(name, username = None):
    db = sqw.sqliteWrapper(qc.query('config_dbfile'))
    if not username:
        d=db.queryToDict("""select value from global where name = :name""",
                         params = {'name':name})
    else:
        d = db.queryToDict("""
select value 
from user_prefs, user
where user_prefs.name = :name
and user.name = :username
and user_prefs.user = user.id;
"""
                           ,params = {"username":username, 
                                     "name":name}
                           )
    
    db.close()
    if len(d) == 0:
        return None
    else:
        return d[0]['value']
    
