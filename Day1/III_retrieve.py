from whoosh import index, scoring
from II_index import index_dir
from whoosh.qparser import MultifieldParser, OrGroup, AndGroup, FuzzyTermPlugin, PhrasePlugin

# Load your index here
ix = index.open_dir(index_dir)

# Choose a query and mode
query_str = "heart attack diabetes"     # normal
# query_str = "\"heart attack\" diabetes" # phrase
# query_str = "heart attack~ diabetes"    # fuzzy
mode = "OR" # OR or AND
top_k = 5

# Choose ONE scoring method (others commented out)
weighting = scoring.BM25F()
# weighting = scoring.TF_IDF()
# weighting = scoring.Frequency()

# Build parser (search across title, body, mesh)
fields = ["title", "body", "mesh"]
group = OrGroup if mode == "OR" else AndGroup
parser = MultifieldParser(fields, schema=ix.schema, group=group)

# Search and print results
with ix.searcher(weighting=weighting) as searcher:
    q = parser.parse(query_str)
    results = searcher.search(q, limit=top_k)

    print("Scoring:", weighting.__class__.__name__)
    print(f"Query: {query_str}")
    print(f"Mode: {mode}")
    print(f"Hits: {len(results)} (showing {min(top_k, len(results))})\n")

    i = 1
    for hit in results:
        pmid = hit.get("pmid", "")
        title = hit.get("title", "")
        score = hit.score

        print(str(i) + ". pmid=" + str(pmid) + "  score=" + str(round(score, 4)))
        print("   title: " + str(title))
        i += 1