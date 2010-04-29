import musicbrainz2.webservice as ws
import musicbrainz2.model as m

def getAlbumsByArtist(artistid):
    q = ws.Query()
    inc = ws.ArtistIncludes(
        releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM),
        tags=True)
    artist = q.getArtistById(artistid, inc)
    return artist.getReleases()

def getTrackRelations(id):
    q = ws.Query()
    inc = ws.TrackIncludes(
        trackRelations=True,
        artistRelations=True,
        releaseRelations=True,
        urlRelations=True
        )
    r =q.getTrackById(id,inc)
    relations =  r.getRelations();
    return relations

def getReleaseRelations(id):
    q = ws.Query()
    inc = ws.ReleaseIncludes(
        trackRelations=True,
        artistRelations=True,
        releaseRelations=True,
        urlRelations=True
        )
    r =q.getReleaseById(id,inc)
    relations =  r.getRelations();
    return relations

def getArtistRelations(id):
    q = ws.Query()
    inc = ws.ArtistIncludes(
        trackRelations=True,
        artistRelations=True,
        releaseRelations=True,
        urlRelations=True
        )
    r =q.getArtistById(id,inc)
    relations =  r.getRelations();
    return relations

def searchRelease(artistName, albumName):
    q = ws.Query()
    if artistName:
        filter = ws.ReleaseFilter(title=albumName, artistName=artistName)
    else:
        filter = ws.ReleaseFilter(query=albumName)
    results = q.getReleases(filter)
    if results:
        return results[0].getRelease()
    return None

<<<<<<< HEAD
def getArtistsAssociated(art_mbid=u"f3b8e107-abe8-4743-b6a3-4a4ee995e71f"):
    q = ws.Query()
    filter = ws.ReleaseFilter(artistId=art_mbid)
    results = q.getReleases(filter)
    out = results

    import re
    year_re = re.compile("[0-9]{4}")
    track_results = []
    
    try:
        for r in results:
            r_mbid = r.release.getId()
            inc = ws.ReleaseIncludes(tracks=True,releaseEvents=True)
            release = q.getReleaseById(r_mbid, include=inc)
            if not release: continue
            tracks = release.getTracks()
            for t in tracks:
                track_mbid = t.getId()
                inc = ws.TrackIncludes(artistRelations=True)
                track_full = q.getTrackById(track_mbid,include = inc)
                track_results.append(track_full)
                
            fulldate = release.getEarliestReleaseDate()
            year =re.search(year_re,fulldate).group()
            title = r.release.getTitle()
            print year, title
    except ws.WebServiceError, e:
	print 'Error:', e
        raise Exception(e)
   

    return track_results
