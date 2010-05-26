import pprint
def pp(inp):
    pprint.pprint(inp);

def unescape(s):
     s = s.replace("&lt;", "<")
     s = s.replace("&gt;", ">")
     # this has to be last:
     s = s.replace("&amp;", "&")
     return s
