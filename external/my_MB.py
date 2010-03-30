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
    relations =  r.getRelations();#m.Relation.TO_ARTIST)
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
