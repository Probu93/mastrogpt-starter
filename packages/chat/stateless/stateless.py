import os
import requests as req
import json
import socket
import traceback

MODEL = "llama3.1:8b"
# MODEL = "deepseek-r1:32b"

def url(args):
    #TODO:E2.1
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
    auth = args.get("AUTH", os.getenv("AUTH"))
    #END TODO
    base = f"https://{auth}@{host}"
    return f"{base}/api/generate"

def stream(args, lines):
    sock = args.get("STREAM_HOST")
    port = int(args.get("STREAM_PORT"))
    out = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sock, port))
        try:
            for line in lines:
                data = json.loads(line.decode("utf-8"))
                response = data.get("response", "error")
                out += response
                msg = {"output": response}
                s.sendall(json.dumps(msg).encode("utf-8"))
        except Exception as e:
            traceback.print_exc()
            out = str(e)
    return out

def stateless(args):
    global MODEL
    llm = url(args)
    out = f"Welcome to {MODEL}"
    inp = args.get("input", "")
    if inp != "":
        if inp.lower() == "llmama":
            MODEL = "llama3.1:8b"
            inp = "who are you"
        elif inp.lower() == "deepseek":
            MODEL = "deepseek-r1:32b"
            inp = "who are you"

        msg = { "model": MODEL, "prompt": inp, "stream": True }
        lines = req.post(llm, json=msg, stream=True).iter_lines()
        out = stream(args, lines)
    return { "output": out, "streaming": True }
