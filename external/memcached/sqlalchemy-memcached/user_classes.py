#!/usr/bin/python
"""
User Database Classes
Impelements two tables, user and user_status, in an SQLLite database.
If executed, it will delete and repopulate the database.
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

import database

from sqlalchemy import *
from sqlalchemy.orm import *

ENGINE = create_engine('sqlite:///example.db', echo=True)

METADATA = MetaData()
METADATA.bind = ENGINE

SESSION = sessionmaker()

class UserStatus(object):
    def __init__(self, name):
        self.name = name

UserStatusTable = Table('user_status', METADATA, \
    Column('user_status_id', Integer, primary_key=True),
    Column('name', String)
)
UserStatusTable.mapper = mapper(UserStatus, UserStatusTable)
UserStatusTable.mapper.compile()


class User(database.MemcachedORMObject):
    def __init__(self, name, email, password, user_status_id):
        self.name = name
        self.email = email
        self.password = password
        self.user_status_id = user_status_id

UserTable = Table('user', METADATA, \
    Column('user_id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
    Column('password', String),
    Column('user_status_id', Integer),
    ForeignKeyConstraint(['user_status_id'], ['user_status.user_status_id'])
)
UserTable.mapper = mapper(User, UserTable, \
    properties = { 'user_status': relation(UserStatus, lazy=False)})
UserTable.mapper.compile()


if __name__ == "__main__":
    #Recreate the database and tables
    METADATA.drop_all()
    METADATA.create_all()

    session = SESSION()

    #Create the user statuses
    active = UserStatus('active')
    session.add(active)
    inactive = UserStatus('inactive')
    session.add(inactive)
    session.commit()

    #Create the users
    user1 = User('John', 'john.hoff@braindonor.net', 'p4ssw0rd', active.user_status_id)
    session.add(user1)
    user2 = User('Jane', 'jane.doe@braindonor.net', 'n0p4ss', inactive.user_status_id)
    session.add(user2)
    user3 = User('wordpress', 'wordpress@braindonor.net', 'blogit', active.user_status_id)
    session.add(user3)
    session.commit()

    session.close()

