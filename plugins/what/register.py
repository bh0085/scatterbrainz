#!/usr/bin/env python

print 'registering what.cd plugin'
import what as w

print '...configuring'
w.configure()
print '...initializing'
w.init()

import dbs.config.prefs as prefs
sb_user = prefs.readPref('what_sb_user')
w_user = prefs.readPref('what_user',sb_user)
print 'Success! set up what.cd pluging for ' +sb_user+' with what.cd account: ' + w_user 
exit(0)
