"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from scatterbrainz.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

from scatterbrainz.model.track import Track
from scatterbrainz.model.album import Album
from scatterbrainz.model.artist import Artist
Artist.tracks = orm.relation(Track, backref='artist')
Album.tracks = orm.relation(Track, backref='album')
