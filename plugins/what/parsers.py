from pyquery import PyQuery as pq
import what.webfuncs as webfuncs
import re

def parseTorrentPageToFiles(html):
    "Find and parse file lists"
    d = pq(html)
    fd_re =  re.compile('files_(\d*)')
    file_div_ids =list(re.finditer(fd_re,html))
    all_parsings = []
    for f in file_div_ids:
        t_grp_id = f.group(1)
        file_div_id = f.group()
        torrent_div = d("#torrent_"+t_grp_id);
        torrent_fl = torrent_div.find("#files_"+t_grp_id);
        parsed_fl = webfuncs.parseFileListToTracks(torrent_fl.html());
        all_parsings.append(parsed_fl)

    nums = webfuncs.parseAlbumInfoToTracks(html);
    all_parsings.append(nums);
    
    best_guess = webfuncs.mergeTracklists(all_parsings)
    return best_guess

def parseTorrentPageToTitle(html):
    import python_helpers as ph
    d = pq(html)
    h2_htmls = []
    a = d("h2").each(lambda x : h2_htmls.append(x.html()))
    title_re = re.compile('</a>\s*\-*\s*([^\[\-]*)')
    if len(h2_htmls) != 1: raise Exception("uh oh")
    title = re.search(title_re,h2_htmls[0]).group(1)
    title = ph.unescape(title)
    return title
               
