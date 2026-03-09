from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

def qdrant_upload(dom_name, port_num, coll_name, embed_len):
    client = QdrantClient(host=dom_name, port=port_num)
    if not client.collection_exists(coll_name):
        client.create_collection(
        collection_name=coll_name,
        vectors_config=VectorParams(size=embed_len, distance=Distance.COSINE),
    )


