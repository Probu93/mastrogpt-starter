import os
import openai
import socket

MODEL = "llama3.1:8b"
ROLE = "system:You are a helpful assistant."

def stream(args, lines):
    host = args.get("STREAM_HOST")
    port = int(args.get("STREAM_PORT"))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for line in lines:
            try:
                content = line.choices[0].delta.get("content", "")
                if content:
                    msg = f"Output: {content}"
                    s.sendall(msg.encode('utf-8'))
            except Exception as e:
                print("Error processing line:", e)

class Chat:
    def __init__(self, args):
        host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
        api_key = args.get("AUTH", os.getenv("AUTH"))
        base_url = f"https://{api_key}@{host}/v1"
        
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        
        self.args = args  # salva args per usarli in stream()
        self.messages = []
        self.add(ROLE)
        
    def add(self, msg):
        role, content = msg.split(":", maxsplit=1)
        self.messages.append({
            "role": role.strip(),
            "content": content.strip(),
        })
    
    def complete(self):
        # Chiamata con stream=True
        res_stream = self.client.chat.completions.create(
            model=MODEL,
            messages=self.messages,
            stream=True,
        )
        
        # Gestisci lo stream e invia al socket
        stream(self.args, res_stream)
        
        # Per complete, accumula testo completo
        full_response = ""
        try:
            for line in res_stream:
                delta = line.choices[0].delta
                content = delta.get("content", "")
                full_response += content
            self.add(f"assistant:{full_response}")
        except Exception as e:
            print("Errore nel completamento:", e)
            full_response = "error"
        return full_response
