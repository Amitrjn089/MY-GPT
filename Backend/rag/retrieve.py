
import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# -------------------- PATHS --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "rag_index.faiss")
DOCSTORE_PATH = os.path.join(BASE_DIR, "documents.pkl")

# -------------------- MODEL --------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------- LOAD INDEX + DOCS --------------------

if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCSTORE_PATH):
    raise RuntimeError("RAG index not found. Run ingest.py first.")

index = faiss.read_index(INDEX_PATH)

with open(DOCSTORE_PATH, "rb") as f:
    documents = pickle.load(f)

# -------------------- RETRIEVAL --------------------

def retrieve_context(query: str, k: int = 3) -> list[str]:
    """
    Retrieves top-k relevant chunks for a query.
    """

    # Encode query
    query_embedding = model.encode(query)

    # Normalize to 2D array: (1, dim)
    query_embedding = np.array(query_embedding)
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    query_embedding = query_embedding.astype("float32")

    # FAISS search
    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(documents):
            results.append(documents[idx])

    return results
