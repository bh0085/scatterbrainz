from SPARQLWrapper.SmartWrapper import SPARQLWrapper2
from rdflib import Namespace
from rdflib.Graph import Graph

def _getPrefixes():
    return """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX mo: <http://purl.org/ontology/mo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mbart: <http://musicbrainz.org/artist/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#>"""


def _getPrefixesDict():
    return dict(  foaf = Namespace("http://xmlns.com/foaf/0.1/"),
                  mo= Namespace("http://purl.org/ontology/mo/"),
                  rdfs= Namespace("http://www.w3.org/2000/01/rdf-schema#"),
                  rdf= Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
                  mbart= Namespace("http://musicbrainz.org/artist/") ,
                  owl= Namespace("http://www.w3.org/2002/07/owl#"))


def WikiFromArtistName(name =  '"Black Sabbath"'):
    sparql = SPARQLWrapper2("http://dbtune.org/musicbrainz/sparql")
    sparql.setQuery( _getPrefixes() + """
SELECT *
WHERE
{

  [] rdf:type mo:MusicArtist ;
          rdfs:label """+name+""";
          owl:sameAs ?same
  filter regex(str(?same), "edia")
}
limit 1
""")
    results = sparql.query()
    for r in results.bindings:
        for k in r.keys():
            dburi=r[k].value
            print DBPediaAbstract(dburi)
    
def dbpedia_from_MBID(ambid =  "5b11f4ce-a62d-471e-81fc-a69a8278c7da"):
    sparql = SPARQLWrapper2("http://dbtune.org/musicbrainz/sparql")

    sparql.setQuery( _getPrefixes() + """
SELECT *
WHERE
{

  [] rdf:type mo:MusicArtist ;
          mo:musicbrainz mbart:"""+ambid+""";
          owl:sameAs ?same;
 
  filter regex(str(?same), "edia")
}
limit 1
""")

    results = sparql.query()
    r = results.bindings[0]['same'].value
    return r

def DBPediaAbstract(uri = "http://dbpedia.org/resource/Black_Sabbath"):
    g = Graph()
    g.parse(uri)
    q = """
SELECT *
WHERE{
   ?s ?p ?o
}
limit 5
"""

    #now, just of the hell of it, print the entire tree:
    for s,p,o in g.triples((None,None,None)):
        print s, p, o
    
    import pdb
    pdb.set_trace()
    
    q1 = g.query('SELECT *  WHERE { ?s ?p ?o . }', 
                       initNs=_getPrefixesDict())
    for row in q1:
        print  row

    results = g.query(q)
    v = results.allVariables
    r_iter = results.result
    for r in r_iter:
        print r

    import pdb
    pdb.set_trace()
    return uri

def runTest():
    g = Graph()
    from rdflib import Namespace
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    g.parse("http://danbri.livejournal.com/data/foaf") 
    [g.add((s, FOAF['name'], n)) for s,_,n in g.triples((None, FOAF['member_name'], None))]
    import pdb
    pdb.set_trace()
    for row in g.query('SELECT * WHERE { ?a foaf:knows ?b . ?a ?cc ?aname . ?b ?dd ?bname . }', 
                       initNs=_getPrefixesDict()):
        print  row[0:1]
