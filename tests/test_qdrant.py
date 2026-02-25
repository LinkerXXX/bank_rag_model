# tests/test_qdrant.py
import pytest
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

def test_qdrant_connection():
    """Тест: подключение к локальному Qdrant"""
    client = QdrantClient(host="localhost", port=6333)
    
    # Правильный способ проверить подключение:
    # Если сервер отвечает, get_collections() вернёт список (даже пустой)
    try:
        collections = client.get_collections()
        assert collections is not None
    except UnexpectedResponse:
        assert False, "Qdrant не отвечает на запросы"
    except Exception as e:
        assert False, f"Ошибка подключения: {e}"

def test_create_collection():
    """Тест: создание тестовой коллекции"""
    client = QdrantClient(host="localhost", port=6333)
    
    collection_name = "test_collection"
    
    # Удаляем коллекцию, если есть (для чистоты теста)
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    # Создаём коллекцию с векторами размера 384
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 384, "distance": "Cosine"}
    )
    
    # Проверяем, что коллекция создана
    collections = client.get_collections()
    collection_names = [c.name for c in collections.collections]
    assert collection_name in collection_names
    
    # Чистим за собой
    client.delete_collection(collection_name)