import sb_helpers as sh

def requestWithUserAndParams(user, params):
    #for now, the user key is meaningless
    action = params['action'][0]

    import dbs.mbrainz.fetchMB as fm
    src_module = fm

    req  = None

    if action == 'albums':
        tryfilter = 'artist_mbid'
        if req == None and tryfilter in params.keys():
            req = src_module.getMBIDArtistAlbums(params[tryfilter])
        if req == None:
            req = src_module.getAllAlbums()   
            print 'request: ' + str(req)
 
    elif action =='artists':
        req = src_module.getAllArtists();

    elif action =='members':
        tryfilter = 'album_mbid'
        if req == None and tryfilter in params.keys():
            req = src_module.getMBIDAlbumMembers(params[tryfilter])
        tryfilter = 'artist_mbid'
        if req == None and tryfilter in params.keys():
            req = src_module.getMBIDArtistMembers(params[tryfilter])
        if req == None:
            req = src_module.getAllMembers()                   

    elif action =='tracks':
        tryfilter = 'album_mbid'
        if req ==None  and tryfilter in params.keys():
            req = src_module.getMBIDAlbumTracks(params[tryfilter])
        tryfilter = 'artist_mbid'
        if req == None and tryfilter in params.keys():
            req = src_module.getMBIDArtistTracks(params[tryfilter])
        if req == None:
            req = src_module.getAllTracks()
    
    if req == None:
        raise Exception('unhandled action for request ' + str(params))

    
    for r in req: r['datatype'] =sh.dtFromAction(action)
    for r in req: r['action'] = action

    return req
