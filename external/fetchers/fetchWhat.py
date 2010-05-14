import what
import remote_sql.fetchRemote as fr
import pdb
import pprint

ws_address = '94.100.21.250:5555'

def getMBIDAlbumAlbums():
    mbid = '735b3a58-3d9b-4f0d-8601-8a041facd6b3'

    data = fr.getMBIDAlbumInfo(mbid)[0]
    
    search_terms = []
    search_terms.extend(unicode.split(data['artist_name'],' '))
    search_terms.extend(unicode.split(data['album_name'],' '))
    data = what.searchTermsToWhat(search_terms)

    tracks = fr.getMBIDAlbumTracks(mbid);
    pprint.pprint(tracks)
    
    pdb.set_trace()
