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

def get_chunks(query, top_k=5):
    
    query_embedding = embedder.encode(query).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    relevent_chunks = []
    for i in range(len(results['matches'])):
        relevent_chunks.append(results['matches'][i]['metadata']['chunk_text'])
    
    return relevent_chunks
