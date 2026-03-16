from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def is_skip_page(text):
    if not text or len(text.strip()) < 50:
        return True
    
    dots = len(re.findall(r'\.{20,}', text))
    if dots > 5:
        return True
    
    version_count = text.lower().count('версия')
    if version_count > 3:
        return True
    
    version_count = text.count('История изменений')
    if version_count >= 1:
        return True

    numbers = len(re.findall(r'\b\d{1,3}\b', text))
    words = len(re.findall(r'[а-яА-Яa-zA-Z]{3,}', text))
    if words > 0 and numbers / (numbers + words) > 0.9:
        return True
    
    return False


def parser_pdf(pdf_to_txt, skip_pages=True):
    reader = PdfReader(pdf_to_txt)
    
    all_text = []
    skipped_pages = []
    
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            
            if skip_pages and is_skip_page(text):
                skipped_pages.append(i + 1)
                continue
            
            if text:
                all_text.append(text)
                
        except Exception as e:
            pass
    
    if skipped_pages:
        print(f"Пропущено страниц: {skipped_pages}")
    
    full_text = "\n\n".join(all_text)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(full_text)
    
    return [
        {"text": chunk, "metadata": {"source": Path(pdf_to_txt).name}}
        for chunk in chunks if len(chunk.strip()) > 50
    ]