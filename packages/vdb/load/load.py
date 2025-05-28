import re
import requests
from bs4 import BeautifulSoup
import vdb

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB.
Start with * to do a vector search in the DB.
Start with ! to remove text with a substring.
"""

def split_utf8_chunks(text, max_bytes=1024):
    chunks = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if len(candidate.encode("utf-8")) > max_bytes:
            if current:
                chunks.append(current)
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks

def load(args):
  
    collection = args.get("COLLECTION", "default")
    out = f"{USAGE}Current colletion is {collection}"
    inp = str(args.get('input', ""))
    db = vdb.VectorDB(args)
  
    if inp.startswith("*"):
        if len(inp) == 1:
            out = "please specify a search string"
        else:
            res = db.vector_search(inp[1:])
            if len(res) > 0:
                out = f"Found:\n"
                for i in res:
                    out += f"({i[0]:.2f}) {i[1]}\n"
            else:
                out = "Not found"
    elif inp.startswith("!"):
        count = db.remove_by_substring(inp[1:])
        out = f"Deleted {count} records."
    elif inp != '':
        if inp.startswith("https://"):
            try:
                response = requests.get(inp)
                response.raise_for_status()
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(separator=' ', strip=True)
                tokens = re.findall(r'\b\w+\b', text)
                cleaned_text = ' '.join(tokens)
                chunks = split_utf8_chunks(cleaned_text, max_bytes=1024)
                
                inserted_ids = []
                for chunk in chunks:
                    res = db.insert(chunk)
                    inserted_ids.extend(res.get("ids", []))
                
                out = "Inserted from URL: "
                out += " ".join(map(str, inserted_ids))
            except Exception as e:
                out = f"Error loading from URL: {e}"
        else:
            res = db.insert(inp)
            out = "Inserted " 
            out += " ".join([str(x) for x in res.get("ids", [])])

    return {"output": out}
