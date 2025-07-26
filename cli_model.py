from httpx import post
import os
from dotenv import load_dotenv
from web_based.infere import get_chunks
import json
import requests

load_dotenv()

def print_header(title):
    print("\n" + "="*60)
    print(f"{title.upper()}")
    print("="*60 + "\n")


API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

class Constitutioner:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL
        self.model = MODEL
        
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

    def api_call(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }

        buffer = ""
        with requests.post(self.base_url, headers=headers, json=payload, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
                buffer += chunk
                while True:
                    line_end = buffer.find('\n')
                    if line_end == -1:
                        break

                    line = buffer[:line_end].strip()
                    buffer = buffer[line_end + 1:]

                    if line.startswith('data: '):
                        data = line[6:]
                        if data == '[DONE]':
                            return

                        try:
                            data_obj = json.loads(data)
                            content = data_obj["choices"][0]["delta"].get("content")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            pass

            
    def inference(self, query):
        docs = get_chunks(query)
        messages = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": self.user_prompt(query, docs)}
        ]
        response_chunks = self.api_call(messages)

        full_response = ""
        print()
        for chunk in response_chunks:
            print(chunk, end="", flush=True)
            full_response += chunk

        print()


def main():
    trial01 = Constitutioner()
    while True:
        question = input("Enter your query: ")
        if question.lower() in ["exit", "stop", "quit", "leave", "end", ""]:
            print_header("Exiting Constitutioner")
            break
        trial01.inference(question)

def print_banner():
    print(r"""
   _____                _   _ _         _   _                       
  / ____|              | | (_) |       | | (_)                      
 | |     ___  _ __  ___| |_ _| |_ _   _| |_ _  ___  _ __   ___ _ __ 
 | |    / _ \| '_ \/ __| __| | __| | | | __| |/ _ \| '_ \ / _ \ '__|
 | |___| (_) | | | \__ \ |_| | |_| |_| | |_| | (_) | | | |  __/ |   
  \_____\___/|_| |_|___/\__|_|\__|\__,_|\__|_|\___/|_| |_|\___|_|   
                                                                    
            🇮🇳  AI Assistant for the Indian Constitution 🇮🇳
""")


if __name__ == "__main__":
    print_banner()
    main()