import postgresWrapper as pgwrap
import dbs.config.queryConfig as qc
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import pprint
import re
import itertools

ask_certain = True
ask_maybe = True
def mbrainz():
    mbhost = qc.query('mbhost')
    mbport = qc.query('mbport')
    mbdb = qc.query('mbdb')
    mbuser = qc.query('mbuser')  

    pgw = pgwrap.postgresWrapper(host = mbhost,
                                 port = mbport,
                                 db = mbdb,
                                 user = mbuser)
    return pgw

def tagDir():
    music_dir = qc.query('music_dir')
    pgw = mbrainz()

    ask_certain = True
    ask_maybe = True

    for base, dirs, files in os.walk(music_dir,followlinks = True):
        #automatically treat each directory as a cluster
        mut = []
        for f in files:
            ext = os.path.splitext(f)[-1]
            if ext == '.mp3': mut.append(MP3(os.path.join(base,f),ID3=EasyID3))

        artist_names = []
        album_names = []
        tracks = []
    
        if mut == []: continue
        for m in mut:
            for k, val in m.iteritems():
                if k == 'artist':
                    if not val[0] in artist_names:
                        artist_names.append(val[0])
                if k == 'album':
                    if not val[0] in album_names:
                        album_names.append(val[0])

            if 'tracknumber' not in m.keys():
                print 'Uh oh... track number is not in the key set.... skipping directory.'
                break
                
            if 'tracknumber' in m.keys() and 'title' in m.keys():
                num = m['tracknumber'][0]
                num_re = re.compile('^\W*\d*')
                num = re.search(num_re,str(num)).group()
                title = m['title'][0]
                length = m.info.length* 1000
                tracks.append({'mut':m,'number':num,'name':title,'length':length})

        ds = []
    
        print '\n\n\nTagging: ' + str(base) + '\n'
        print 'found artists:'
        pprint.pprint(artist_names)
        print 'and albums:'
        pprint.pprint(album_names)
        print '\n'

        for a in artist_names:
            for alb in album_names:
                d = pgw.queryToDict("""
select set_limit(.6);
select 
  artist.name as artist_name, 
  release_group.name as rg_name,
  album.name as album_name,
  album.gid as album_mbid,
  release_group.gid as rg_mbid,
  artist.gid as artist_mbid,
  track.gid as track_mbid,
  track.name as name,
  albumjoin.sequence as number,
  track.length as length
from artist, album, track, albumjoin, release_group
where artist.name %% %s
and release_group.artist = artist.id
and album.name %% %s
and release_group.id = album.release_group
and albumjoin.album = album.id
and albumjoin.track = track.id
limit 100;
""",params = (a,alb))
                ds.extend(d)

        #for each appearance of an artist or album in the current directory,
        #all possible matching releases have been accumulated into ds.

        #now, assume that each song in the current dwells within
        #the same release group and try to parse everything.


        if ds == []: 
            print '\n\nUh oh. \n \n Found no musicbrainz info....\n Continuing\n\n'
            continue
        rgs = []
        albs = []
        for k, g in itertools.groupby(ds, key = lambda x: x['rg_mbid']):
            items = list(g)
            rgs.append(items)
            for k2, g2 in itertools.groupby(items, key = lambda x:x['album_mbid']):
                i2 = list(g2)
                albs.append(i2)

        #the easiest case: finding an album match
        outcome = matchAlbum(tracks, albs)
                
    pgw.close()

import numpy as np
from numpy import array, zeros
import difflib

def matchAlbum(tracks, albums):

    fatal_flags = []
    warning_flags = []

    ntracks = len(tracks)
    
    trks = tracks
    amatched = albums

    l =len(amatched)
    for i in range(l):
        idx = l - i - 1
        a = amatched[idx]
        if len(a) != ntracks:
            amatched.pop(idx)


    nmeans = zeros(len(amatched))
    lmeans = zeros(len(amatched))
    nmins = zeros(len(amatched))
    all_sims = []

    namefun = lambda x: x['name']
    numfun = lambda x:int(x['number'])

    trks = sorted(trks,key =numfun)
    for a in amatched:
        
        a = sorted(a,
                   key = numfun)

    
    if tracks[0].has_key('number'):
        for j in range(len( amatched)):
            a = amatched[j]
            tnames = map(namefun, trks)
            anames = map(namefun,a)

            tlengths = map(lambda x:int(x['length']),trks)
            alengths = map(lambda x:int(x['length']),a)
            
            name_sims = getSimilarities(tnames,anames)
            length_sims = getSimilarities(tlengths,alengths)
            length_sims = np.divide(length_sims,10000)
            length_sims[np.where(length_sims > 1)] = 1
            length_sims = 1 - length_sims

            nmeans[j] = (name_sims.mean())
            lmeans[j] = (length_sims.mean())
            nmins[j] = (name_sims.min())
            all_sims.append({'name_sims':name_sims, 'length_sims':length_sims})

        bad = np.where(np.logical_or(nmeans < .6 ,lmeans < .6))[0]
        bad = sorted(bad, key = lambda x: -1* x)
        nmeans = np.delete(nmeans,bad)
        lmeans =np.delete(lmeans,bad)
        nmins = np.delete(nmins,bad)
        for b in bad:
            amatched.pop(b)
            all_sims.pop(b)

    if len(amatched) == 0:
        print 'Found no matching albums for current directory.'
        print
    elif len(amatched) == 1:
        print 'Everything seems pretty good! \n -One album found for the directory.'
        album = amatched[0]
        confirmMatch(trks,album, certain = True)              
    else:
        print 'Multiple matches found, disambiguating.'
        album = disambiguate(trks,amatched)
        confirmMatch(trks,album, certain = False)
def confirmMatch(trks,album, certain = False):
    ntracks = len(trks)
    old_names = map(lambda x:x['name'],trks)
    new_names = map(lambda x:x['name'],album)
    
    cw = 35
 
    print strfit('',15) + strfit('old_name',cw) + strfit('new_name',cw)
    for i in range(ntracks):
        trkstring=strfit('Track # '+str(i),15) + strfit(old_names[i],cw) + strfit(new_names[i],cw)
        print trkstring
    print
    if certain:
        print "We're pretty certain that this one is right - to toggle automatic tagging for similarly certain matches, type 'all-certain'"
    else:
        print "We're not completely sure that this one is right - to toggle automatic tagging for similarly likely matches, type 'all'"

    retry_count = -1
    while True:
        retry_count += 1
        
        
        global ask_certain
        global ask_maybe

        if not certain:
            if ask_maybe: 
                var =  raw_input('good? (y/n, default: y)')
            else:
                var = 'y'
        else:
            if ask_certain: 
                var =  raw_input('good? (y/n, default: y)')
            else:
                var = 'y'

        if var ==  'all-certain':
            var = 'y'
            ask_certain = False
        if var == 'all':
            var = 'y'
            ask_certain = False
            ask_maybe = False
        
        if var == 'y':
            for i in range(ntracks):
                m = trks[i]['mut']
                m['musicbrainz_trackid'] = album[i]['track_mbid']
                m['musicbrainz_albumid'] = album[i]['album_mbid']
                m['musicbrainz_artistid'] = album[i]['artist_mbid']
                m.save()
            print 'changes saved'
            break
        elif var == 'n':
            break
            print 'changes discarded'
        else:
            print 'input unrecognized...'
            print
        
def strfit(string, n):
    if not string:
        string = ''
    l = len(string)
    if l < n:
        strout = string + ' '*(n-l)
    elif l > n:
        strout = string[0:n]
    else:
        strout = string
    return strout
    
def getSimilarities(arr1,arr2):
    sims = zeros(len(arr1))
    if type(arr1[0]) == str or type(arr1[0]) == unicode:
        for i in range(len(arr1)):
            sm = difflib.SequenceMatcher()
            sm.set_seqs(arr1[i],arr2[i])
            sims[i] = sm.quick_ratio()
    if type(arr1[0]) == int:
        for i in range(len(arr1)):
            sims[i] = abs(arr1[i] - arr2[i])
    return sims
                
def disambiguate(trks,albums):
    namefun = lambda x: x['name']
    lengthfun = lambda x: int(x['length'])

    na = len(albums)
    name_scores = np.zeros(na)
    length_scores = np.zeros(na)
    pop_scores = np.zeros(na)

    for j in range(na):
        a = albums[j]
        anames =map(namefun, a) 
        tnames =map(namefun, trks)
        name_sims = (getSimilarities(anames,tnames))
        name_scores[j] = name_sims.mean()

    s = sorted(name_scores, key = lambda x:-1*x)
    name_gap = s[0] - s[1]
        
    for j in range(na):
        a = albums[j]
        alengths =map(lengthfun, a) 
        tlengths =map(lengthfun, trks)
        length_sims = getSimilarities(tlengths,alengths)
        length_sims = np.divide(length_sims,10000)
        length_sims[np.where(length_sims > 1)] = 1
        length_sims = 1 - length_sims
        length_scores[j] = length_sims.mean()

    s = sorted(length_scores, key = lambda x:-1*x)
    length_gap = s[0] - s[1]

    for j in range(na):
        a = albums[j]
        mbid = a[0]['album_mbid']
        pgw = mbrainz()
        d = pgw.queryToDict("""select 
count(l_album_artist.id) as count
from l_album_artist, album 
where album.gid = %s
and l_album_artist.link0 = album.id ;
""",params = [mbid])
        nalb_rel = d[0]['count']
        pop_scores[j] = nalb_rel
        pgw.close()

    pop_scores = pop_scores / pop_scores.max()
    s = sorted(pop_scores, key = lambda x:-1*x)
    pop_gap = s[0] - s[1]

    points = zeros(na)
    points[(np.where(pop_scores == pop_scores.max()))] += pop_gap
    points[(np.where(length_scores == length_scores.max()))] += length_gap
    points[(np.where(name_scores == name_scores.max()))] += name_gap
    
    print str(na) + ' albums match the current directory.'
    print 'Disambiguation matrix: '
    print points
    print

    return albums[np.where(points == points.max())[0]]
