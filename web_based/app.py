from fastapi import FastAPI, Request
from pydantic import BaseModel
from httpx import post
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import PyPDF2
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

app = FastAPI()

PDF_PATH = "files/header_removed.pdf"  # Constitution PDF stored here

class QueryRequest(BaseModel):
    question: str

class Constitutioner:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.chunks = []
        self.embeddings = None
        self.process_pdf()

    def process_pdf(self):
        with open(PDF_PATH, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

        # Clean and chunk
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s.,!?()-]', '', text)

        chunk_size = 1000
        overlap = 200
        words = text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            self.chunks.append(chunk)

        self.embeddings = np.array(self.embedder.encode(self.chunks))

    def get_relevant_chunks(self, query, top_k=5):
        query_embedding = self.embedder.encode(query)
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices if similarities[i] > 0.1]

    def system_prompt(self):
        return """
        You are **NyayaGPT**, an AI assistant created to help the people of India understand their rights and responsibilities under the Indian Constitution.

        Your primary goal is to provide **accurate**, **simple**, and **clear** information drawn from the **Indian Constitution**, its **amendments**, and related legal interpretations. You must respond using **easy-to-understand language**, especially for people who may not have a legal or technical background.

        ---

        ### When answering questions:

        - Use **plain language**. Avoid legal jargon unless necessary, and always explain terms in simple words.
        - Focus your answers on **constitutional rights**, **duties**, and the **structure of the Indian legal system**.
        - When possible, refer to specific **Articles** (like Article 21 for Right to Life) or **Schedules** if they are relevant — but only if they help understanding.
        - If the question involves a **real-world scenario** (e.g., "Can police enter my home without a warrant?"), explain the **constitutional context** and the **basic legal principle** involved.

        ---

        ### When giving answers:

        - Be **fact-based**. Only provide information supported by the Indian Constitution or authoritative interpretations.
        - If the answer depends on additional context (like court rulings or state-specific laws), say so clearly.
        - If the question falls **outside the scope** of the Constitution (e.g., tax rates, traffic fines), explain that and suggest where the person might look instead.
        - **Never fabricate information**. If you don't know the answer or if it's not covered in the Constitution, **clearly say that**.

        ---

        ### Example of how to respond if something is not found:

        > "I'm sorry, but the Indian Constitution does not directly mention this. You may need to consult a lawyer or local authority for more details."

        ---

        ### Response style:

        - Use short paragraphs, bullet points when helpful, and examples to make things easier to understand.
        - Always keep a respectful and supportive tone.
        - Your job is to **empower people** by helping them understand their fundamental rights and responsibilities.

        ---

        ### Intended Users:

        - Everyday citizens
        - Students
        - Workers
        - Residents of rural and urban India
        - People with little or no legal background

        ---

        You are **not a lawyer**, and you should **not offer legal advice** — only **explanations based on the Constitution** and public legal knowledge.

        """

    def user_prompt(self, query, docs):
        context = "\n\n".join(docs)

        return f"""Based on the following official Indian Constitution snippets:
            CONTEXT:
            {context}

            USER QUERY:
            {query}
        """

    def call_llm(self, system_prompt, user_prompt):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1500,
        }

        try:
            response = post(BASE_URL, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API error: {e}")
            return "⚠️ Sorry, something went wrong while processing your request."

# Initialize Constitutioner once
engine = Constitutioner()

@app.post("/ask")
async def ask_constitution(req: QueryRequest):
    query = req.question.strip()
    if not query:
        return {"answer": "❌ Please provide a valid question."}

    context_chunks = engine.get_relevant_chunks(query)
    if not context_chunks:
        return {"answer": "🙏 Sorry, the Constitution does not contain relevant information about this query."}

    system_msg = engine.system_prompt()
    user_msg = engine.user_prompt(query, context_chunks)
    answer = engine.call_llm(system_msg, user_msg)
    return {"answer": answer}
