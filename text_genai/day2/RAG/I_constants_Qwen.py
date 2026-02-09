# -*- coding: utf-8 -*-
"""
Task Sparse IR

Created on Tue November 11 09:14:24 2025

@author: agha
"""

# Indexer
persist_path= 'day2/output/chroma_db_Qwen'
models_path = 'day2/output/models'
source_path = 'day2/output/squad/texts'
embeddings_model_name='Qwen/Qwen3-Embedding-0.6B'
chunk_size = 500
chunk_overlap = 50
K_source_chunks=4


# LLM generator
llm_base = 'llms'
model_n_ctx=512
model_n_batch=32
num_gpu_layers =20
