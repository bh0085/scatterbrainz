from SPARQLWrapper.SmartWrapper import SPARQLWrapper2

sparql = SPARQLWrapper2("http://dbtune.org/musicbrainz/sparql")

ambid = "5b11f4ce-a62d-471e-81fc-a69a8278c7da"
sparql.setQuery("""
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX mo: <http://purl.org/ontology/mo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mbart: <http://musicbrainz.org/artist/> 

SELECT *
WHERE
{
  ?artist rdf:type mo:MusicArtist ;
           mo:musicbrainz mbart:"""+ambid+""";
           rdfs:label ?label .
  ?madeby foaf:maker ?artist

}
limit 5
""")


results = sparql.query()
for r in results.bindings:
    for k in r.keys():
        print k,  r[k].value

