from sqlalchemy.orm import scoped_session, sessionmaker
import dbs.config.prefs as prefs


class db():
    _soup = None
    _user = None
    _dbset = False
    print "Setting initial class values for db"

    def _makeSoup(self):
        from sqlalchemy.ext.sqlsoup import SqlSoup
        
        "A wrapper for a user's what db, at 'what_$user.sqlite'"
        dbfile = prefs.readPref('what_dbfile',self._user)
        dbstr = 'sqlite:///'+dbfile
        print "Wrapping soup with dbfile: " + dbstr
        db._soup = SqlSoup(dbstr)#,session=scoped_session(sessionmaker(autoflush = True, expire_on_commit=False, autocommit=True)))
        print "Setting autoflush, autocommit = True for sqlite session"

        db._dbset = True

    
    def _killSessions(self):
        import sqa_helpers as sah
        sah.ssCloseAll()
        db._dbset = False
        db._soup = None
        db._user = None
    def killall(self):
        print "whatdb, killing all connections"
        self._killSessions()

    def soup(self, user = None):
        if user ==None:
            print "no user specified for what db, assuming bh0085"
            self._user = 'bh0085'
        else:
            print "note, user switching is not really implemented yet."
            self._user = user

        if not db._dbset:
            self._makeSoup()
        return db._soup
    
    def commit(self):
        s = self.session()
        s.commit()

    def session(self):
        from sqlalchemy.ext.sqlsoup import Session
        return Session

        
    
    
