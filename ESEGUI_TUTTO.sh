#!/bin/bash
# Script per eseguire tutta l'estrazione e analisi dei turni

echo "================================================"
echo "  ANALISI TURNI ROTA - SISTEMA COMPLETO"
echo "================================================"
echo ""

# Vai nella directory corretta
cd "$(dirname "$0")"

# Attiva virtual environment
echo "🔧 Attivazione ambiente virtuale..."
source venv/bin/activate

# Esegui estrazione avanzata
echo ""
echo "================================================"
echo "  PASSO 1: ESTRAZIONE TURNI DAI PDF"
echo "================================================"
python3 extract_turni_avanzato.py

# Esegui analisi avanzata
echo ""
echo "================================================"
echo "  PASSO 2: ANALISI AVANZATA DEI DATI"
echo "================================================"
python3 analisi_avanzata.py

# Esegui analisi HR Equità e Compliance
echo ""
echo "================================================"
echo "  PASSO 3: ANALISI HR EQUITÀ E COMPLIANCE"
echo "================================================"
python3 analisi_equita_hr.py

# Mostra file generati
echo ""
echo "================================================"
echo "  ✅ PROCESSO COMPLETATO!"
echo "================================================"
echo ""
echo "📁 File generati nella cartella:"
pwd
echo ""
echo "📊 File principali:"
echo "   • turni_dettagliati.csv - Dati grezzi"
echo "   • turni_dettagliati.xlsx - Dati organizzati"
echo "   • REPORT_FINALE_COMPLETO.xlsx - Report con analisi"
echo ""
echo "💡 Apri REPORT_FINALE_COMPLETO.xlsx per vedere tutte le statistiche!"
echo ""

