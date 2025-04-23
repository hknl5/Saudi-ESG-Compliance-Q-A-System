import json
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# File with cleaned ESG chunks
input_file = "data/sector_chunks.jsonl"

# Output files
faiss_index_file = "sector_faiss_index.index"
metadata_file = "sector_metadata.json"

# Load your ESG chunks
with open(input_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]

# Load the E5 model (Large version for high accuracy)
model_name = "intfloat/e5-large-v2"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(model_name, device=device)

# Prepare text prompts (E5 expects this format)
texts = ["passage: " + chunk["text"] for chunk in chunks]

# Generate embeddings
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity with normalized vectors
index.add(embeddings)

# Save the index
faiss.write_index(index, faiss_index_file)
# Save metadata (so you can map back later)
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)
