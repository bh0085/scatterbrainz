from rdflib.Graph import Graph
import re

def getURILabel(uri):
    rdfs="http://www.w3.org/2000/01/rdf-schema#"
    g = Graph()
    g.parse(uri)
    for s, p, o in g.triples((None,None,None)):
        if re.search(re.compile(rdfs+".*label",re.I),p):
            return o
    return "No URILABEL Found"

