# 🚀 Guida Deploy su Render.com

Guida passo-passo per pubblicare la dashboard HR online e condividerla con tua sorella.

---

## 📋 Prerequisiti

- ✅ Account GitHub (gratuito)
- ✅ Account Render.com (gratuito)
- ✅ Git installato sul computer

---

## 🔐 PASSO 1: Crea Repository GitHub

### 1.1 Crea Nuovo Repository

1. Vai su [github.com](https://github.com)
2. Clicca **"New repository"** (bottone verde)
3. Compila:
   - **Repository name**: `hr-dashboard` (o nome a tua scelta)
   - **Description**: "Dashboard HR per analisi turni"
   - **Visibility**: **Private** ✅ (importante per privacy!)
   - **NON** spuntare "Add README" (lo abbiamo già)
4. Clicca **"Create repository"**

### 1.2 Copia URL Repository

Dopo la creazione, vedrai un URL tipo:
```
https://github.com/TUO_USERNAME/hr-dashboard.git
```

**Copialo!** Ti servirà tra poco.

---

## 💻 PASSO 2: Push Codice su GitHub

### 2.1 Apri Terminale

```bash
# Vai nella cartella del progetto
cd "/Users/radice/Downloads/ROTA Chicca"
```

### 2.2 Inizializza Git (se non già fatto)

```bash
# Inizializza repository
git init

# Aggiungi tutti i file (solo quelli non in .gitignore)
git add .

# Verifica cosa verrà committato
git status
```

**IMPORTANTE**: Verifica che NON ci siano:
- ❌ File con nomi completi
- ❌ PDF originali
- ❌ CSV non censurati

Se vedi file sensibili, sono già esclusi da `.gitignore` ✅

### 2.3 Commit Iniziale

```bash
# Crea commit
git commit -m "Initial commit - HR Dashboard con dati censurati"
```

### 2.4 Push su GitHub

```bash
# Aggiungi remote (SOSTITUISCI con il TUO URL!)
git remote add origin https://github.com/TUO_USERNAME/hr-dashboard.git

# Rinomina branch a main
git branch -M main

# Push!
git push -u origin main
```

Se ti chiede username/password:
- **Username**: Il tuo username GitHub
- **Password**: Usa un **Personal Access Token** (non la password!)
  - Vai su GitHub → Settings → Developer settings → Personal access tokens
  - Genera nuovo token con permessi "repo"

### 2.5 Verifica su GitHub

Vai su `https://github.com/TUO_USERNAME/hr-dashboard`

Dovresti vedere:
- ✅ `dashboard_completa.html`
- ✅ `dati_web.csv` (censurato!)
- ✅ `server.py`
- ✅ `requirements.txt`
- ✅ `render.yaml`
- ✅ `README.md`
- ❌ **NON** dati_arricchiti.csv (originale)
- ❌ **NON** PDF

---

## 🌐 PASSO 3: Deploy su Render.com

### 3.1 Crea Account Render

1. Vai su [render.com](https://render.com)
2. Clicca **"Get Started"**
3. Registrati con:
   - Email
   - **Oppure** "Sign in with GitHub" ✅ (più veloce!)

### 3.2 Connetti GitHub

Se non hai usato "Sign in with GitHub":
1. Vai su **Account Settings**
2. Clicca **"Connect GitHub"**
3. Autorizza Render ad accedere ai tuoi repository

### 3.3 Crea Web Service

1. Dalla dashboard Render, clicca **"New +"** (in alto a destra)
2. Seleziona **"Web Service"**
3. Trova il tuo repository `hr-dashboard`
4. Clicca **"Connect"**

### 3.4 Configurazione (Automatica!)

Render rileverà automaticamente `render.yaml` e configurerà:

- **Name**: `hr-dashboard` (puoi cambiarlo)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python server.py`
- **Plan**: **Free** ✅

**NON devi cambiare nulla!** Render usa `render.yaml` automaticamente.

### 3.5 Deploy!

1. Clicca **"Create Web Service"**
2. Render inizierà il deploy (2-3 minuti)
3. Vedrai log in tempo reale:
   ```
   Installing dependencies...
   ✅ pandas installed
   ✅ numpy installed
   ✅ scipy installed
   Starting server...
   ✅ Server running on port 10000
   ```

### 3.6 Ottieni URL

Quando il deploy è completo, vedrai:
```
✅ Live at: https://hr-dashboard-xxxx.onrender.com
```

**Questo è il tuo URL pubblico!** 🎉

---

## 👥 PASSO 4: Condividi con Tua Sorella

### 4.1 Invia URL

Manda a tua sorella:
```
https://hr-dashboard-xxxx.onrender.com
```

### 4.2 Istruzioni per Lei

**Dashboard HR - Istruzioni d'Uso**

1. Apri il link nel browser
2. Vedrai 5 tab:
   - **Overview**: Statistiche generali
   - **Festivi**: Distribuzione festivi lavorati
   - **Confronti**: Confronta 2-6 staff
   - **Grafici**: Visualizzazioni
   - **Equità**: Indici CV

3. **Privacy**: Nomi censurati (3 lettere)
   - VIS = Vissani
   - PAG = Pagano
   - PAC = Pacini
   - TAM = Tamberi
   - CIR = Circelli
   - MOR = Morale

4. **Confronti Multi-Staff**:
   - Spunta 2+ checkbox
   - Clicca "Aggiorna Confronto"
   - Vedi tabella e grafico radar

5. **Tutti i calcoli**: JavaScript Math puro (no AI)

---

## 🔄 PASSO 5: Aggiornamenti Futuri

### Se Modifichi Qualcosa Localmente

```bash
# 1. Salva modifiche
git add .
git commit -m "Descrizione modifiche"

# 2. Push su GitHub
git push

# 3. Render rileverà automaticamente e ri-deploya!
```

Render fa **auto-deploy** ad ogni push su GitHub! 🚀

---

## 🆓 Piano Gratuito Render

### Cosa Include (GRATIS)
- ✅ 750 ore/mese (sufficiente!)
- ✅ HTTPS automatico
- ✅ Auto-deploy da GitHub
- ✅ Nessuna carta di credito richiesta

### Limitazioni
- ⏱️ Server si "addormenta" dopo 15 min inattività
- 🐌 Primo caricamento dopo sleep: 30-60 secondi
- 🔄 Poi veloce come sempre

**Soluzione**: Basta aspettare 30 sec al primo accesso! ✅

---

## 🧪 PASSO 6: Test Post-Deploy

### 6.1 Verifica Dashboard

1. Apri URL Render
2. Controlla che si carichi la dashboard
3. Verifica che i dati siano censurati (VIS, PAG, ecc.)
4. Prova a cambiare tab
5. Prova confronto multi-staff

### 6.2 Test Completo

```bash
# Localmente, esegui test
./TEST_PRE_DEPLOY.sh

# Dovrebbe mostrare:
# ✅ TUTTI I TEST PASSATI - SISTEMA PRONTO!
```

---

## 🔒 Sicurezza e Privacy

### ✅ Cosa È Online
- Dashboard HTML (solo frontend)
- Dati censurati (3 lettere)
- Script analisi (senza dati sensibili)

### ❌ Cosa NON È Online
- Nomi completi
- PDF originali
- CSV non censurati
- Report Excel con dati completi

### 🔐 Repository Privato
- Solo tu puoi vedere il codice su GitHub
- Solo chi ha il link Render può vedere la dashboard
- Nessun motore di ricerca indicizzerà il sito

---

## 🆘 Troubleshooting

### Problema: "Application failed to respond"

**Soluzione**:
1. Vai su Render Dashboard
2. Clicca sul tuo servizio
3. Vai su "Logs"
4. Cerca errori in rosso
5. Spesso è solo il primo avvio lento (aspetta 1-2 min)

### Problema: "Module not found"

**Soluzione**:
1. Verifica che `requirements.txt` sia committato
2. Vai su Render → "Manual Deploy" → "Clear build cache & deploy"

### Problema: Dashboard non carica dati

**Soluzione**:
1. Verifica che `dati_web.csv` sia su GitHub
2. Apri DevTools browser (F12) → Console
3. Cerca errori JavaScript
4. Verifica che il file CSV sia accessibile: `https://TUO_URL/dati_web.csv`

### Problema: Server si addormenta

**Normale!** Piano gratuito Render.
- Primo accesso dopo 15 min: 30-60 sec
- Poi veloce normalmente

**Soluzione Pro** (opzionale, $7/mese):
- Upgrade a piano Starter
- Server sempre attivo

---

## 📊 Monitoraggio

### Render Dashboard

Vai su [dashboard.render.com](https://dashboard.render.com)

Puoi vedere:
- ✅ Status servizio (Running/Sleeping)
- 📊 Uso risorse
- 📝 Log in tempo reale
- 🔄 Deploy history

### Log in Tempo Reale

```bash
# Dalla dashboard Render
Logs → Tail logs
```

Vedrai:
```
Server attivo su porta 10000
GET /dashboard_completa.html 200
GET /dati_web.csv 200
```

---

## 🎉 Checklist Finale

Prima di condividere con tua sorella:

- [ ] ✅ Repository GitHub creato (privato)
- [ ] ✅ Codice pushato su GitHub
- [ ] ✅ Dati censurati (solo 3 lettere)
- [ ] ✅ File sensibili NON committati
- [ ] ✅ Deploy Render completato
- [ ] ✅ Dashboard accessibile da URL
- [ ] ✅ Dati si caricano correttamente
- [ ] ✅ Tab funzionano tutti
- [ ] ✅ Confronti multi-staff funziona
- [ ] ✅ Test locale passato (TEST_PRE_DEPLOY.sh)

---

## 📞 Supporto

### Documentazione Render
- [Render Docs](https://render.com/docs)
- [Python Deploy Guide](https://render.com/docs/deploy-python)

### File di Riferimento
- `README.md` - Documentazione completa
- `SINTESI_FORENSE.txt` - Risultati analisi
- `TEST_PRE_DEPLOY.sh` - Test suite

---

## 🚀 Riepilogo Comandi

```bash
# 1. Inizializza e push GitHub
cd "/Users/radice/Downloads/ROTA Chicca"
git init
git add .
git commit -m "Initial commit - HR Dashboard"
git remote add origin https://github.com/TUO_USERNAME/hr-dashboard.git
git branch -M main
git push -u origin main

# 2. Vai su render.com
# 3. New + → Web Service → Connetti repo
# 4. Deploy automatico!
# 5. Condividi URL con tua sorella

# 6. Per aggiornamenti futuri
git add .
git commit -m "Aggiornamento"
git push
# Render auto-deploya! 🚀
```

---

**Tempo totale stimato**: 15-20 minuti ⏱️

**Costo**: GRATIS 💰

**Difficoltà**: Facile ⭐⭐☆☆☆

---

🎉 **Buon deploy!** 🎉

