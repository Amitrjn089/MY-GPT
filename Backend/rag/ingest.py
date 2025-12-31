
import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "..", "data")
INDEX_PATH = os.path.join(BASE_DIR, "rag_index.faiss")
DOCSTORE_PATH = os.path.join(BASE_DIR, "documents.pkl")


model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------- DOCUMENT LOADING --------------------

def load_documents() -> list[str]:
    """
    Loads all .txt and .md files from the data directory.
    """
    documents = []

    if not os.path.exists(DATA_DIR):
        raise RuntimeError(f"Data directory not found: {DATA_DIR}")

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt") or filename.endswith(".md"):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append(f.read())

    if not documents:
        raise RuntimeError("No valid documents found in /data")

    return documents

# -------------------- CHUNKING --------------------

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into overlapping chunks to preserve context.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def ingest():
    """
    Full ingestion pipeline:
    documents -> chunks -> embeddings -> FAISS index
    """
    print("🔹 Loading documents...")
    raw_documents = load_documents()

    print("🔹 Chunking documents...")
    chunks = []
    for doc in raw_documents:
        chunks.extend(chunk_text(doc))

    if not chunks:
        raise RuntimeError("Chunking produced zero chunks")

    print(f"🔹 Total chunks: {len(chunks)}")

    print("🔹 Generating embeddings (local model)...")
    embeddings = model.encode(chunks)

    # Ensure embeddings is always 2D
    embeddings = np.array(embeddings)
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)

    dimension = embeddings.shape[1]

    print(f"🔹 Embedding dimension: {dimension}")

    print("🔹 Building FAISS index...")
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype("float32"))

    print("🔹 Saving FAISS index...")
    faiss.write_index(index, INDEX_PATH)

    print("🔹 Saving document store...")
    with open(DOCSTORE_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print("✅ RAG ingestion complete")
    print(f"   → Index saved at: {INDEX_PATH}")
    print(f"   → Documents saved at: {DOCSTORE_PATH}")

# -------------------- ENTRY POINT --------------------

if __name__ == "__main__":
    ingest()
