#Request format
import memcache

def requestWithParams(user,db,params,force_reset=False):
    key = makeKey(user,db,params)
    result = request(key,force_reset)
    return(result)

def request(key,force_reset = False):
    c=memcache.Client(['127.0.0.1:11211'])
    
    print key
    print 'was_key'
    val = None
    if not force_reset:
        val = c.get(key)

    if val != None: 
        return val

    user,db,params = parseKey(key)
    
    val = retrieveDB(user,db,params)
    import string
    print 'setting value in memcached'
    c.set(key,val)
    return val
    

def retrieveDB(user,db,params):
    if db=='what':
        from what.fetchWhat import fetcher as f
    elif db=='music':
        from dbs.music.fetchMusic import fetcher as f
    elif db =='mbrainz':
        from dbs.mbrainz.fetchMB import fetcher as f
    else:
        raise Exception( 'unhandled db request for db' + db)

    import dbs.requests.sb_dbrouter as dbr
    return dbr.route(f(user),params)


def parseKey(key):
    spl = str.split(key,"::")
    return (spl[0],spl[1],parseAction(spl[2]))

def makeKey(user,db,params):
    action = makeAction(params)
    keyval = user+'::'+db+'::'+action
    if type(keyval) == unicode:
        keyval = unicode.encode(keyval)
    return keyval

def makeAction(params):
    #url encoded designed to include dictionaries whose values may be lists.
    import urllib
    p_list = []
    for key,value in params.iteritems():
        if type(value) != list:
            p_list.append(urllib.urlencode({key:value}))
        else:
            for elt in value:
                p_list.append(urllib.urlencode({key:elt}))
    
    import string
    p_final = string.join(p_list,'&')
    return p_final
def parseAction(encoded):
    import urlparse
    parse = urlparse.parse_qs(encoded)
    return parse
