#!/bin/bash

# Questo script funge da "lanciatore" per il bot in Python.

# Verifica se l'ambiente virtuale esiste
if [ ! -d "venv" ]; then
    echo "❌ Errore: L'ambiente virtuale (venv) non è stato ancora creato."
    echo ""
    echo "Per crearlo, esegui questi comandi nel terminale:"
    echo "1. sudo apt update && sudo apt install -y python3-venv"
    echo "2. python3 -m venv venv"
    echo "3. source venv/bin/activate"
    echo "4. pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Attiva l'ambiente virtuale ed esegue il bot Python passando eventuali argomenti
source venv/bin/activate
python3 main.py "$@"