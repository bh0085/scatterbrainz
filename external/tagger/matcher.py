import mbrainzWrapper as mbw
import re
import pprint

import unicodedata
def strip_accents(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def tokenize(s):
    s = unicode(s)
    stripped = strip_accents(s)
    stripped = re.compile(u"'").sub(u'',stripped)
    stripped = stripped.lower()
    tokens = unicode.split(stripped,u" ")
    try:
        tokens.remove('')
    except: pass

    return tokens

def wordUseCount(word,use_type,wrapper):
    "given a preexisting db connection, ask how many times a word occurs in the database in a given context"
    if use_type =='artist':
        d = wrapper.queryToDict("""
select artistusecount as count
from wordlist
where word = %(word)s;""",{'word':word})
    elif use_type =='album':
        d = wrapper.queryToDict("""
select albumusecount as count
from wordlist
where word = %(word)s;""",{'word':word})
    elif use_type =='track':
        d = wrapper.queryToDict("""
select trackusecount as count
from wordlist
where word = %(word)s;""",{'word':word})
    else:
        raise Exception("Unhandled use type")
    if len(d) == 0:
        return 0
    else:
        return d[0]['count']

def _artistMatchFromTokens(tokens):
    m = mbw.mbrainzWrapper()
    pops = []
    entries = []

    for t in tokens:
        pops.append((t,wordUseCount(t,'artist',m)))
    tokens_s = sorted(pops, key = lambda x: x[1])
    for i in range(len(tokens_s)):
        word = tokens_s[i][0]
        if i == 0:
            m.query("""
create temporary table matched_artists as
select artist.id as art_id, artist.name as art_name, artist.gid as gid
from artist, artistwords, wordlist
where artistwords.artistid = artist.id
and artistwords.wordid = wordlist.id
and wordlist.word = %(word)s;
""",
                    {"word":word})
        else:
            m.query("""
delete
from matched_artists
using
(select count( wordid ), art_name
from
  ( 
  select *
  from 
  matched_artists 
  LEFT OUTER JOIN 
      (select * 
           from artistwords RIGHT JOIN wordlist
                          ON ( artistwords.wordid = wordlist.id)  
                          where word = %(word)s ) as firstjoin
   
   ON ( art_id = artistid )
  ) as joined
group by art_name) as counted
where counted.count = 0
and counted.art_name = matched_artists.art_name
""",
                    {'word':word})

    d = m.queryToDict("select * from matched_artists")  
    m.close()
    entries.extend(d)   
    return entries

def matchArtistString(artist):
    
    matchType= 'fast'
    if matchType == 'fast':
        tokens = tokenize(artist)
        matches = _artistMatchFromTokens(tokens)
    elif matchType == 'trgm':
        m = mbw.mbrainzWrapper()
        match_limit = .4     
        d = m.queryToDict("""
select set_limit( .6 );
select gid, id, name
from artist
where name %% %(artist_name)s;
""",{'match_limit':match_limit,'artist_name':artist})
        m.close()
        matches = d
    
    return matches

def matchTrackListWithArtistMBIDAndGroupName(tracks,artists):
    pass
