# -*- coding: utf-8 -*-
"""
Task Sparse IR

Created on Tue November 11 10:42:53 2025

@author: agha
"""

import json
import chromadb
import numpy as np
from tqdm import tqdm
from I_constants import *
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

test_data = json.load(open('day2/output/squad_multiple_contexts.json', 'r'))

def get_f1(true_doc: set, pred_doc: set) -> float:
    """
    Compute F1 score between two sets of document identifiers.
    F1 = 2 * (precision * recall) / (precision + recall)

    Edge cases:
      - If both sets are empty: perfect match -> 1.0
      - If either set is empty (but not both): -> 0.0
    """
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

if __name__ == "__main__":
    version = 1
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, cache_folder=models_path)
    chroma_client = chromadb.PersistentClient(persist_path)
    db = Chroma(persist_directory=persist_path,
                embedding_function=embeddings,
                collection_name="test_collection",
                client=chroma_client
                )

    retriever = db.as_retriever(search_type="similarity",
                                search_kwargs={"k": K_source_chunks})

    f1s = []
    for entry in tqdm(test_data):
        query = entry['text']
        from pathlib import PurePath

        entry_prediction = [
            PurePath(doc.metadata.get("source", "")).name
            for doc in retriever.invoke(query)
        ]
        entry_true = entry['sources']
        f1s.append(get_f1(set(entry_true), set(entry_prediction)))
        
    print("embeddings_model_name:", embeddings_model_name)
    print("chunk_size:", chunk_size)
    print("chunk_overlap:", chunk_overlap)
    print("K_source_chunks:", K_source_chunks)
    print("persist_path:", persist_path)
    print("models_path:", models_path)
    print("source_path:", source_path)
    print("F1: %.2f"%(np.mean(f1s)))
