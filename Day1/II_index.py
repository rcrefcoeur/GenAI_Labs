import os
import pickle
import shutil
from tqdm import tqdm
from whoosh import index
from I_fetch_pubmed import medline_folder
from whoosh.fields import Schema, TEXT, ID


schema = Schema(
    pmid=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    body=TEXT(stored=True),
    mesh=TEXT(stored=True),
)

index_dir = "pubmed_index"


def get_index():
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    ix = index.create_in(index_dir, schema)

    pkl_files = sorted(
        f for f in os.listdir(medline_folder)
        if f.startswith("pmid2content") and f.endswith(".pkl")
    )

    writer = ix.writer()

    for pkl_name in tqdm(pkl_files, desc="Pickles", unit="file"):
        pkl_path = os.path.join(medline_folder, pkl_name)
        with open(pkl_path, "rb") as f:
            pmid2content = pickle.load(f)

        for pmid, (title, body, mesh_terms) in pmid2content.items():
            pmid = str(pmid)
            title = str(title)
            body = str(body)
            mesh_text = " ".join(mesh_terms) if mesh_terms else ""

            writer.update_document(
                pmid=pmid,
                title=title,
                body=body,
                mesh=mesh_text,
            )

    writer.commit()
    return ix


if __name__ == "__main__":
    get_index()