from sentence_transformers import SentenceTransformer

# load once (important)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    return model.encode(texts)