from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API = os.getenv("PINECONE_API")

pc = Pinecone(api_key=PINECONE_API)
index = pc.Index("trial01")

def get_chunks(query, top_k=5):
    results = index.search(
        namespace="trial01", 
        query={
            "inputs": {"text": f"{query}"}, 
            "top_k": top_k
        },
        fields=["chunk_text"]
    )
    
    final = [
        hit["fields"].get("chunk_text", "") for hit in results["result"]["hits"]
    ]
    
    if len(final) == 0:
        return None
    return final 