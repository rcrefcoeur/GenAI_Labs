import os
import pickle
import random
import shutil
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser, OrGroup
from I_fetch_pubmed import medline_folder

# Settings (edit these)
TRAIN_SIZE = 200000
TEST_SIZE = 1000
TOP_K = 5

index_dir = "day1/mesh_pred_index"

# Step 4.1: Load data and sample train/test
def load_examples():
    examples = []
    target = TRAIN_SIZE + TEST_SIZE

    files = os.listdir(medline_folder)
    files.sort()

    for filename in files:
        if not (filename.startswith("pmid2content") and filename.endswith(".pkl")):
            continue

        path = os.path.join(medline_folder, filename)
        with open(path, "rb") as f:
            pmid2content = pickle.load(f)

        for pmid in pmid2content:
            title, body, mesh_terms = pmid2content[pmid]

            pmid_str = str(pmid)
            text = str(title) + " " + str(body)

            mesh_list = []
            for t in mesh_terms:
                if t:
                    mesh_list.append(str(t).lower())

            if len(mesh_list) == 0:
                continue

            examples.append((pmid_str, text, mesh_list))

            if len(examples) >= target:
                return examples

    return examples


def sample_train_test(examples):
    random.shuffle(examples)

    train = examples[:min(TRAIN_SIZE, len(examples))]
    test = random.sample(train, TEST_SIZE)

    return train, test


# Step 4.2: Build Whoosh index over Title+Abstract only (no MeSH indexed)
def build_index(train):
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.mkdir(index_dir)

    schema = Schema(
        pmid=ID(stored=True, unique=True),
        content=TEXT(stored=False),
    )

    ix = index.create_in(index_dir, schema)
    writer = ix.writer()

    for pmid, text, mesh_terms in train:
        writer.update_document(pmid=pmid, content=text)

    writer.commit()
    return ix


# Step 4.3: Evaluate Accuracy@1 and Accuracy@5
def evaluate(ix, test):
    correct_at_1 = 0
    correct_at_5 = 0
    total = len(test)

    with ix.searcher() as searcher:
        parser = QueryParser("content", schema=ix.schema, group=OrGroup)

        for pmid, text, mesh_terms in test:
            # "Treat the MeSH terms as a sentence"
            query_str = " ".join(mesh_terms)

            q = parser.parse(query_str)
            results = searcher.search(q, limit=TOP_K)

            # collect hit pmids
            hit_pmids = []
            for hit in results:
                hit_pmids.append(hit["pmid"])

            # Accuracy@1
            if len(hit_pmids) > 0 and hit_pmids[0] == pmid:
                correct_at_1 += 1

            # Accuracy@5
            if pmid in hit_pmids:
                correct_at_5 += 1

    acc1 = correct_at_1 / total if total > 0 else 0.0
    acc5 = correct_at_5 / total if total > 0 else 0.0

    print("Test docs:", total)
    print("Accuracy@1:", acc1)
    print("Accuracy@5:", acc5)


def main():
    random.seed(42)

    print("Loading examples from pickles...")
    examples = load_examples()
    print("Total usable examples:", len(examples))

    print("Sampling train/test...")
    train, test = sample_train_test(examples)
    print("Train size:", len(train))
    print("Test size:", len(test))

    print("Building index (Title+Abstract only)...")
    ix = build_index(train)

    print("Evaluating...")
    evaluate(ix, test)


if __name__ == "__main__":
    main()