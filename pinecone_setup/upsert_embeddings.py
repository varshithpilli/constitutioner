from pinecone import Pinecone
import PyPDF2
import re
import os
from dotenv import load_dotenv

load_dotenv()

file_path = "../files/header_removed.pdf"
contents = ""

try:
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            contents += page.extract_text() + "\n\n"
except Exception as e:
    print(f"Error reading PDF: {e}")

contents = re.sub(r"\s+", " ", contents.strip())
contents = re.sub(r"[^\w\s.,!?()-]", "", contents)

chunk_size = 1000
overlap = 200
words = contents.split()

chunks = []
for i in range(0, len(words), chunk_size - overlap):
    chunk = " ".join(words[i:i + chunk_size])
    if chunk.strip():
        chunks.append(chunk)

vectors_with_ids = [
    {"_id": f"vec{i}", "chunk_text": chunk}
    for i, chunk in enumerate(chunks)
]

PINECONE_API = os.getenv("PINECONE_API")
pc = Pinecone(api_key=PINECONE_API)
index = pc.Index("trial01")

batch_size = 10
for i in range(0, len(vectors_with_ids), batch_size):
    batch = vectors_with_ids[i:i + batch_size]
    print(f"Uploading batch {i} to {i+len(batch)}")
    index.upsert_records(
        "trial01",
        batch
    )
