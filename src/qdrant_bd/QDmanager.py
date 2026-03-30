from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import ollama
import requests

class QdrantManager:

    def __init__(self, host='localhost', port=6333, embedding_model='mxbai-embed-large', llm_model='qwen2.5:3b'):
        self.client = QdrantClient(host=host, port=port)
        self.embedding_model = embedding_model
        self.llm_model = llm_model

    def create_collection(self, collection_name="bank_docs"):
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
    
    def ollama_embed(self, prompt):
        result = ollama.embed(model=self.embedding_model, input=[prompt])
        return result["embeddings"][0]

    def upsert_chunks(self, chunks, collection_name="bank_docs"):
        self.create_collection(collection_name)

        points = []
        for i, chunk in enumerate(chunks):
            vector = self.ollama_embed(chunk["text"])
            points.append(PointStruct(
                id=i,
                vector=vector,
                payload=chunk
            ))
        
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

    def points_search(self, query, limit, collection_name="bank_docs"):
        query_vector = self.ollama_embed(query)
        
        search_result = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            with_payload=True,
            limit=limit
        )
        
        return search_result.points
    
    def generate_response(self, prompt: str):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.llm_model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]