import textwrap
from typing import List

MAX_CHARS_PER_CHUNK = 800

def clean_text(text: str) -> str:
    return " ".join(text.split())

def chunk_text(text: str) -> List[str]:
    """
    Simple, robust chunking:
    - cleans whitespace
    - wraps into fixed-size chunks
    - filters out empty/whitespace-only chunks
    """
    text = (text or "").strip()
    if not text:
        return []

    text = clean_text(text)

    raw_chunks = textwrap.wrap(text, MAX_CHARS_PER_CHUNK)
    chunks = [c.strip() for c in raw_chunks if c.strip()]

    return chunks