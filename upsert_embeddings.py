from pinecone.grpc import PineconeGRPC as Pinecone
import PyPDF2
import re
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer('all-MiniLM-L6-v2')
load_dotenv()

chunks = []
embeddings = []

file_path = "files/header_removed.pdf"
try:
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        contents = ""
        for page in reader.pages:
            contents += page.extract_text() + "\n\n"

except Exception as e:
    print(f"Something happened mf: {e}")

contents = re.sub(r'\s+', ' ', contents.strip())
contents = re.sub(r'[^\w\s.,!?()-]', '', contents)

chunk_size = 1000
overlap = 200

words = contents.split()
for i in range(0, len(words), chunk_size - overlap):
    chunk = ' '.join(words[i:i + chunk_size])
    if chunk.strip():
        chunks.append(chunk)

embeddings = np.array(embedder.encode(chunks))

PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_API = os.getenv("PINECONE_API")
print("env successful")
pc = Pinecone(api_key=PINECONE_API)
index = pc.Index(host=PINECONE_HOST)
print("index successful")

vector_dim = 384
vector_count = 10000

vectors_with_ids = [
    (f"vec{i}", vector.tolist(), {"chunk_text": chunk})
    for i, (vector, chunk) in enumerate(zip(embeddings, chunks))
]

batch_size = 500
for i in range(0, len(vectors_with_ids), batch_size):
    batch = vectors_with_ids[i:i + batch_size]
    print(f"Uploading batch {i} to {i + len(batch)}")
    index.upsert(vectors=batch)
