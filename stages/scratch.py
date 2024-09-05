import biobricks as bb, pandas as pd
from rdflib import Graph, Namespace
from rdflib.plugins.stores import sparqlstore
from rdflib_hdt import HDTStore
import pandas as pd

eutoxrisk = bb.assets('eutoxrisk')

pathways = pd.read_parquet(eutoxrisk.pathways_parquet)
overview = pd.read_parquet(eutoxrisk.overview_parquet)
temposeq = pd.read_parquet(eutoxrisk.temposeq_parquet)

pathways.head()
overview.head()
temposeq.head()


overview.columns

overview.iloc[0]

# region transform the pathways parquet
# 1. use geneontology that wikipathway uses?
# 2. use pathways from wikipathways
# 3. 

wikipathways = bb.assets('wikipathways')

# Create a Graph with HDTStore
store = HDTStore(wikipathways.wikipathways_hdt)
g = Graph(store=store)

# SPARQL query with explicit namespace definitions
query = """
PREFIX wp: <http://vocabularies.wikipathways.org/wp#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX purl: <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?pathway_label (STR(?gene_label) AS ?geneProduct) WHERE {
    ?geneProduct a wp:GeneProduct . 
    ?geneProduct rdfs:label ?gene_label .
    ?geneProduct dcterms:isPartOf ?pathway .
    ?pathway a wp:Pathway .
    # ?pathway dcterms:identifier "WP1560" .
    ?pathway purl:title ?pathway_label .
} LIMIT 10
"""

# Execute the query
results = g.query(query)
df = pd.DataFrame(results, columns=['pathway', 'geneProduct'])
store.close()

df

# endregion
# 