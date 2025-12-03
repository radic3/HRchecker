#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# COMANDI DEPLOY - Copia e incolla nel terminale
# ═══════════════════════════════════════════════════════════════════

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║              📋 COMANDI DEPLOY GITHUB + RENDER 📋                   ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  IMPORTANTE: Prima di eseguire questi comandi:"
echo "   1. Crea repository su GitHub (privato!)"
echo "   2. Copia l'URL del repository"
echo "   3. Sostituisci TUO_USERNAME con il tuo username GitHub"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Vai nella cartella del progetto
# ═══════════════════════════════════════════════════════════════════

echo "📁 STEP 1: Vai nella cartella del progetto"
echo ""
echo "cd \"/Users/radice/Downloads/ROTA Chicca\""
echo ""

cd "/Users/radice/Downloads/ROTA Chicca"

# ═══════════════════════════════════════════════════════════════════
# STEP 2: Inizializza Git
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 STEP 2: Inizializza Git"
echo ""
echo "git init"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 3: Aggiungi file (solo quelli non in .gitignore)
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 STEP 3: Aggiungi file"
echo ""
echo "git add ."
echo ""
echo "⚠️  Verifica che NON ci siano file sensibili:"
echo "git status"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 4: Commit
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💾 STEP 4: Commit"
echo ""
echo "git commit -m \"Initial commit - HR Dashboard con dati censurati\""
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 5: Aggiungi remote (SOSTITUISCI TUO_USERNAME!)
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 STEP 5: Aggiungi remote GitHub"
echo ""
echo "⚠️  SOSTITUISCI 'TUO_USERNAME' con il tuo username GitHub!"
echo ""
echo "git remote add origin https://github.com/TUO_USERNAME/hr-dashboard.git"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 6: Rinomina branch a main
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌿 STEP 6: Rinomina branch"
echo ""
echo "git branch -M main"
echo ""

# ═══════════════════════════════════════════════════════════════════
# STEP 7: Push su GitHub
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 STEP 7: Push su GitHub"
echo ""
echo "git push -u origin main"
echo ""
echo "⚠️  Se ti chiede username/password:"
echo "   • Username: Il tuo username GitHub"
echo "   • Password: Usa un Personal Access Token (non la password!)"
echo "     → GitHub → Settings → Developer settings → Personal access tokens"
echo ""

# ═══════════════════════════════════════════════════════════════════
# RIEPILOGO COMANDI
# ═══════════════════════════════════════════════════════════════════

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 RIEPILOGO COMANDI (copia tutto insieme):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
cat << 'EOF'
cd "/Users/radice/Downloads/ROTA Chicca"
git init
git add .
git status  # Verifica file
git commit -m "Initial commit - HR Dashboard con dati censurati"
git remote add origin https://github.com/TUO_USERNAME/hr-dashboard.git
git branch -M main
git push -u origin main
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 DOPO IL PUSH SU GITHUB:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Vai su render.com"
echo "2. Sign up / Login (usa 'Sign in with GitHub')"
echo "3. New + → Web Service"
echo "4. Connetti repository 'hr-dashboard'"
echo "5. Render rileva render.yaml automaticamente"
echo "6. Create Web Service"
echo "7. Attendi 2-3 minuti"
echo "8. Ottieni URL: https://hr-dashboard-xxxx.onrender.com"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ FATTO! Condividi l'URL con tua sorella"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 Per guida dettagliata: leggi DEPLOY_RENDER.md"
echo ""

