#!/bin/bash
# Script per avviare la dashboard con server HTTP locale

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║       🚀 AVVIO DASHBOARD HR CON SERVER LOCALE 🚀                    ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "✅ Avvio server HTTP locale sulla porta 8000..."
echo "🌐 La dashboard si aprirà automaticamente nel browser"
echo ""
echo "⚠️  Per fermare il server: premi CTRL+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Avvia server in background
python3 -m http.server 8000 &
SERVER_PID=$!

# Aspetta che il server si avvii
sleep 2

# Apri nel browser
echo "🌐 Apertura dashboard nel browser..."
open "http://localhost:8000/dashboard_finale.html"

echo ""
echo "✅ Dashboard aperta all'indirizzo: http://localhost:8000/dashboard_finale.html"
echo ""
echo "🔒 Tutti i calcoli sono JavaScript Math puro (zero AI)"
echo "📊 Esplora i 5 tab per vedere tutte le analisi"
echo ""
echo "⏹️  Per fermare: premi CTRL+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Aspetta che l'utente fermi il server
wait $SERVER_PID

