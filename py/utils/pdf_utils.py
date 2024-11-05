import fitz

def extract_text_from_pdf(pdf_path):
    """Extracts text from each page in a PDF."""
    doc = fitz.open(pdf_path)
    text_data = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        doc_id = f"{pdf_path}_page_{page_num}"
        text_data.append((doc_id, page.get_text("text")))
    return text_data