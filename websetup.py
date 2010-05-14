"""Setup the scatterbrainz application"""
import logging

from scatterbrainz.config.environment import load_environment
from scatterbrainz.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup scatterbrainz here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info("Creating tables")
    meta.metadata.create_all(bind=meta.engine,checkfirst=False)
    log.info("Tables created")
