# D:\FHNW\CO5 - Generative AI\CO5-main\RAG\II_index_test.py

# -*- coding: utf-8 -*-
"""
Task Sparse IR
"""

import json
import chromadb
import numpy as np
from tqdm import tqdm
from pathlib import PurePath

from RAG.I_constants import *
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

test_data = json.load(open("squad_multiple_contexts.json", "r", encoding="utf-8"))


def get_f1(true_doc: set, pred_doc: set) -> float:
    if not true_doc and not pred_doc:
        return 1.0
    if not true_doc or not pred_doc:
        return 0.0

    tp = len(true_doc & pred_doc)
    if tp == 0:
        return 0.0

    precision = tp / len(pred_doc)
    recall = tp / len(true_doc)
    return 2.0 * precision * recall / (precision + recall)


def prf1(true_set: set[str], pred_list: list[str]) -> tuple[float, float, float, set[str], set[str], set[str]]:
    pred_set = set(pred_list)

    if not true_set and not pred_set:
        return 1.0, 1.0, 1.0, set(), set(), set()
    if not pred_set and true_set:
        return 0.0, 0.0, 0.0, set(), set(), set(true_set)
    if pred_set and not true_set:
        return 0.0, 0.0, 0.0, set(), set(pred_set), set()

    tp_set = true_set & pred_set
    fp_set = pred_set - true_set
    fn_set = true_set - pred_set

    precision = len(tp_set) / len(pred_set) if pred_set else 0.0
    recall = len(tp_set) / len(true_set) if true_set else 0.0
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    return precision, recall, f1, tp_set, fp_set, fn_set


def format_list(items: list[str] | set[str], max_items: int = 10) -> str:
    items_sorted = sorted(items)
    if len(items_sorted) <= max_items:
        return str(items_sorted)
    head = items_sorted[:max_items]
    return f"{head} ... (+{len(items_sorted) - max_items} more)"


if __name__ == "__main__":
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, cache_folder=models_path)

    chroma_client = chromadb.PersistentClient(persist_path)
    db = Chroma(
        persist_directory=persist_path,
        embedding_function=embeddings,
        collection_name="test_collection",
        client=chroma_client,
    )

    print(f"Chroma persist_path: {persist_path}")
    try:
        print("Chroma count:", db._collection.count())
    except Exception as e:
        print("Could not read collection count:", repr(e))

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": K_source_chunks})

    f1s = []
    precisions = []
    recalls = []

    for idx, entry in enumerate(tqdm(test_data), start=1):
        query = entry["text"]
        true_list = entry["sources"]
        true_set = set(true_list)

        docs = retriever.invoke(query)

        pred_list = [PurePath(doc.metadata.get("source", "")).name for doc in docs]
        pred_set = set(pred_list)

        p, r, f1, tp_set, fp_set, fn_set = prf1(true_set, pred_list)

        precisions.append(p)
        recalls.append(r)
        f1s.append(f1)

        print("\n" + "=" * 90)
        print(f"Task {idx:02d}/{len(test_data)}")
        print(f"Query (first 180 chars): {query[:180]!r}")
        print(f"TRUE ({len(true_set)}): {format_list(true_set)}")
        print(f"PRED ({len(pred_set)}): {format_list(pred_set)}")
        print(f"TP  ({len(tp_set)}): {format_list(tp_set)}")
        print(f"FP  ({len(fp_set)}): {format_list(fp_set)}")
        print(f"FN  ({len(fn_set)}): {format_list(fn_set)}")
        print(f"P/R/F1: {p:.3f} / {r:.3f} / {f1:.3f}")

        # Extra debug: show raw source metadata to spot naming/path mismatches
        if docs:
            print("\nTop retrieved docs (ranked):")
            for rank, doc in enumerate(docs, start=1):
                raw_source = doc.metadata.get("source")
                norm_name = PurePath(raw_source or "").name
                print(f"  {rank:02d}. source_name={norm_name!r}  raw_source={raw_source!r}")
        else:
            print("\nNo docs retrieved for this query.")

    print("\n" + "#" * 90)
    print(f"Macro Precision: {float(np.mean(precisions)):.3f}")
    print(f"Macro Recall:    {float(np.mean(recalls)):.3f}")
    print(f"Macro F1:        {float(np.mean(f1s)):.3f}")
