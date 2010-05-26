import sb_helpers as sh
def route(fetcher,params):
    #for now, the user key is meaningless
    action = params['action'][0]
    req  = None

    if action == 'albums':
        tryfilter = 'artist_mbid'
        if req == None and tryfilter in params.keys():
            req = fetcher.getMBIDArtistAlbums(params[tryfilter][0])
        if req == None:
            req = fetcher.getAllAlbums()   
            print 'request: ' + str(req)
 
    elif action =='artists':
        req = fetcher.getAllArtists();

    elif action =='members':
        tryfilter = 'album_mbid'
        if req == None and tryfilter in params.keys():
            req = fetcher.getMBIDAlbumMembers(params[tryfilter][0])
        tryfilter = 'artist_mbid'
        if req == None and tryfilter in params.keys():
            req = fetcher.getMBIDArtistMembers(params[tryfilter][0])
        if req == None:
            req = fetcher.getAllMembers()                   

    elif action =='tracks':
        tryfilter = 'album_mbid'
        if req ==None  and tryfilter in params.keys():
            req = fetcher.getMBIDAlbumTracks(params[tryfilter][0])
        tryfilter = 'artist_mbid'
        if req == None and tryfilter in params.keys():
            req = fetcher.getMBIDArtistTracks(params[tryfilter][0])
        if req == None:
            req = fetcher.getAllTracks()
    
    if req == None:
        raise Exception('unhandled action for request ' + str(params))

    
    for r in req: r['datatype'] =sh.dtFromAction(action)
    for r in req: r['action'] = action

    return req
