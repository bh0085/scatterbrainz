def requestWithUserAndParams(user, params):

    import sb_helpers as sh
    import what.whathelpers as wh
    wp = wh.whatPlug(user)
    try:
        action = params['action'][0]
    except KeyError as e:
        return ['No action found for params']
    
    req = None

    if action =='artists':
        req = []
        soup = wp.wrap()
        artists = soup.artist.all()
        for art in artists:
            i = art.id
            gids =map(lambda x: x.gid, soup.artist_gids.filter_by(artist=i).all())
            for g in gids:
                req.append({'artist_mbid':g,'name':art.name})
            
    elif action =='albums':
        soup = wp.wrap()
        req = map(lambda x: x.name, id.release.all())
    else:
        raise Exception('unimplemented action: '+action)

    for r in req: r['datatype'] =sh.dtFromAction(action)
    for r in req: r['action'] = action
    return req
