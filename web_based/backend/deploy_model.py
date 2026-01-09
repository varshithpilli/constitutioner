import httpx
import os
from dotenv import load_dotenv
from infere import get_chunks
import requests
import json

load_dotenv()

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
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "stream": True
        })

        buffer = ""
        with requests.post(url=self.base_url, headers=headers, data=payload, stream=True) as r:
            for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
                buffer += chunk
                print(chunk)
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
        
        # response = httpx.post(self.base_url, json=payload, headers=headers, timeout=20.0)
        # print(response)
        # response.raise_for_status()
        # result = response.json()
        # print("Status Code:", response.status_code)
        # print("Response Text:", response.text)

        return result['choices'][0]['message']['content']
                        
    def inference(self, query):
        docs = get_chunks(query)
        if docs is None:
            return None
        
        # print(docs)
        
        messages = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": self.user_prompt(query, docs)}
        ]
        
        yield from self.api_call(messages)
        # return self.api_call(messages)