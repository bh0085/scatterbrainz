import dbs.requests.sb_fetcher as sbf
import what.whathelpers as wh

class fetcher(sbf.sb_fetcher) :
    def getMBIDAlbumInfo(self,gid):raise Exception()
    def getAllArtists(self):
        wp = wh.whatPlug(self.user)

        req = []
        soup = wp.wrap()
        artist_mbids = soup.artist_gids.all()
        for amb in artist_mbids:
            art = soup.artist.filter_by(id = amb.artist).first()
            name = art.name
            req.append({'artist_mbid':amb.gid,'name':name})
        return req

    def getMBIDArtistAlbums(self,gid):
        wp = wh.whatPlug(self.user)

        req = []
        soup = wp.wrap()
        gid_matches = soup.artist_gids.filter_by(gid = gid).all()
        for g in gid_matches:
            i = g.artist
            releases = soup.artist_release.filter_by(artist = i).all()
            for r in releases:
                rval = soup.release.filter_by(id = r.release).first()
                print rval.name

                name = rval.name
                mbids =  soup.release_gids.filter_by(release = rval.id).all()
                if len(mbids) == 0:
                    req.append({'artist_mbid':gid,'name':name})
                else:
                    for m in mbids:
                        req.append({'artist_mbid':gid,'name':name,'album_mbid':m.gid})
        return req

    def getMBIDArtistTracks(self,gid):
        return []
    def getMBIDArtistMembers(self,gid):
        return []

    def getAllAlbums(self):
        req = []
        wp = wh.whatPlug(self.user)
        soup = wp.wrap()        
        releases = soup.release.all()
        for r in releases:
            mbids =  soup.release_gids.filter_by(release = r.id).all()
            if len(mbids) == 0:
                req.append({'name':r.name})
            else:
                for m in mbids:
                    req.append({'name':r.name,'album_mbid':m.gid})
        return req

    def getMBIDAlbumMembers(self,gid):
        return []
    def getMBIDAlbumTracks(self,gid):
        return []
    def getAllTracks(self): 
        return []
    def getAllMembers(self):
        return []

 
