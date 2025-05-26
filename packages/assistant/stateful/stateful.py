import chat
import history

def stateful(args):
    inp = args.get("input", "")
    out = f"Hello from {chat.MODEL}"
    res = {}

    if inp != "":
        # Crea un'istanza della chat
        ch = chat.Chat(args)

        # Carica la cronologia precedente
        hi = history.History(args)
        hi.load(ch)

        # Aggiungi messaggio utente
        msg = f"user:{inp}"
        ch.add(msg)

        # Ottieni la risposta del modello
        out = ch.complete()

        # Salva lo scambio nella cronologia
        hi.save(msg)
        hi.save(f"assistant:{out}")

        # Includi lo stato (id della cronologia) nella risposta
        res["state"] = hi.id()

    # Risultato da restituire (solo valori JSON serializzabili)
    res["output"] = out
    return res
