try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

def extract_text(path: str) -> str:
    """Extract text from a PDF file."""
    if PdfReader is None:
        with open(path, "rb") as f:
            return f.read().decode("utf-8", errors="ignore")
    try:
        reader = PdfReader(path)
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        with open(path, "rb") as f:
            return f.read().decode("utf-8", errors="ignore")