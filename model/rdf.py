from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from scatterbrainz.model.meta import metadata

Base = declarative_base(metadata=metadata)
class RDFTriple(Base):
    __tablename__ = 'triples'

    id = Column(Integer, primary_key=True)
    
    subject = Column(Unicode, nullable = False)
    predicate = Column(Unicode, nullable = False)
    obj = Column(Unicode, nullable = False)

    artistid = Column('artistid', Integer, ForeignKey('artists.id'))
    albumid = Column('albumid', Integer, ForeignKey('albums.id'))
    trackid = Column('trackid',Integer, ForeignKey('tracks.id'))

    #A true RDF triple would have no need for these associations...
    #For subject, and object can be strings, uri references or they may 
    #be one of :artist, :album, :track.
    #
    #In the case where subj/obj in {:track,:album,:artist}, the relevant
    #id should be treated as the subj/obj. This simple (and bad) scheme 
    #does not allow one artist to refer to another... I suppose though,
    #that an artist may refer to herself.


    def __init__(self,subject,predicate, obj, artist=None, track = None, album = None):
        self.subject = subject
        self.predicate = predicate
        self.obj = obj
        self.artist = artist
        self.album = album
        self.track = track

    def __repr__(self):
        return "s: "+self.subject+", p: "+self.predicate+", o: "+self.obj
