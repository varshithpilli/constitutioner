from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API = os.getenv("PINECONE_API")
PINECONE_HOST = os.getenv("PINECONE_HOST")

embedder = SentenceTransformer('all-MiniLM-L6-v2')

pc = Pinecone(api_key=PINECONE_API)
index = pc.Index(host=PINECONE_HOST)

query = "what is the legal age to marry in india"
query_embedding = embedder.encode(query).tolist()

results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)

print(results)
