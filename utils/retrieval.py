import faiss
import numpy as np

# embedding dimension for MiniLM
DIM = 384

index = faiss.IndexFlatL2(DIM)
store = []

def build_index(chunks, embeddings):
    global store
    index.reset()  # IMPORTANT: clear previous runs
    index.add(np.array(embeddings))
    store = chunks

def retrieve(query_embedding, k=3):
    D, I = index.search(np.array([query_embedding]), k)
    return [store[i] for i in I[0] if i < len(store)]