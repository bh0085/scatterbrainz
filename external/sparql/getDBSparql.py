from SPARQLWrapper.SmartWrapper import SPARQLWrapper2
import getDBRDF

def WikiFromArtistName(name =  '"Black Sabbath"'):
    sparql = SPARQLWrapper2("http://dbtune.org/musicbrainz/sparql")

    sparql.setQuery("""
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX mo: <http://purl.org/ontology/mo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mbart: <http://musicbrainz.org/artist/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT *
WHERE
{
  ?artist rdf:type mo:MusicArtist ;
          rdfs:label """+name+""" .
  ?artist  owl:sameAs ?same

}
limit 1
""")
    results = sparql.query()
    
    import re
    repedia = re.compile("dbpedia")

    for r in results.bindings:
        for k in r.keys():
            if re.search(repedia,r[k].value):
                dburi=r[k].value
                print getDBRDF.DBPediaAbstract(dburi)
    

def WikiFromMBArtist(ambid =  "5b11f4ce-a62d-471e-81fc-a69a8278c7da"):
    sparql = SPARQLWrapper2("http://dbtune.org/musicbrainz/sparql")

    sparql.setQuery("""
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX mo: <http://purl.org/ontology/mo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mbart: <http://musicbrainz.org/artist/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT *
WHERE
{
  ?artist rdf:type mo:MusicArtist ;
           mo:musicbrainz mbart:"""+ambid+""";
           rdfs:label ?label .
  ?artist  owl:sameAs ?same

}
limit 5
""")
    results = sparql.query()
    
    import re
    repedia = re.compile("dbpedia")

    for r in results.bindings:
        for k in r.keys():
            if re.search(repedia,r[k].value):
                dburi=r[k].value
                print getDBRDF.DBPediaAbstract(dburi)
    

