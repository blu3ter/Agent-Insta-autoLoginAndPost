#!/bin/bash

# 1. Configurazione delle variabili (caricate dal file .env)
if [ -f .env ]; then
    source .env
else
    echo "❌ Errore: File .env non trovato! Crea un file .env partendo da .env.example"
    exit 1
fi

# Controllo che le variabili necessarie non siano vuote
if [ -z "$ACCOUNT_ID" ] || [ -z "$ACCESS_TOKEN" ] || [ -z "$IMAGE_URL" ]; then
    echo "❌ Errore: Assicurati che ACCOUNT_ID, ACCESS_TOKEN e IMAGE_URL siano definiti nel file .env!"
    exit 1
fi

echo "⏳ Creazione del container in corso..."

# 2. Chiamata per creare il container (salviamo la risposta in una variabile)
RESPONSE=$(curl -s -X POST "https://graph.instagram.com/v23.0/$ACCOUNT_ID/media" \
     -d "image_url=$IMAGE_URL" \
     -d "access_token=$ACCESS_TOKEN")

# 3. Estraiamo l'ID dal JSON usando jq
CONTAINER_ID=$(echo "$RESPONSE" | jq -r '.id')

# Controllo per sicurezza: se l'ID è vuoto o null, c'è stato un errore
if [ "$CONTAINER_ID" == "null" ] || [ -z "$CONTAINER_ID" ]; then
    echo "❌ Errore nella creazione del container. Risposta del server:"
    echo "$RESPONSE"
    exit 1
fi

echo "✅ Container creato! ID: $CONTAINER_ID"

#da il tempo ai servere ig di caricare il container con il tuo post, prima di pubblicarlo
echo "⏳ Attendo 10 secondi per l'elaborazione dell'immagine da parte di Instagram..."
sleep 10  
echo "🚀 Pubblicazione in corso..."

# 4. Chiamata per pubblicare il container
PUBLISH_RESPONSE=$(curl -s -X POST "https://graph.instagram.com/v23.0/$ACCOUNT_ID/media_publish" \
     -d "creation_id=$CONTAINER_ID" \
     -d "access_token=$ACCESS_TOKEN")

echo "✅ Post pubblicato! Risposta del server:"
echo "$PUBLISH_RESPONSE"