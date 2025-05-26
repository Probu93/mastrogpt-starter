import re, os, requests as req

MODEL = "phi4:14b"

# Definisco il form per customizzare il puzzle
FORM = [
    {
        "name": "pieces",
        "label": "Which pieces to include (e.g. K,Q,B,N)?",
        "type": "text",
        "required": True
    },
    {
        "name": "difficulty",
        "label": "Select difficulty: easy, medium, hard",
        "type": "radio",
        "options": ["easy", "medium", "hard"],
        "required": True
    }
]

def chat(args, inp):
    host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
    auth = args.get("AUTH", os.getenv("AUTH"))
    url = f"https://{auth}@{host}/api/generate"
    msg = {"model": MODEL, "prompt": inp, "stream": False}
    res = req.post(url, json=msg).json()
    out = res.get("response", "error")
    return out

def extract_fen(out):
    pattern = r"([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+"
    m = re.search(pattern, out, re.MULTILINE)
    return m.group(0) if m else None

def puzzle(args):
    inp = args.get("input", "")
    res = {}

    # Se non c'è input o non c'è il form compilato, mostro il form per farlo compilare
    if not inp or (isinstance(inp, dict) and "form" not in inp):
        res["output"] = "Please customize your chess puzzle."
        res["form"] = FORM
        return res

    # Se ricevo i dati compilati dal form
    if isinstance(inp, dict) and "form" in inp:
        data = inp["form"]
        pieces = data.get("pieces", "")
        difficulty = data.get("difficulty", "")
        # costruisco il prompt per il modello
        prompt = (
            f"Generate a chess puzzle in FEN format "
            f"using pieces: {pieces} "
            f"with difficulty: {difficulty}."
        )
        out = chat(args, prompt)
        fen = extract_fen(out)
        if fen:
            res["chess"] = fen
            res["output"] = "Here is your customized chess puzzle."
        else:
            res["output"] = "Sorry, could not generate a valid puzzle."
        return res

    # fallback output
    res["output"] = "Send 'puzzle' to start customizing your chess puzzle."
    return res

