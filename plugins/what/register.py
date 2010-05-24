#!/usr/bin/env python

import dbs.config.queryConfig as qc
import os
import dbs.config.pluginConfig as pc
import config as wc
import whatdb as wd
from what.whathelpers import whatPlug

def register():

    print 'registering what.cd plugin'
    sb_dir = qc.query('scatterbrainz_dir')
    what_dir =os.path.join(sb_dir,'external/dbs/what')
    if not os.path.isdir(what_dir):
        os.mkdir(what_dir)
        
    print "Register what.cd for which SB user?"
    sb_user = raw_input('username: ')

    if pc.pluginRegistered('what',sb_user):
        print "Plugin already registered for " + sb_user
        print "... exiting"
        exit(1)
    

    print "\nWhat.cd username?"
    what_user = raw_input('username: ')
    print "\nWhat.cd password "
    what_pass = raw_input('password: ')
    

    print '...configuring'
    wc.configure(what_user,what_pass,what_dir,sb_user)
    print '...initializing'
    wc.init(sb_user)
    
    import dbs.config.prefs as prefs
    w_user = prefs.readPref('what_user',sb_user)
    print 'Success! set up what.cd pluging for ' +sb_user+' with what.cd account: ' + w_user 
    pc.register('what',sb_user)
    exit(0)

def unregister():
    print "Unregister what.cd for which SB user?"
    sb_user = raw_input('username: ')

    if not pc.pluginRegistered('what',sb_user):
        print "Plugin is not registered for user: " + sb_user
        print "...exiting"
        exit(1)

    plug = whatPlug(sb_user)
    dbfile = plug.whatDBFile()
    cookiefile = plug.whatCookieFile()
    if os.path.isfile(cookiefile):
        os.remove(cookiefile)
    os.remove(dbfile)
    wc.unconfigure(sb_user)
    pc.unregister('what',sb_user)


def usage():
    print '''Usage: catalog.py -opt
Options:
   -h: Prints help.
   -r: Register plugin.
   -u: Unregister plugin.
'''

import sys
import getopt

def main(argv):
    if len(argv) == 0:
        usage()
        sys.exit(1)
    try:  
        opts, args = getopt.getopt(argv, 'hur')
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)      
    for opt, arg in opts:  
        if opt == '-h':
            usage()
        elif opt == '-r':
            register()
        elif opt == '-u':
            unregister()
    sys.exit(0)


if __name__ == "__main__":
    exit(main(sys.argv[1:]))


