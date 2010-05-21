import re
import urllib
import pdb
import MultipartPostHandler, urllib2, cookielib
from metatorrent import decode
from pyquery import PyQuery as pq
from whatOpener import whatOpener
import itertools
import pprint

def submitlog():

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                  MultipartPostHandler.MultipartPostHandler)
    p0 = { "username" : "bh0085", "password" : "dinobot1w"}
    logfile="/Users/bh0085/Music/Rips/Finished/Rahsaan Roland Kirk - Simmer, Reduce, Garnish, & Serve - (1995) [FLAC]/Simmer, Reduce, Garnish & Serve.log"
    p1 = { "action" : 'takeupload', 'log':open(logfile, "rb") }

    f0 = opener.open("http://what.cd/login.php",p0)
    f1a = opener.open("http://what.cd/logchecker.php")
    f1 = opener.open("http://what.cd/logchecker.php", p1)

    d0 = f0.read()
    d1a = f1a.read()
    d1 = f1.read()

    file0= open('what0.html','w')
    file1a= open('what1a.html','w')
    file1= open('what1.html','w')
    file0.write(d0)
    file1a.write(d1a)
    file1.write(d1)

def readartist():

    url = u'http://what.cd/artist.php?id=224'
    wo = whatOpener()
    o = wo.opener()

    # second request should automatically pass back any
    # cookies received during login... thanks to the HTTPCookieProcessor

    return torrentinfo(0,o)

  
    f = o.open( url )
    data = f.read()
    uni = unicode(data,'utf-8')    
    f.close()

    ##Can open the page with libxml2dom
    import libxml2dom
    doc = libxml2dom.parseString(data, html=1)

    ##can open with lxml
    from lxml import etree
    #tree = etree.fromstring(uni)

    d = pq(uni);
    
    htmls = []
    logged = []
    import re
    relog = re.compile("Log")
    elts =  d("#torrents_album").find("td").find("a").filter(lambda i : pq(this).html() != None).filter(lambda i : re.search(relog,pq(this).html()) != None)
    elts.each(lambda x : (   logged.append((x))))

    for f in logged:
        s = f.attr('href');
        t_id = re.compile("[^t]id=([0-9]*)").search(s).group(1)
        t_grp_id = re.compile("torrentid=([0-9]*)").search(s).group(1)
        
        i = getinfo(t_id,o)
        break
        logfile = retrievelog( t_id, t_grp_id, o)
        if logfile != None:
            tracks = getlogtracks(logfile)
            #print tracks
    
def increasingSequences(arr, max_inc = 1):
    
    big_arr = []
    last_num = None
    current_list = None
    arr2 = []
    for item in arr:
        arr2.append((item, len(arr2)))

    for item in arr2:
        num = item[0]
        if last_num ==None:
            last_num  = num
            current_list = [item]
        elif num > last_num and num <= last_num +max_inc:
            last_num = num
            current_list.append(item)
        else:
            big_arr.append(current_list)
            last_num = num
            current_list = [item]

    big_arr.append(current_list)
    return big_arr

def searchTermsToWhat(terms):
    tstring = str.join('+',terms)
    url = 'http://what.cd/torrents.php?order_way=desc&order_by=seeders&searchstr=' + tstring
    wo = whatOpener()
    o = wo.opener()
    text = o.open(url).read()
    d = pq(text)
    torrents = []

    #print 'hi'
    #print text

    d('.torrent_table').find("a").filter(lambda i : pq(this).attr('title') == 'View Torrent').each(lambda i:torrents.append(i))


    all_outs = {}
    for t in torrents:
        match = re.compile("\d+").search(t.attr('href'))
        if match == None:
            continue
        ti = torrentinfo(match.group(),o)
        all_outs[match.group()] = ti

    return all_outs
    


def torrentinfo(t_id,opener):
    url = 'http://what.cd/torrents.php?id='+t_id
    text = opener.open(url).read()
    d = pq(text)
    fd_re = re.compile('files_(\d*)')
    file_div_ids =list(re.finditer(fd_re,text))

    all_parsings = []
    for f in file_div_ids:
        t_grp_id = f.group(1)
        file_div_id = f.group()
        torrent_div = d("#torrent_"+t_grp_id);
        torrent_fl = torrent_div.find("#files_"+t_grp_id);
        parsed_fl = parseFileListToTracks(torrent_fl.html());
        all_parsings.append(parsed_fl)

    nums = parseAlbumInfoToTracks(text);
    all_parsings.append(nums);
    
    best_guess = mergeTracklists(all_parsings)
    return best_guess

    

def map_number(num):
    starttype = type(num)
    num_maps={
        'one':1,
        'two':2,
        'three':3,
        'four':4,
        'i':1,
        'ii':2,
        'iii':3,
        'iv':4
        }    
    if str.lower(str(num)) in num_maps.keys():
        return starttype(num_maps[str.lower(str(num))])
    return num
def mergeTracklists(parsings):

    #get the most common disc listing
    disc_seqs = []
    count = -1 
    for p in parsings:
        count += 1
        if not p: continue
        this_seq = sorted(p.keys())
        if len(disc_seqs) == 0 or (not this_seq in map(lambda x: x[0], disc_seqs)):
            disc_seqs.append([this_seq, 1,[count]])
        else:
            mapped = map(lambda x: x[0],disc_seqs)
            idx =mapped.index(this_seq)
            disc_seqs[idx][1] += 1
            disc_seqs[idx][2].append(count)


    if disc_seqs == []:
        return None
    
    disc_seqs = sorted(disc_seqs, key = lambda x: -1*x[1])
    best_seq = disc_seqs[0]
    matching_parsings = best_seq[2]

    #from the subset of discs matching the best listing, get the most common track listing
    trk_counts = []
    matched_parsings = []
    count = -1
    for m in matching_parsings:
        count +=1
        p = parsings[m]
        this_seq = []
        matched_parsings.append(p)
        for k in sorted(p.keys()):
            this_seq.append(len(p[k]['number']))

        if len(trk_counts) == 0 or (not this_seq in map(lambda x: x[0], trk_counts)):
            trk_counts.append([this_seq, 1,[count]])
        else:
            mapped = map(lambda x: x[0],trk_counts)
            idx =mapped.index(this_seq)
            trk_counts[idx][1] += 1
            trk_counts[idx][2].append(count)

    trk_counts = sorted(trk_counts, key = lambda x: -1*x[1])
    best_count = trk_counts[0]
    matching_parsings = best_count[2]
    
    final_parsings = []
    best_parsing = None
    # now try to return the parsing with the most information.
    for m in matching_parsings:
        p = matched_parsings[m]
        final_parsings.append(p)
        if p[p.keys()[0]]['time'][0] != None:
            #if you find time, return immediately.
            best_parsing = p

    #return the parsing with the most data and all other qualified ones.
    return (best_parsing,final_parsings)
   
        
    
        



            




def parseFileListToTracks(fl):
    ext_re =re.compile("\.mp3|\.flac")
    this_tracklist = []
    fname_re = re.compile("<td>([^<]*)</td>");
    trks = list(re.finditer(fname_re,fl))
    for elt in trks:
        txt = elt.group(1)
        result = re.search(ext_re,txt)
        if result != None:
            this_tracklist.append(txt)
    if this_tracklist == []: return None
    parsed_txt = parseStrArrToTracks(this_tracklist)
    return parsed_txt
def parseStrArrToTracks(arr, no_retry = False):
    stats = []
    dc_fails = False
    tc_fails = False
    dm_fails = False
    tm_fails = False
    for item in arr:

        this_stat = {}
        init_str= item
        this_stat['text'] = init_str
        item = '/' + item
        dashes = list(re.finditer(re.compile('-'),item))
        this_stat['dashes'] = (dashes != None and len(dashes)) or (None) 
        match = re.search(re.compile('(dis[kc]|cd)\W*(?P<disc>[0-9]+|one|two|three|four|[IV]+)\W+((?P<track>[\d]{1,2})[^\d]){0,1}',re.I), item)  
        this_stat['disc_certain'] = (match != None and match.group('disc')) or (None)
        this_stat['track_certain'] = (match != None and match.group('track')) or (None)
        match = re.search(re.compile('/\W*((?P<disc>[0-9]+)\W+)*((?P<track>[\d]{1,2})[^\d])'),item)
        this_stat['disc_maybe'] =(match != None and match.group('disc')) or None
        this_stat['track_maybe'] =(match != None and match.group('track')) or None
        match = re.search(re.compile('(\d+:\d+)'),item)
        this_stat['time']= (match != None and match.group()) or None
        
        dc_fails = dc_fails or (this_stat['disc_certain'] == None)
        tc_fails = tc_fails or (this_stat['track_certain'] == None)
        dm_fails = dm_fails or (this_stat['disc_maybe'] == None)
        tm_fails = tm_fails or (this_stat['track_maybe'] == None)
        stats.append(this_stat)

    if not (dc_fails or dm_fails):
        raise Exception()

    if (not no_retry) and tm_fails and tc_fails:
        #check to see if maybe some of the lines work by searching for increasing sequences
        #in the tracks where numbering did work.
        lm = lambda x:x['track_maybe']
        lc = lambda x:x['track_certain']
        tmc = len(list(itertools.ifilter(lambda x: lm(x) != None,stats)));
        tcc = len(list(itertools.ifilter(lambda x: lc(x) != None,stats)));
        
        if tmc == 0 and tcc == 0: return None
        tfun = (tcc >= tmc and lc) or (lm) 
        trks = map(tfun, stats)
        
        nums = []
        for t in trks:
            try: 
                nums.append(int(t))
            except:
                nums.append(-1)
        inc_nums = increasingSequences(nums)
        seq_good = []
        for seq in inc_nums:
            if seq[0][0] == 1 and seq[-1][0] > 1: 
                seq_good.extend(map(lambda x: x[1],seq))
        
        redo_tracks = []
        for idx in seq_good:
            redo_tracks.append(arr[idx])
        
        return parseStrArrToTracks(redo_tracks, no_retry = True)
        
    if not dc_fails:
        discfun = lambda x: map_number(x['disc_certain'])
    elif not dm_fails:
        discfun = lambda x: map_number(x['disc_maybe'])
    else:
        discfun = lambda x: 0


    if not tc_fails:
        track_fun = lambda x: x['track_certain']
    elif not tm_fails:
        track_fun = lambda x: x['track_maybe']
    else:
        track_fun = lambda x: 0
    

    disc_list = {}
    for k, items in itertools.groupby(stats, key = discfun):
        item_l = list(items)
        disc_list[k]={}
        disc_list[k]['number'] = map( track_fun, item_l)
        disc_list[k]['text'] = map( lambda x : x['text'], item_l)
        disc_list[k]['time'] = map( lambda x : x['time'], item_l)

    return disc_list
def parseAlbumInfoToTracks(text):
    d = pq(text)
    infos = []
    infodiv = d("div").filter(".box").each(lambda x : infos.append(x));
    ai_re = re.compile("^ *album *info",re.I | re.M)

    tracks = []
    disc_switch = None
    for i in infos:
        match =  re.search(ai_re,i.text())
        if match: 
            h0 = i.html()
            h0 = re.sub(re.compile("<br[^>]*>"),'\n',h0);
            h0 = re.sub(re.compile("<[^>]*>"),'',h0);
            elts = re.split("\n",h0)
            for e in elts:
                disc_re = re.compile("(dis[kc]|cd)\W*\d+",re.I)
                disc_match = disc_re.search(e)
                if disc_match != None:
                    disc_switch = disc_match.group()

                track_re = re.compile("^\W*([0-9]+).*$",re.M);
                match = (re.search(track_re,e))
                if match != None:
                    s = match.group();
                    if disc_switch != None: s = disc_switch + " aa /" + s
                    tracks.append(s)
            break

    if tracks == []: return None
    parsed = parseStrArrToTracks(tracks)
    return  parsed
            
def retrievelog(t_id, t_grp_id,opener):
    loglink = 'http://what.cd/torrents.php?action=viewlog&torrentid='+t_grp_id+'&groupid='+t_id
    print loglink
    text = opener.open(loglink).read()
    log_re = re.compile('<pre[^>]*>(.*)</pre',re.M | re.DOTALL)
    match = list(re.finditer(log_re,text))
    
    logs = []
    for m in matches:
        logs.append(m.group(1))

def getlogtracks(logfile):
    first_line_re =re.compile(".{100}", re.DOTALL)
    row_re = re.compile("\|.*")
    track_re = re.compile("track\s*(\d+)",re.I)
    flmatch = re.search(first_line_re,logfile)
    track_matches = re.finditer(track_re,logfile)
    track_nums = []
    if track_matches:
        for t in track_matches:
            gp = int(t.group(1))
            if not gp in track_nums:
                track_nums.append(gp)
    track_nums.sort()

    print track_nums
#return match.group()
    


#   #or with pyquery
#
#   m2 = re.findall(re.compile('table.*?<(?=/table).{5}',re.S),uni)[0]
#   rerelease = re.compile(u'<strong>([0-9]{4}).*?>(.*?)<',re.S)
#   resplit = re.compile(u'<strong>[0-9]{4}.*?>.*?<',re.S)
#   releases = re.finditer(rerelease,m2)
#   splits = re.split(resplit,m2)
#   splits = splits[1:len(splits)]
#   titles = []
#   years = []
#   infos = []
#
#   for sub in splits:
#       try:
#           release= releases.next()
#       except StopIteration:
#           break
#       year = release.group(1)
#       title = release.group(2)
#       titles.append(title)
#       years.append(year)
#       torrents = re.finditer(re.compile('href="(.*?)".*?title="Download"'),sub)
#       info = []
#       while 1:
#           try:
#               torrent = torrents.next()
#               dlurl = 'http://what.cd/'+torrent.group(1)          
#               dlurl = re.sub(re.compile('&amp;'),'&',dlurl)
#               opened = o.open( dlurl )
#               r = opened.read()
#               t = decode(r)
#               names = []
#               lengths = []
#               for file in t["info"]["files"]:
#                   names.append("/".join(file["path"]))
#                   lengths.append(file["length"])
#                   
#               info.append({'names':names,'lengths':lengths})   
#           except StopIteration:
#               break
#       infos.append(info)
#
#   pdb.set_trace()
