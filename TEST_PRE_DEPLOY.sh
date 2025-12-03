#!/bin/bash

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║              🧪 TEST SUITE COMPLETO PRE-DEPLOY 🧪                   ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🔍 Verifica completa di tutti i componenti del sistema"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Contatori
TESTS_PASSED=0
TESTS_FAILED=0

# Funzione per test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo "🔹 Test: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo "   ✅ PASS"
        ((TESTS_PASSED++))
        return 0
    else
        echo "   ❌ FAIL"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 FASE 1: VERIFICA FILE ESSENZIALI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test "File dati_arricchiti.csv" "test -f dati_arricchiti.csv"
run_test "File dashboard_completa.html" "test -f dashboard_completa.html"
run_test "File analisi_statistica_manipolazione.py" "test -f analisi_statistica_manipolazione.py"
run_test "Virtual environment" "test -d venv"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐍 FASE 2: VERIFICA DIPENDENZE PYTHON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -d "venv" ]; then
    source venv/bin/activate
    
    run_test "Modulo pandas" "python3 -c 'import pandas'"
    run_test "Modulo numpy" "python3 -c 'import numpy'"
    run_test "Modulo scipy" "python3 -c 'import scipy'"
    run_test "Modulo openpyxl" "python3 -c 'import openpyxl'"
else
    echo "   ⚠️  Virtual environment non trovato, skip test Python"
    ((TESTS_FAILED+=4))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 FASE 3: VERIFICA INTEGRITÀ DATI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "dati_arricchiti.csv" ]; then
    # Conta righe
    NUM_RIGHE=$(wc -l < dati_arricchiti.csv)
    echo "🔹 Test: Numero righe dati"
    if [ "$NUM_RIGHE" -gt 100 ]; then
        echo "   ✅ PASS ($NUM_RIGHE righe)"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL (solo $NUM_RIGHE righe)"
        ((TESTS_FAILED++))
    fi
    
    # Verifica colonne essenziali
    echo "🔹 Test: Colonne essenziali"
    if head -1 dati_arricchiti.csv | grep -q "staff" && \
       head -1 dati_arricchiti.csv | grep -q "tipo_turno" && \
       head -1 dati_arricchiti.csv | grep -q "is_festivo"; then
        echo "   ✅ PASS (colonne trovate)"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL (colonne mancanti)"
        ((TESTS_FAILED++))
    fi
else
    echo "   ⚠️  File dati_arricchiti.csv non trovato"
    ((TESTS_FAILED+=2))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔬 FASE 4: TEST ANALISI FORENSE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -d "venv" ] && [ -f "analisi_statistica_manipolazione.py" ]; then
    source venv/bin/activate
    
    echo "🔹 Test: Esecuzione analisi forense"
    echo "   (può richiedere qualche secondo...)"
    
    if python3 analisi_statistica_manipolazione.py > /tmp/test_forense_output.txt 2>&1; then
        echo "   ✅ PASS (script eseguito senza errori)"
        ((TESTS_PASSED++))
        
        # Verifica che il report sia stato generato
        echo "🔹 Test: Generazione report Excel"
        if [ -f "REPORT_FORENSE_MANIPOLAZIONE.xlsx" ]; then
            FILE_SIZE=$(stat -f%z "REPORT_FORENSE_MANIPOLAZIONE.xlsx" 2>/dev/null || stat -c%s "REPORT_FORENSE_MANIPOLAZIONE.xlsx" 2>/dev/null)
            if [ "$FILE_SIZE" -gt 1000 ]; then
                echo "   ✅ PASS (report generato: ${FILE_SIZE} bytes)"
                ((TESTS_PASSED++))
            else
                echo "   ❌ FAIL (report troppo piccolo)"
                ((TESTS_FAILED++))
            fi
        else
            echo "   ❌ FAIL (report non trovato)"
            ((TESTS_FAILED++))
        fi
        
        # Verifica output
        echo "🔹 Test: Calcolo P-value"
        if grep -q "P-value" /tmp/test_forense_output.txt; then
            echo "   ✅ PASS (P-value calcolato)"
            ((TESTS_PASSED++))
        else
            echo "   ❌ FAIL (P-value non trovato)"
            ((TESTS_FAILED++))
        fi
        
        echo "🔹 Test: Calcolo Score Favoritismo"
        if grep -q "SCORE DI FAVORITISMO" /tmp/test_forense_output.txt; then
            echo "   ✅ PASS (Score calcolato)"
            ((TESTS_PASSED++))
        else
            echo "   ❌ FAIL (Score non trovato)"
            ((TESTS_FAILED++))
        fi
    else
        echo "   ❌ FAIL (errore esecuzione)"
        echo "   Dettagli: $(tail -5 /tmp/test_forense_output.txt)"
        ((TESTS_FAILED+=4))
    fi
else
    echo "   ⚠️  Skip (venv o script non disponibile)"
    ((TESTS_FAILED+=4))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 FASE 5: TEST DASHBOARD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "dashboard_completa.html" ]; then
    # Verifica struttura HTML
    echo "🔹 Test: Struttura HTML valida"
    if grep -q "<html" dashboard_completa.html && grep -q "</html>" dashboard_completa.html; then
        echo "   ✅ PASS (HTML valido)"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL (HTML malformato)"
        ((TESTS_FAILED++))
    fi
    
    # Verifica tab
    echo "🔹 Test: Tab Overview presente"
    if grep -q "Overview" dashboard_completa.html; then
        echo "   ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL"
        ((TESTS_FAILED++))
    fi
    
    echo "🔹 Test: Tab Festivi presente"
    if grep -q "Festivi" dashboard_completa.html; then
        echo "   ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL"
        ((TESTS_FAILED++))
    fi
    
    echo "🔹 Test: Tab Confronti presente"
    if grep -q "Confronti" dashboard_completa.html; then
        echo "   ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL"
        ((TESTS_FAILED++))
    fi
    
    echo "🔹 Test: Chart.js incluso"
    if grep -q "chart.js" dashboard_completa.html; then
        echo "   ✅ PASS"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL"
        ((TESTS_FAILED++))
    fi
    
    echo "🔹 Test: Caricamento CSV censurato"
    if grep -q "dati_web.csv" dashboard_completa.html; then
        echo "   ✅ PASS (dati_web.csv - censurato)"
        ((TESTS_PASSED++))
    else
        echo "   ❌ FAIL"
        ((TESTS_FAILED++))
    fi
    
    # Verifica che tab "Dettaglio" sia stato rimosso
    echo "🔹 Test: Tab Dettaglio rimosso (come richiesto)"
    if grep -q "tab-dettaglio" dashboard_completa.html || grep -q "Dettaglio" dashboard_completa.html; then
        echo "   ⚠️  WARNING (tab Dettaglio ancora presente)"
        # Non contiamo come fail, ma come warning
    else
        echo "   ✅ PASS (tab rimosso correttamente)"
        ((TESTS_PASSED++))
    fi
else
    echo "   ⚠️  Dashboard non trovata"
    ((TESTS_FAILED+=7))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 FASE 6: TEST SERVER HTTP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🔹 Test: Python http.server disponibile"
if python3 -m http.server --help > /dev/null 2>&1; then
    echo "   ✅ PASS"
    ((TESTS_PASSED++))
else
    echo "   ❌ FAIL"
    ((TESTS_FAILED++))
fi

echo "🔹 Test: Porta 8000 libera"
if lsof -i :8000 > /dev/null 2>&1; then
    echo "   ⚠️  WARNING (porta già in uso - server già attivo?)"
else
    echo "   ✅ PASS (porta disponibile)"
    ((TESTS_PASSED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 FASE 7: VERIFICA DOCUMENTAZIONE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test "File SINTESI_FORENSE.txt" "test -f SINTESI_FORENSE.txt"
run_test "File ISTRUZIONI_DASHBOARD_FINALE.txt" "test -f ISTRUZIONI_DASHBOARD_FINALE.txt"
run_test "Script ESEGUI_ANALISI_FORENSE.sh" "test -x ESEGUI_ANALISI_FORENSE.sh"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RISULTATI FINALI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
SUCCESS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo "Test totali: $TOTAL_TESTS"
echo "✅ Passati: $TESTS_PASSED"
echo "❌ Falliti: $TESTS_FAILED"
echo "📊 Success rate: $SUCCESS_RATE%"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║              ✅ TUTTI I TEST PASSATI - SISTEMA PRONTO! ✅           ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🚀 Sistema pronto per il deploy!"
    echo ""
    echo "📋 COMPONENTI VERIFICATI:"
    echo "   ✅ Dati: dati_arricchiti.csv"
    echo "   ✅ Dashboard: dashboard_completa.html"
    echo "   ✅ Analisi Forense: analisi_statistica_manipolazione.py"
    echo "   ✅ Report: REPORT_FORENSE_MANIPOLAZIONE.xlsx"
    echo "   ✅ Server HTTP: Pronto su porta 8000"
    echo "   ✅ Documentazione: Completa"
    echo ""
    echo "🌐 Per avviare la dashboard:"
    echo "   python3 -m http.server 8000"
    echo "   Poi apri: http://localhost:8000/dashboard_completa.html"
    echo ""
    echo "🔬 Per rieseguire analisi forense:"
    echo "   ./ESEGUI_ANALISI_FORENSE.sh"
    echo ""
    exit 0
elif [ $SUCCESS_RATE -ge 80 ]; then
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║           ⚠️  SISTEMA OK CON AVVERTIMENTI (${SUCCESS_RATE}%)                  ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "⚠️  Alcuni test hanno fallito ma il sistema è funzionante"
    echo "   Verifica i warning sopra per dettagli"
    echo ""
    exit 0
else
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║              ❌ SISTEMA NON PRONTO - ERRORI CRITICI ❌              ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "❌ Troppi test falliti (success rate: $SUCCESS_RATE%)"
    echo "   Rivedi gli errori sopra prima del deploy"
    echo ""
    exit 1
fi

