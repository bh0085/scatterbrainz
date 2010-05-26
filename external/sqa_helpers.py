#A few helpers to help me keep my head straight.

from sqlalchemy.ext.sqlsoup import Session
import python_helpers as ph

#SQLSoup Helpers:
def ssCloseAll():
    s = Session()
    s.close_all()

def sses():
    s = Session()
    return s
