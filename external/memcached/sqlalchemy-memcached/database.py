#!/usr/bin/python
"""
memcached objects for use with SQLAlchemy
"""
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import memcache
import sqlalchemy
import sqlalchemy.orm

SQLA_SESSION = sqlalchemy.orm.sessionmaker()

MEMCACHED_CLIENT = memcache.Client(['127.0.0.1:11211'])

class DetachedORMObject(object):
    """
    Session-detached object for use with ORM Mapping.  As the SQLAlchemy
    documentation indicates, creating and closing a session is not analogous
    to creating and closing a database connection.  Connections are pooled by
    the database engine by default.  Creating new sessions is of a minimal
    cost.  Also, objects using this wrapper will not likely interact in with
    the database through the full power of SQLAlchemy queries.

    """
    @classmethod
    def fetch_by_field(cls, field, value):
        """Fetch a mapped orm object with the give field and value"""
        session = SQLA_SESSION()
        try:
            class_object = session.query(cls).filter(field == value).one()
        except sqlalchemy.orm.exc.NoResultFound:
            class_object = None
        finally:
            session.close()
        return class_object

    def update(self):
        """Update the database with the values of the object"""
        session = SQLA_SESSION()
        session.add(self)
        session.commit()
        session.refresh(self)
        session.close()

    def refresh(self):
        """Refresh the object with the values of the database"""
        session = SQLA_SESSION()
        session.add(self)
        session.refresh(self)
        session.close()

    def delete(self):
        """Delete the object from the database"""
        session = SQLA_SESSION()
        session.add(self)
        session.delete(self)
        session.commit()
        session.close()


class MemcachedObject(object):
    """
    Object Wrapper for serializing objects in memcached. Utilizes an abstract
    method, get_isntance_key, to understand how to get and set objects that
    impliment this class.
    """
    @classmethod
    def get_cached_instance(cls, instance_key):
        """Retrieve and return the object matching the instance_key"""
        key = str(cls.__module__ + '.' + cls.__name__ + ':' \
           + str(instance_key))
        print "Memcached Getting:", key
        return MEMCACHED_CLIENT.get(key)

    def set_cached_instance(self, time=0, min_compress_len=0):
        """Set the cached instance of an object"""
        print "Memcached Setting:", self.get_cache_key()
        return MEMCACHED_CLIENT.set(self.get_cache_key(), self, time, \
            min_compress_len)

    def delete_cached_instance(self, time=0):
        """Wrapper for the memcached delete method"""
        print "Memcached Deleting:", self.get_cache_key()
        return MEMCACHED_CLIENT.delete(self.get_cache_key(), time)

    def get_cache_key(self):
        """Prepends the full class path of the object to the instance key"""
        return self.__class__.__module__ + '.' + \
            self.__class__.__name__ + ':' + self.get_instance_key()

    def get_instance_key(self):
        """Get the instance key, must be implemented by child objects"""
        raise NotImplementedError \
            ("'GetInstanceKey' method has not been defined.")


class MemcachedORMObject(DetachedORMObject, MemcachedObject):
    """
    Putting it all together now.  Implements both of the above classes. Worth
    noting is the method for checking to see if the fetch_by_field method is
    invoked using a primary key of the class.  The same technique is used to
    generate an instance key for an instance of the class.
    """
    @classmethod
    def fetch_by_field(cls, field, value):
        """Fetch the requested object from the cache and database"""
        orm_object = None
        matched_primary_key = True
        for key in cls._sa_class_manager.mapper.primary_key:
            if field.key != key.key:
                matched_primary_key = False
        if matched_primary_key:
            orm_object = cls.get_cached_instance('(' + str(value) + ')')
        if orm_object is None:
            orm_object = super(MemcachedORMObject, cls). \
                fetch_by_field(field, value)
            if orm_object is not None:
                orm_object.set_cached_instance()
        return orm_object

    def update(self):
        """Update the object in the database and memcached"""
        DetachedORMObject.update(self)
        self.set_cached_instance()

    def refresh(self):
        """Refresh the object from the database and memcached"""
        DetachedORMObject.refresh(self)
        self.set_cached_instance()

    def delete(self):
        """Delete the object from the database and memcached"""
        DetachedORMObject.delete(self)
        self.delete_cached_instance()

    def get_instance_key(self):
        """Get the instance key, implimenting abstract method in base"""
        key = []
        for column in self._sa_instance_state.manager.mapper.primary_key:
            key.append('(' + str(getattr(self, column.key)) + ')')
        return ''.join(key)


