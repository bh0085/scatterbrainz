#An sb fetcher interface... is it really needed?
#...probably not. I haven't had any problems with typing thus far.
#well. It doesn't seem to hurt.

class sb_fetcher():
    def __init__(self,user):
        self.user = user
    def getMBIDAlbumInfo(self,gid):raise Exception()
    def getAllArtists(self):raise Exception()
    def getMBIDArtistAlbums(self,gid):raise Exception()
    def getMBIDArtistTracks(self,gid):raise Exception()
    def getMBIDArtistMembers(self,gid):raise Exception()
    def getAllAlbums(self):raise Exception()
    def getMBIDAlbumMembers(self,gid): raise Exception()
    def getMBIDAlbumTracks(self,gid):raise Exception()
    def getAllTracks(self): raise Exception()
    def getAllMembers(self): raise Exception()
