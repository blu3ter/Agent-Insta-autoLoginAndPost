import urllib.parse

def get_images(prompts):
    print("🎨 Generazione immagini tramite Pollinations.ai...")
    image_urls = []
    for i, p in enumerate(prompts):
        encoded_prompt = urllib.parse.quote(p)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
        image_urls.append(url)
        print(f"✅ Immagine {i+1} pronta")
    return image_urls
