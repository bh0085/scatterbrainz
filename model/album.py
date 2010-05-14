from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Unicode, DateTime, Boolean, ForeignKey

from scatterbrainz.model.meta import metadata

Base = declarative_base(metadata=metadata)
class Album(Base):

    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    artistid = Column('artistid', Integer, ForeignKey('artists.id'))
    mbid = Column(Unicode)
    albumArtURL = Column(Unicode)
    added = Column(DateTime, nullable=False)

    def __init__(self, name, artist, mbid, albumArtURL, added):
        self.name = name
        self.artist = artist
        self.mbid = mbid
        self.albumArtURL = albumArtURL
        self.added = added
    
    def toTreeJSON(self, children=None):
        json = {
                'attributes': {'id'   : self.__class__.__name__ + '/' + str(self.id),
                               'class': 'browsenode',
                               'rel'  : self.__class__.__name__
                              },
                'data': self.name or "&nbsp;", # jstree bug triggers on null or ""
                'state' : 'closed'
               }
        if children is not None:
            json['state'] = 'open'
            json['children'] = children
        else:
            json['state'] = 'closed'
        return json

    def __repr__(self):
        return "<Album%s>" % (self.__dict__)
