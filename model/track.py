from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Unicode, DateTime, ForeignKey

from scatterbrainz.model.meta import metadata
from scatterbrainz.model.artist import Artist

from scatterbrainz.controllers import renderer as r

Base = declarative_base(metadata=metadata)
class Track(Base):

    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    
    # Joins
    artistid = Column('artistid', Integer, ForeignKey('artists.id'))
    albumid = Column('albumid', Integer, ForeignKey('albums.id'))
    
    # Filesystem props
    filepath = Column(Unicode, nullable=False)
    filesize = Column(Integer, nullable=False)
    filemtime = Column(DateTime, nullable=False)
    
    # MP3 props
    mp3bitrate = Column(Integer, nullable=False)
    mp3samplerate = Column(Integer, nullable=False)
    mp3length = Column(Integer, nullable=False)
    
    # ID3 props
    id3artist = Column(Unicode)
    id3album = Column(Unicode)
    id3title = Column(Unicode)
    id3tracknum = Column(Unicode)
    id3date = Column(Unicode)
    id3composer = Column(Unicode)
    id3genre = Column(Unicode)
    id3lyricist = Column(Unicode)

    # MusicBrainz Properties (or "props" for short)
    mbid = Column(Unicode)
    
    # Generated props
    added = Column(DateTime, nullable=False)

    def __init__(self, artist, album, filepath, filesize, filemtime, mp3bitrate,
                 mp3samplerate, mp3length, id3artist, id3album, id3title,
                 id3tracknum, id3date, id3composer, id3genre, id3lyricist,
                 added,mbid):
        self.artist = artist
        self.album = album
        self.filepath = filepath
        self.filesize = filesize
        self.filemtime = filemtime
        self.mp3bitrate = mp3bitrate
        self.mp3samplerate = mp3samplerate
        self.mp3length = mp3length
        self.id3artist = id3artist
        self.id3album = id3album
        self.id3title = id3title
        self.id3tracknum = id3tracknum
        self.id3date = id3date
        self.id3composer = id3composer
        self.id3genre = id3genre
        self.id3lyricist = id3lyricist
        self.mbid = mbid
        self.added = added
    
    def toPlaylistJSON(self):
        return dict(id = self.id,
                    title = r.title(self),
                    artist = r.artist(self),
                    album = r.album(self),
                    tracknum = r.tracknum(self),
                    filepath = r.filepath(self),
                    bitrate = r.bitrate(self),
                    length = r.length(self))
    
    def toTreeJSON(self):
        json = {
                'attributes': {'id'   : self.__class__.__name__ + '/' + str(self.id),
                               'class': 'browsenode',
                               'rel'  : self.__class__.__name__
                              },
                'data': self.id3title or "&nbsp;" # jstree bug triggers on null or ""
               }
        return json

    def __repr__(self):
        return "<Track%s>" % (self.__dict__)
