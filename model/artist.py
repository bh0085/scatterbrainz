from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Unicode, DateTime

from scatterbrainz.model.meta import metadata

Base = declarative_base(metadata=metadata)
class Artist(Base):

    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    mbid = Column(Unicode)
    added = Column(DateTime, nullable=False)

    def __init__(self, name, mbid, added):
        self.name = name
        self.mbid = mbid
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
        return "<Artist%s>" % (self.__dict__)
