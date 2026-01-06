#!/bin/bash

# Script per configurare l'ambiente virtuale e avviare la dashboard

echo "🚀 Configurazione PlayTheEvent Analytics Dashboard"
echo "=================================================="

# Verifica se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installalo prima di proseguire."
    exit 1
fi

echo "✓ Python trovato: $(python3 --version)"

# Crea virtual environment
echo ""
echo "📦 Creazione virtual environment..."
python3 -m venv venv

# Attiva il virtual environment
echo "✓ Virtual environment creato"
echo ""
echo "🔧 Attivazione virtual environment..."
source venv/bin/activate

# Aggiorna pip
echo "📥 Aggiornamento pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Installa i requirements
echo "📥 Installazione dipendenze..."
pip install -r requirements.txt

echo ""
echo "✓ Installazione completata!"
echo ""
echo "📊 Avvio della dashboard..."
echo "=================================================="
echo "Dashboard disponibile su: http://localhost:8050"
echo "Premi Ctrl+C per fermare il server"
echo "=================================================="
echo ""

# Avvia la dashboard
python3 analytics_dashboard.py
