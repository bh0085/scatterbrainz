import sb_helpers as sh

def register(plugname,username):
    if pluginRegistered(plugname,username):
        raise Exception("Plugin, "+plugname+" already registered for "+username)
    else:
        w = sh.wrap('config')
        uid = sh.userID(username)
        w.query("""
INSERT INTO plugin(name, user)
values(:plugname,:uid);
""",
                params = {'plugname':plugname,'uid':uid})
        w.commit()
        w.close()
    
def pluginRegistered(plugname,username):
    w = sh.wrap('config')
    e =  w.exists("""
select * from plugin, user 
where user.name = :username 
and plugin.name = :plugname
and plugin.user = user.id;""",
                  params = {'plugname':plugname, 'username':username})
    w.close()
    return e

def unregister(plugname, username):
    if not pluginRegistered(plugname,username):
        raise Exception("Plugin, "+plugname+" not registered for "+username)
    else:
        w = sh.wrap('config')
        uid = sh.userID(username)
        w.query("""
DELETE FROM plugin
WHERE name = :plugname
AND user = :uid;
""",
                params = {'plugname':plugname,'uid':uid})
        w.commit()
        w.close()
        
