#!/usr/bin/python
"""
Fetches each of the users by name, bypassing the primary key cache and
repopulating memcached.  Important to run after rerunning user_classes.py
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

    for name in ('John', 'Jane', 'wordpress'):
        user = User.fetch_by_field(User.name, name)

    print 'memcached calls:', MEMCACHED_CLIENT.stats

