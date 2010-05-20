import dbs.config.queryConfig as qc
import urllib2
def sb_root_url():
    addr = qc.query('sb_address')
    port = qc.query('sb_port')
    url ="http://"+str(addr)+":"+str(port)
    return url


def queryLocalSB(rel):
    address = sb_root_url()+rel
    o = urllib2.build_opener()
    data = o.open(address).read()
    return data
    
