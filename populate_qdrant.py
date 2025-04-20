import os
import uuid
import time
from get_all_tables_from_datahub import get_all_tables, DescribeTable, generate_table_description
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
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
embedder = TextEmbedding(model_name="BAAI/bge-base-en-v1.5")  # You can change the model if needed

# Correct vector size for BAAI/bge-base-en-v1.5
VECTOR_SIZE = 768

# Drop collection if it exists (to avoid dimension mismatch)
collections = [c.name for c in client.get_collections().collections]
if QDRANT_COLLECTION in collections:
    print(f"Collection '{QDRANT_COLLECTION}' exists. Dropping it to avoid dimension mismatch...")
    client.delete_collection(collection_name=QDRANT_COLLECTION)

# Create collection
client.create_collection(
    collection_name=QDRANT_COLLECTION,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
)

# Fetch all tables
tables = get_all_tables()
print(f"Fetched {len(tables)} tables from DataHub.")

# Limit to first 9 tables to avoid long waits
# max_tables = 9
# tables = tables[:max_tables]

docs = []
ids = []
rate_limit = 10  # Gemini API calls per minute
calls_this_minute = 0
minute_start = time.time()
for idx, t in enumerate(tables):
    try:
        # Rate limiting for Gemini API
        if calls_this_minute >= rate_limit:
            elapsed = time.time() - minute_start
            if elapsed < 60:
                sleep_time = 60 - elapsed
                print(f"Rate limit reached. Sleeping for {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            calls_this_minute = 0
            minute_start = time.time()
        desc_data = DescribeTable(t.urn)
        columns = desc_data.get('columns', [])
        description = generate_table_description(t.name, columns)
        calls_this_minute += 1
        doc_text = f"Table: {t.name}\nDescription: {description}"
        docs.append(doc_text)
        ids.append(str(uuid.uuid4()))
    except Exception as e:
        print(f"Error processing table {t.urn}: {e}")

print(f"Generating embeddings for {len(docs)} documents...")
embeddings = list(embedder.embed(docs))

print(f"Uploading to Qdrant...")
points = [
    PointStruct(
        id=uuid_,
        vector=embedding,
        payload={
            "text": doc,
            "table_urn": urn
        }
    )
    for uuid_, embedding, doc, urn in zip(ids, embeddings, docs, [t.urn for t in tables])
]

client.upsert(collection_name=QDRANT_COLLECTION, points=points)
print(f"Uploaded {len(points)} documents to Qdrant collection '{QDRANT_COLLECTION}'.") 