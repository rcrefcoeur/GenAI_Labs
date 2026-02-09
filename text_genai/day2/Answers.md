I have ran the code with two different models for indexing: intfloat/multilingual-e5-base and Qwen/Qwen3-Embedding-0.6B.
After indexing, I ran the index test with different values for K_source_chunks: 2, 3, 4, 5, and 10.

| embeddings_model_name         | chunk_size | chunk_overlap | K_source_chunks |   F1 |
| ----------------------------- | ---------: | ------------: | --------------: | ---: |
| intfloat/multilingual-e5-base |        500 |            50 |               2 | 0.50 |
| Qwen/Qwen3-Embedding-0.6B     |        500 |            50 |               2 | 0.47 |
| intfloat/multilingual-e5-base |        500 |            50 |               3 | 0.50 |
| Qwen/Qwen3-Embedding-0.6B     |        500 |            50 |               3 | 0.61 |
| intfloat/multilingual-e5-base |        500 |            50 |               4 | 0.68 |
| Qwen/Qwen3-Embedding-0.6B     |        500 |            50 |               4 | 0.61 |
| intfloat/multilingual-e5-base |        500 |            50 |               5 | 0.68 |
| Qwen/Qwen3-Embedding-0.6B     |        500 |            50 |               5 | 0.63 |
| intfloat/multilingual-e5-base |        500 |            50 |              10 | 0.65 |
| Qwen/Qwen3-Embedding-0.6B     |        500 |            50 |              10 | 0.53 |

Both models sort all text chunks according to what the models predict to be best matching to the questions.
K_source_chunks determines how many of the chunks are returned, starting from the models top predicted match.

K2-3 (Low F1 scores)
If the model doesn't have all the correct text chunks in the top results, K_source_chunks will be lower initially, due to a low recall.

K4-5 (Optimal range for high F1 scores)
This seems to be the K_source_chunks value with the best trade-off between higher recall and lowering precision due to retrieving irrelevant chunks.

K10 (Low F1 scores)
Results get more polluted with irrelevant text chunks, so the precision decreases.

I was also interested in comparing other parameters, such as chunk size and chunk overlap, but the II_index.py process is not deterministic, so it would be difficult to see (for a low number of runs) fair cause/effect.