import json
import sys
import google.generativeai as genai

def generate_content(topic, api_key):
    print("🧠 Sto generando il testo e i prompt con Gemini...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Sei un social media manager. Crea un post per Instagram sul tema: "{topic}".
    L'output DEVE essere in formato JSON valido con questa esatta struttura:
    {{
        "caption": "Il testo del post con gli hashtag",
        "image_prompts": [
            "prompt in inglese dettagliato per l'immagine 1 (stile fotografico)",
            "prompt in inglese dettagliato per l'immagine 2 (stile fotografico)",
            "prompt in inglese dettagliato per l'immagine 3 (stile fotografico)"
        ]
    }}
    Non aggiungere altro testo fuori dal JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        
        data = json.loads(text.strip())
        return data
    except Exception as e:
        print("❌ Errore nella generazione JSON con Gemini:", e)
        print("Dettagli dell'errore:", str(e))
        sys.exit(1)
