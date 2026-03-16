from pathlib import Path
import sys
import os

os.environ["DOCLING_OCR_ENABLED"] = "false"
os.environ["DOCLING_DO_OCR"] = "false"

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qdrant_bd.QDmanager import QdrantManager
import ollama

qdrant = QdrantManager(host="localhost", port=6333)

prompt = input("Enter a prompt: ")

results = qdrant.points_search(prompt, collection_name="bank_docs", limit=10)

seen = set()
filtered = []
for r in results:
    text = r.payload['text'].strip()
    if len(text) > 50 and text not in seen:
        seen.add(text)
        filtered.append(r)

if not filtered:
    print("Не найдено релевантной информации.")
else:
    context = "\n\n".join([r.payload['text'] for r in filtered])
    response = ollama.generate(
        model='qwen2.5:3b',
        prompt=f"""Ты помощник по документации банка. Ответь на вопрос ТОЛЬКО на основе контекста.
Если информации нет — так и скажи.

Контекст:
{context}

Вопрос: {prompt}

Ответ:"""
    )
    
    print(f"\n{response['response']}\n")