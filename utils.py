from PyPDF2 import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with open("temp.pdf", "wb") as f:
        f.write(file_bytes)
    reader = PdfReader("temp.pdf")
    for page in reader.pages:
        text += page.extract_text() or ""
    return text