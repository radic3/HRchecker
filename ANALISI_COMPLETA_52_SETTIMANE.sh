#!/bin/bash
# Script per analisi HR completa su tutte le 52 settimane

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║   ANALISI HR COMPLETA - ANNO 2025 (52 SETTIMANE)                    ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "🔧 Attivazione ambiente virtuale..."
source venv/bin/activate

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PASSO 1: ESTRAZIONE DATI DA 54 PDF (52 SETTIMANE)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 extract_turni_completo.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PASSO 2: ANALISI HR EQUITÀ E COMPLIANCE - ANNO COMPLETO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 analisi_hr_anno_completo.py

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║   ✅ ANALISI COMPLETATA!                                            ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 FILE GENERATI:"
echo "   • REPORT_HR_ANNO_COMPLETO_2025.xlsx (10 fogli)"
echo "   • turni_completi_52_settimane.csv (1381 turni)"
echo "   • REPORT_FINALE_HR.txt (riepilogo)"
echo ""
echo "📋 DATI ANALIZZATI:"
echo "   • 52 settimane"
echo "   • 1381 turni"
echo "   • 6 membri staff"
echo "   • 12 anomalie identificate"
echo ""
echo "🎯 PROSSIMO PASSO:"
echo "   Apri REPORT_HR_ANNO_COMPLETO_2025.xlsx"
echo "   Leggi REPORT_FINALE_HR.txt per il riepilogo"
echo ""

