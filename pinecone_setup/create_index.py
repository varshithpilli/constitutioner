from pinecone import Pinecone, ServerlessSpec
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API = os.getenv("PINECONE_API")
pc = Pinecone(api_key=PINECONE_API)

index_name = "trial02"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )