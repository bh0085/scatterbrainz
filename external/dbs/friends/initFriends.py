import sys
def usage():
    print 'acceptable args: help, reset-all, reset-meta'

def main(argv):
    import os
    import dbs.config.queryConfig as qc
    import sqliteWrapper as swrap
    import getopt

    do_reset = False
    try:  
        opts, args = getopt.getopt(argv, '',['reset-all','help'])
    except getopt.GetoptError, e:
        print e
        usage()                         
        sys.exit(2)      
    for opt, arg in opts:  
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit()                  
        elif opt == '--reset-all':
            do_reset = True
 

    friends_dir = qc.query('friends_dir')
    dbfile = qc.query('friends_dbfile')
    sqw = swrap.sqliteWrapper(dbfile)

    if do_reset:
        d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
        print 'Resetting all friends tables'
        for table in d:
            sqw.query("""drop table '""" + table['name'] + """';""")

    d = sqw.queryToDict('''select name from sqlite_master where type = 'table';''')
    if not 'known' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE known(
      id INTEGER PRIMARY KEY,
      address TEXT UNIQUE,
      pg_port INTEGER, 
      sb_port INTEGER
);
    ''')

    if not 'friends' in map(lambda x: x['name'],d):
        sqw.query('''
    CREATE TABLE friends(
      id INTEGER PRIMARY KEY,
      known INTEGER NON NULL UNIQUE,
      FOREIGN KEY(known) REFERENCES known(id)

);
    ''')



if __name__ == "__main__":
    exit(main(sys.argv[1:]))

exit(1)

                                   
