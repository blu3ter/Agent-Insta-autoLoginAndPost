import requests
import time
import sys

def create_carousel_item(image_url, account_id, access_token):
    url = f"https://graph.instagram.com/v23.0/{account_id}/media"
    payload = {
        "image_url": image_url,
        "is_carousel_item": "true",
        "access_token": access_token
    }
    res = requests.post(url, data=payload)
    data = res.json()
    if 'id' in data:
        return data['id']
    else:
        print("❌ Errore creazione item carosello:", data)
        sys.exit(1)



def publish_carousel(item_ids, caption, account_id, access_token):
    print("⏳ Attendo 15 secondi per dare tempo a Instagram di scaricare ed elaborare le 3 immagini...")
    time.sleep(15)
    
    print("🔄 Creazione del container Carosello...")
    url_container = f"https://graph.instagram.com/v23.0/{account_id}/media"
    payload_container = {
        "media_type": "CAROUSEL",
        "children": ",".join(item_ids),
        "caption": caption,
        "access_token": access_token
    }
    res_container = requests.post(url_container, data=payload_container)
    container_data = res_container.json()
    
    if 'id' not in container_data:
        print("❌ Errore creazione container carosello:", container_data)
        sys.exit(1)
        
    container_id = container_data['id']
    print(f"✅ Container carosello creato: {container_id}")
    
    print("🚀 Pubblicazione finale in corso...")
    url_publish = f"https://graph.instagram.com/v23.0/{account_id}/media_publish"
    payload_publish = {
        "creation_id": container_id,
        "access_token": access_token
    }
    res_publish = requests.post(url_publish, data=payload_publish)
    publish_data = res_publish.json()
    
    if 'id' in publish_data:
        print(f"🎉 Pubblicazione completata! ID del post: {publish_data['id']}")
    else:
        print("❌ Errore nella pubblicazione:", publish_data)
        sys.exit(1)
