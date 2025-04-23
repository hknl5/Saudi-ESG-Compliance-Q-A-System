import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv
import os
import hashlib

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load FAISS index + metadata
index = faiss.read_index("data/sector_faiss_index.index")
with open("data/sector_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embedding model (must match your index)
model = SentenceTransformer("intfloat/e5-large-v2", device="cpu")

#CONFIGS
TOP_K = 10  # retrieve top k results per query variant
FINAL_TOP_N = 5 # how many results you want to re-rank and show
MIN_WORDS = 8
EXCLUSION_KEYWORDS = ["copyright", "page", "table of contents", "appendix"]

seen_texts = set()

def is_valid_chunk(text):
    text = text.lower().strip()
    if (
        len(text.split()) < 8 or
        any(keyword in text for keyword in EXCLUSION_KEYWORDS) or
        text.isupper() or
        text in seen_texts
    ):
        return False

    seen_texts.add(text)
    return True

def expand_query(original):
    variants = [
        original,
        f"Explain: {original}",
        f"Clarify the meaning of: {original}",
        f"What does this mean: {original}?",
        f"Definition of: {original}",
    ]
    print("\nQuery Expansion Variants:")
    for q in variants:
        print("-", q)
    return variants


def retrieve_chunks(query):
    query_variants = expand_query(query)
    all_results = {}  # key: hash, value: (chunk, score, from_query)
    seen_hashes = set()

    print("\nRaw Retrieved Chunks with Similarity Scores:")

    for q in query_variants:
        q_embed = model.encode("query: " + q, normalize_embeddings=True)
        D, I = index.search(np.array([q_embed]).astype("float32"), k=TOP_K)

        for score, idx in zip(D[0], I[0]):
            chunk = metadata[idx]
            text = chunk["text"].strip().lower()

            # Generate a hash to remove duplicates across files
            content_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)

            if is_valid_chunk(text):
                all_results[content_hash] = (chunk, score, q)

    # Sort by score descending
    sorted_chunks = sorted(all_results.values(), key=lambda x: x[1], reverse=True)
    selected = sorted_chunks[:FINAL_TOP_N]

    # Print info for each chunk
    for i, (chunk, score, from_query) in enumerate(selected, 1):
        clean_text = chunk['text'][:150].replace("\n", " ")
        print(f"Chunk {i}")
        print(f"   From: {chunk['source_file']}")
        print(f"   Matched Query: {from_query}")
        print(f"   Score: {score:.4f}")
        print(f"   Text: {clean_text}...")
        print()

    return [item[0] for item in selected]


def rerank_with_gpt(question, chunks):
    excerpt_texts = "\n".join([f"{i+1}. {c['text']}" for i, c in enumerate(chunks)])

    prompt = f"""Rank the following ESG excerpts in order of relevance to the question: "{question}"
Return the top most relevant ones. Just list their numbers like: 1, 3, 4 or one per line.

Excerpts:
{excerpt_texts}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["choices"][0]["message"]["content"]

    # Handle both comma-separated or line-separated
    raw_items = []
    for line in content.splitlines():
        raw_items += line.replace(",", " ").split()

    selected_indices = []
    for item in raw_items:
        try:
            idx = int(item.strip().strip(".")) - 1
            if 0 <= idx < len(chunks):
                selected_indices.append(idx)
        except:
            continue

    return [chunks[i] for i in selected_indices]