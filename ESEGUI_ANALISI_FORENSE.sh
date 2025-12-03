#!/bin/bash

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║      🔬 ANALISI STATISTICA FORENSE - MANIPOLAZIONE TURNI 🔬         ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🔍 Identificazione manipolazioni con metodi matematici rigorosi"
echo "   • Test Chi-Quadrato (scipy.stats)"
echo "   • Z-Score Analysis"
echo "   • Pattern Recognition"
echo "   • Score di Favoritismo"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Attiva virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment attivato"
else
    echo "❌ Virtual environment non trovato!"
    echo "   Esegui prima: python3 -m venv venv && source venv/bin/activate && pip install pandas numpy scipy openpyxl"
    exit 1
fi

echo ""
echo "🚀 Avvio analisi forense..."
echo ""

# Esegui analisi
python3 analisi_statistica_manipolazione.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ ANALISI COMPLETATA!"
echo ""
echo "📄 File generati:"
echo "   • REPORT_FORENSE_MANIPOLAZIONE.xlsx (Excel completo)"
echo "   • SINTESI_FORENSE.txt (Sintesi risultati)"
echo ""
echo "📊 Apri i file per vedere:"
echo "   • Test statistici formali"
echo "   • Score di favoritismo per staff"
echo "   • Pattern riposi sospetti"
echo "   • Evidenze matematiche di manipolazione"
echo ""
echo "🔒 Tutti i calcoli: scipy.stats + numpy (ZERO AI)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

