import io
import pdfplumber

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF file (bytes) using pdfplumber.
    Returns a single cleaned string.
    """
    text_parts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    full_text = "\n".join(text_parts)
    return full_text.strip()