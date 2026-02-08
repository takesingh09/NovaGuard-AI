import io
import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts and cleans text from a PDF file-like object.
    
    Args:
        pdf_file: A file-like object (e.g., from streamlit.file_uploader).
        
    Returns:
        str: Cleaned text content from the PDF.
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        
        # Basic cleaning: remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
