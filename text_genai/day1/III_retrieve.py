from whoosh import index, scoring
from II_index import index_dir
from whoosh.qparser import MultifieldParser, OrGroup, AndGroup, FuzzyTermPlugin, PhrasePlugin

# Load your index here
ix = index.open_dir(index_dir)
queries = [
    "heart attack diabetes",                                       # normal
#    "\"heart attack\" diabetes",                                   # phrase
#    "heart attack~ diabetes",                                      # fuzzy

    "myocardial infarction diabetes",                              # normal
#    "\"myocardial infarction\" diabetes",                          # phrase
#    "myocardial infarction~ diabetes",                             # fuzzy

#    "(\"heart attack\" OR \"myocardial infarction\") diabetes",    # synonyms
]
modes = ["OR", "AND"]
weightings = [scoring.BM25F(),scoring.TF_IDF(),scoring.Frequency(),]
top_k = 5

def run_search(ix, query_str, mode, weighting, top_k):
    # Build parser (search across title, body, mesh)
    fields = ["title", "body", "mesh"]
    group = OrGroup if mode == "OR" else AndGroup
    parser = MultifieldParser(fields, schema=ix.schema, group=group)

    # Search and print results
    with ix.searcher(weighting=weighting) as searcher:
        q = parser.parse(query_str)
        results = searcher.search(q, limit=top_k)

        print("\n==============================")
        print("Scoring:", weighting.__class__.__name__)
        print("Query:", query_str)
        print("Mode:", mode)
        print("Hits:", len(results), "(showing", min(top_k, len(results)), ")\n")

        i = 1
        for hit in results:
            pmid = hit.get("pmid", "")
            title = hit.get("title", "")
            score = hit.score

            print(str(i) + ". pmid=" + str(pmid) + "  score=" + str(round(score, 4)))
            print("   title: " + str(title))
            i += 1
            
for query_str in queries:
    for mode in modes:
        for weighting in weightings:
            run_search(ix, query_str, mode, weighting, top_k)