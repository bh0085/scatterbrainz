from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Unicode, DateTime

from scatterbrainz.model.meta import metadata

Base = declarative_base(metadata=metadata)
class Artist(Base):

    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    added = Column(DateTime, nullable=False)

    def __init__(self, name, added):
        self.name = name
        self.added = added

    def __repr__(self):
        return "<Artist%s>" % (self.__dict__)