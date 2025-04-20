import os
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))
QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION', 'datahub_tables')

# Initialize Qdrant client
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Initialize fastembed
embedder = TextEmbedding(model_name="BAAI/bge-base-en-v1.5")


def search_tables(query: str, top_k: int = 7):
    """Search for tables in Qdrant using a text query and return top_k results."""
    query_embedding = list(embedder.embed([query]))[0]
    search_result = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=top_k
    )
    results = []
    for hit in search_result:
        payload = hit.payload
        score = hit.score
        results.append({
            'score': score,
            'table_urn': payload.get('table_urn'),
            'text': payload.get('text')
        })
    return results

if __name__ == "__main__":
    print("Searching for tables similar to 'users'...")
    results = search_tables("users", top_k=7)
    for i, res in enumerate(results, 1):
        print(f"Result {i} (score={res['score']:.4f}):")
        print(res['text'])
        print(f"URN: {res['table_urn']}")
        print("---") 