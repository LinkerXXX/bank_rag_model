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

chunks = parser_pdf('data/test.pdf')
with open("data/parse.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

qdrant = QdrantManager(host="localhost", port=6333)
qdrant.create_collection("bank_docs")
qdrant.upsert_chunks(chunks, collection_name="bank_docs")

prompt = input("Enter a prompt: ")
results = qdrant.points_search(prompt, collection_name="bank_docs", limit=5)
print(results)