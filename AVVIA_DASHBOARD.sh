#!/bin/bash
# Script per avviare la Dashboard HR Interattiva

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║          🚀 AVVIO DASHBOARD HR INTERATTIVA 🚀                       ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "🔧 Attivazione ambiente Python..."
source venv/bin/activate

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 SCELTA DASHBOARD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Hai 2 opzioni:"
echo ""
echo "1. 🌐 Dashboard HTML Standalone"
echo "   • Si apre direttamente nel browser"
echo "   • Nessun server richiesto"
echo "   • Grafici interattivi con Chart.js"
echo "   • Confronti e filtri in tempo reale"
echo ""
echo "2. 🖥️  Dashboard Python Flask"
echo "   • Server web locale"
echo "   • API REST per integrazioni"
echo "   • Calcoli Python certificati"
echo "   • Più funzionalità avanzate"
echo ""
read -p "Scegli (1 o 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "🌐 Apertura Dashboard HTML..."
    
    # Apri nel browser
    if command -v open &> /dev/null; then
        open dashboard_hr.html
    elif command -v xdg-open &> /dev/null; then
        xdg-open dashboard_hr.html
    else
        echo "📄 Apri manualmente: dashboard_hr.html nel tuo browser"
    fi
    
    echo ""
    echo "✅ Dashboard HTML aperta nel browser!"
    echo "📊 Tutti i calcoli sono eseguiti in JavaScript puro (matematica deterministica)"
    echo ""
    
elif [ "$choice" == "2" ]; then
    echo ""
    echo "🖥️  Avvio server Flask..."
    echo ""
    
    python3 dashboard_server.py
    
else
    echo ""
    echo "❌ Scelta non valida. Riprova con 1 o 2."
fi

