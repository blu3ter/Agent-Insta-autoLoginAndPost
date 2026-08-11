import os
import sys
from dotenv import load_dotenv

import gemini_api
import pollinations_api
import instagram_api

def main():
    print("==========================================")
    print(" Benvenuto nell'Instagram Auto-Poster Bot ")
    print("==========================================")
    
    # Caricamento delle variabili d'ambiente dal file .env
    load_dotenv()
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not all([ACCOUNT_ID, ACCESS_TOKEN, GEMINI_API_KEY]):
        print("❌ Errore: Assicurati di aver configurato ACCOUNT_ID, ACCESS_TOKEN e GEMINI_API_KEY nel file .env")
        sys.exit(1)
        
    # Determinazione del topic
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        print(f"📌 Topic ricevuto dagli argomenti: {topic}")
    else:
        topic = input("✍️ Inserisci il topic di oggi: ")
        
    if not topic.strip():
        print("❌ Errore: Il topic non può essere vuoto.")
        sys.exit(1)
        
    # 1. Chiamata a Gemini 1.5 per generare caption e prompt
    content_data = gemini_api.generate_content(topic, GEMINI_API_KEY)
    caption = content_data.get("caption")
    image_prompts = content_data.get("image_prompts", [])
    
    if not caption or not image_prompts:
        print("❌ Errore: Dati generati da Gemini incompleti o non validi.")
        sys.exit(1)
        
    # 2. Generazione delle foto con Pollinations
    image_urls = pollinations_api.get_images(image_prompts)
    
    if not image_urls or len(image_urls) != len(image_prompts):
        print("❌ Errore: Non è stato possibile generare tutte le immagini.")
        sys.exit(1)
        
    # 3. Creazione degli item per il carosello su Instagram
    print("🔄 Creazione degli elementi per il carosello Instagram...")
    item_ids = []
    for i, url in enumerate(image_urls):
        item_id = instagram_api.create_carousel_item(url, ACCOUNT_ID, ACCESS_TOKEN)
        item_ids.append(item_id)
        print(f"✅ Item carosello {i+1} creato (ID: {item_id})")
        
    # 4. Pubblicazione del carosello
    instagram_api.publish_carousel(item_ids, caption, ACCOUNT_ID, ACCESS_TOKEN)

if __name__ == "__main__":
    main()
