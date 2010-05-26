import logging
from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn
from scatterbrainz.lib.base import BaseController, render

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import os
import re
import itertools

import urllib
import simplejson as sjson

log = logging.getLogger(__name__)

import sb_helpers as sh
import dbs.requests.request as db_req


class GetsbController(BaseController):
    cxn = None
    #Query the centralized scatterbrainz DB
    #For now, should call _cursor and close the cursor manually when done.

    def index(self):
        return render('/rosa_template.html')

    def parseSources(self,p):
        sources = [];
        for k in p.keys():
           if k[0:6] == 'source':
                if not sources: sources = []
                sources.append( p[k] )
        return sources
            
    def parseFilters(self,p):
        filters = {}
        for k in p.keys():
            if k[0:6] == 'filter':
                r = re.compile("\[(.*)\]$")
                match = re.search(r,k).group(1)
                filters[match] = p[k]
        return filters

    
    #fetch3 uses memcached for requests...
    @authorize(RemoteUser())
    def fetch2(self):
        uname = sh.unameFromCookie(request.cookies['authkit'])
        
        p = request.params
        sources = self.parseSources(p)
        filters = self.parseFilters(p)
        action = p['action']
        
        data_arr = []
        for s in sources:
            req = None
            if s== 'remote': db = 'mbrainz'
            elif s == 'local': db = 'music'
            elif s == 'what': db = 'what'
            else: raise Exception('data source unhandled')
            db_params = {'action':action,'src':s}
            for key, item in filters.iteritems():
                db_params[key]=item
            #memcaching disabled (since, true)
            req = db_req.requestWithParams(uname,db,db_params,True)
            if not req: continue
            for r in req: r['source'] = s
            data_arr.extend(req)

        if len(data_arr) == 0:
            return None
        dt = data_arr[0]['datatype']
        if ( dt =='artist' or dt =='track'):
            mbstr = dt + "_mbid"
            data_arr = mergeDict(data_arr, mbstr)

        has_year = False
        for i in data_arr: 
            if i.has_key('year'): 
                has_year = 'True';
                break;
        #if has_year: data_arr = mergeDict(data_arr,'year')

        createAllStrs(data_arr,['set_to_merge']);
        getSBSortData(data_arr)
        return sjson.dumps(data_arr)
            
    def fetch3(self):
        import dbs.mbrainz.fetchMB as fr
        import dbs.music.fetchMusic as fm
        p = request.params
        sources = self.parseSources(p)
        filters = self.parseFilters(p)
        action = p['action']

        data_arr = []
        for s in sources:
                req = None
                if s == 'remote':
                    src_module = fr
                elif s =='local':
                    src_module = fm
                    
                if action == 'albums':
                    dt = 'album'
                    tryfilter = 'artist_mbid'
                    if req == None and tryfilter in filters.keys():
                        req = src_module.getMBIDArtistAlbums(filters[tryfilter])
                    if req == None:
                        req = src_module.getAllAlbums()   
 
                elif action =='artists':
                    dt = 'artist'
                    req = src_module.getAllArtists();

                elif action =='members':
                    dt = 'artist'
                    tryfilter = 'album_mbid'
                    if req == None and tryfilter in filters.keys():
                        req = src_module.getMBIDAlbumMembers(filters[tryfilter])
                    tryfilter = 'artist_mbid'
                    if req == None and tryfilter in filters.keys():
                        req = src_module.getMBIDArtistMembers(filters[tryfilter])
                    if req == None:
                        req = src_module.getAllMembers()                   

                elif action =='tracks':
                    dt = 'track'
                    tryfilter = 'album_mbid'
                    if req ==None  and tryfilter in filters.keys():
                        req = src_module.getMBIDAlbumTracks(filters[tryfilter])
                    tryfilter = 'artist_mbid'
                    if req == None and tryfilter in filters.keys():
                        req = src_module.getMBIDArtistTracks(filters[tryfilter])
                    if req == None:
                        req = src_module.getAllTracks()
                if not req: continue
                for r in req: r['source'] = s
                for r in req: r['datatype'] = dt
                for r in req: r['action'] = action
                data_arr.extend(req)
                
        if ( dt =='artist' or dt =='track'):
            mbstr = dt + "_mbid"
            data_arr = mergeDict(data_arr, mbstr)

        has_year = False
        for i in data_arr: 
            if i.has_key('year'): 
                has_year = 'True';
                break;
        if has_year: data_arr = mergeDict(data_arr,'year')

        createAllStrs(data_arr,['set_to_merge']);
        getSBSortData(data_arr)
        return sjson.dumps(data_arr)


#data manipulation for easy display.
def mergeDict(dat_in, merge_key,unique_key = None,errors = 'replace'):

    merged_dat = dat_in
    try:
        get_key = (lambda x :  (x[merge_key]))
        merged_dat.sort(key = get_key)
    except Exception, e:
        if errors == 'strict':
            raise Exception(e)
        if errors == 'eliminate':
            merged_dat = list(itertools.ifilter(lambda x : x.has_key(merge_key), merged_dat))
            merged_dat.sort(key = get_key)
        if errors == 'replace':
            for elt in merged_dat:
                if not elt.has_key(merge_key):
                    elt[merge_key] = '0000 (Some Local Data Lacks Release Yr?)'
            merged_dat.sort(key = get_key)



    group_list = []
    for k, items in itertools.groupby(merged_dat, key = get_key):
        group_list.append(list(items))  

    data = [];
    for g in group_list:
        entry = {};    
        entry['locations'] = []
        entry['elements'] = []
        entry['merges'] = [merge_key]
        for sub in g:
            if not sub.has_key('elements'):
                entry['elements'].append(sub)

            for k, item in sub.iteritems():
                #treat the source key as a special case
                if k == 'source':
                    entry['locations'].append(sub[k])
                    continue
                

                #check if key is set.
                if k in entry.keys(): 
                    if item.__class__==list and entry[k].__class__  == list:
                        entry[k].extend(item)

                    else:
                        pass
                else:
                    entry[k] = item;
        data.append(entry);
    return data;

def createAllStrs(data,opts = []):
    for d in data:
        makeDataString(d,opts)
        if d.has_key('elements'):
            for e in d['elements']:
                makeDataString(e,opts)
        
def createStrs(data,opts = []):
    for d in data:
        makeDataString(d,opts)
    

def makeDataString(d, opts = []):
    dt = d['datatype']
    strval = u''

    if dt == 'artist':
        strval = strval + d['name']
    elif dt=='album':
        strval = strval + d['name']
        if 'year' in d.keys(): strval = d['year'] +" - "+ strval
    elif dt=='track':
        strval = strval + d['name']
    elif dt=='member':
        strval = strval + d['name']
    else:
        strval = strval + d['name']

    if 'append_src' in opts:
        strval = "Source: " +d['source'] + " " + strval  
    if 'append_dt' in opts:
        strval = strval + d['datatype']
    if 'set_to_merge' in opts:
        if d.has_key('merges'):
            last_merge = d['merges'][0]
            if (last_merge == 'year'):
                strval = d['year'] +" - " + d['name']

    if strval == '' :
        strval = 'blank'

    d['tostring'] = strval   


    
def getSBSortData(data,sort_key = None):
    if sort_key == None:
        sort_key = 'tostring'
        
    #this line just corrects for bad encodings... not sure where they are coming from.
    get_key = lambda x :x[sort_key].__class__ == unicode and x[sort_key] or unicode(x[sort_key],'utf-8')
    data.sort(key = get_key)
    


