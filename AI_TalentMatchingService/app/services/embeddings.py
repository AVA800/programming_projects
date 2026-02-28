import requests
from typing import List
import numpy as np

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
EXPECTED_DIM = 768

class EmbeddingError(Exception):
    pass

def embed_text(text: str) -> List[float]:
    text = (text or "").strip()
    if not text:
        raise EmbeddingError("Cannot embed empty text")

    resp = requests.post(
        OLLAMA_EMBED_URL,
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30,
    )

    if resp.status_code != 200:
        raise EmbeddingError(f"Embedding request failed: {resp.status_code} {resp.text}")

    data = resp.json()
    embedding = data.get("embedding")

    if not embedding or not isinstance(embedding, list):
        raise EmbeddingError(f"Invalid embedding response: {data}")

    if len(embedding) != EXPECTED_DIM:
        raise EmbeddingError(
            f"Expected {EXPECTED_DIM} dimensions, got {len(embedding)}"
        )

    return embedding

def compute_embedding_similarity(resume_chunks, job_chunks):
    resume_vectors = [
        np.array(c.embedding) 
        for c in resume_chunks 
        if c.embedding is not None
    ]
    job_vectors = [
        np.array(j.embedding) 
        for j in job_chunks 
        if j.embedding is not None
    ]

    if not resume_vectors or not job_vectors:
        return 0.0

    resume_matrix = np.vstack(resume_vectors)
    job_matrix = np.vstack(job_vectors)

    resume_norm = resume_matrix / np.linalg.norm(resume_matrix, axis=1, keepdims=True)
    job_norm = job_matrix / np.linalg.norm(job_matrix, axis=1, keepdims=True)

    sim_matrix = np.dot(resume_norm, job_norm.T)

    return float(sim_matrix.mean())
