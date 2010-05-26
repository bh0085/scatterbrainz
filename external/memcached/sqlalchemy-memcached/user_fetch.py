#!/usr/bin/python
"""
Fetches and prints the user data by user_id ensuring it hits memcached
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

from database import *
from user_classes import *

if __name__ == '__main__':

    for id in (1, 2, 3):
        user = User.fetch_by_field(User.user_id, id)
        if (user is not None):
            print user.name, user.email, user.password, user.user_status.name

    print 'memcached calls:', MEMCACHED_CLIENT.stats

