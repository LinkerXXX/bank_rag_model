from pathlib import Path
import sys
import json
import os

os.environ["DOCLING_OCR_ENABLED"] = "false"
os.environ["DOCLING_DO_OCR"] = "false"

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from docling_parser.parser import parser_pdf
from qdrant_bd.QDmanager import QdrantManager

docs_dir = Path("data/docs")
parse_dir = Path("data/parse")
parse_dir.mkdir(parents=True, exist_ok=True)

qdrant = QdrantManager(host="localhost", port=6333)
qdrant.create_collection("bank_docs")

total_chunks = 0

for pdf_file in docs_dir.glob("*.pdf"):
    print(f"Обработка: {pdf_file.name}")
    
    chunks = parser_pdf(str(pdf_file))
    
    json_file = parse_dir / f"{pdf_file.stem}.json"
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)
    
    qdrant.upsert_chunks(chunks, collection_name="bank_docs")
    total_chunks += len(chunks)

print(f"\nГотово. Всего чанков: {total_chunks}")