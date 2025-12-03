# 📊 HR Dashboard - Analisi Turni 2025

Dashboard interattiva per l'analisi statistica dei turni di lavoro con identificazione di anomalie e pattern sospetti.

![Dashboard Preview](https://img.shields.io/badge/Status-Production-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-Private-red)

## 🎯 Caratteristiche

### 📊 Dashboard Interattiva
- **5 Tab Principali**: Overview, Festivi, Confronti Multi-Staff, Grafici, Indici Equità
- **Visualizzazioni**: Chart.js per grafici dinamici
- **Filtri**: Analisi per periodo, staff, tipo turno
- **Privacy**: Nomi censurati (prime 3 lettere)

### 🔬 Analisi Statistica Forense
- **Test Chi-Quadrato**: Verifica casualità distribuzione
- **Z-Score Analysis**: Identificazione outlier statistici
- **Score Favoritismo**: Metrica matematica per identificare trattamenti preferenziali
- **Pattern Recognition**: Analisi riposi consecutivi e turni comodi/scomodi

### 📈 Metriche Analizzate
- Turni lavorati (normali, festivi, weekend)
- Ore totali e media ore/turno
- Riposi consecutivi (2, 3, 4+ giorni)
- Ferie godute
- Distribuzione per giorno settimana
- Coefficient of Variation (CV) per equità

## 🚀 Deploy su Render.com

### Prerequisiti
- Account GitHub
- Account Render.com (gratuito)

### Passo 1: Push su GitHub

```bash
# Inizializza repository
git init
git add .
git commit -m "Initial commit - HR Dashboard"

# Aggiungi remote (sostituisci con il tuo repo)
git remote add origin https://github.com/TUO_USERNAME/hr-dashboard.git
git branch -M main
git push -u origin main
```

### Passo 2: Deploy su Render

1. Vai su [render.com](https://render.com)
2. Clicca **"New +"** → **"Web Service"**
3. Connetti il tuo repository GitHub
4. Render rileverà automaticamente `render.yaml`
5. Clicca **"Create Web Service"**
6. Attendi il deploy (2-3 minuti)
7. Accedi all'URL fornito (es: `https://hr-dashboard-xxxx.onrender.com`)

### Configurazione Automatica

Il file `render.yaml` configura automaticamente:
- ✅ Ambiente Python 3.11
- ✅ Installazione dipendenze (`requirements.txt`)
- ✅ Avvio server HTTP (`server.py`)
- ✅ Porta dinamica per Render

## 💻 Uso Locale

### Installazione

```bash
# Clona repository
git clone https://github.com/TUO_USERNAME/hr-dashboard.git
cd hr-dashboard

# Crea virtual environment
python3 -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt
```

### Avvio Dashboard

```bash
# Metodo 1: Server Python personalizzato
python3 server.py

# Metodo 2: Server HTTP semplice
python3 -m http.server 8000

# Apri browser
open http://localhost:8000
```

### Esegui Analisi Forense

```bash
# Attiva virtual environment
source venv/bin/activate

# Esegui analisi
python3 analisi_statistica_manipolazione.py

# Oppure usa lo script
./ESEGUI_ANALISI_FORENSE.sh
```

## 📁 Struttura File

```
hr-dashboard/
├── dashboard_completa.html      # Dashboard principale
├── dati_web.csv                 # Dati censurati (prime 3 lettere)
├── server.py                    # Server HTTP per Render
├── requirements.txt             # Dipendenze Python
├── render.yaml                  # Configurazione Render.com
├── .gitignore                   # File esclusi da Git
├── README.md                    # Questo file
│
├── analisi_statistica_manipolazione.py  # Analisi forense
├── censura_nomi.py              # Script censura nomi
├── ESEGUI_ANALISI_FORENSE.sh    # Launcher analisi
├── TEST_PRE_DEPLOY.sh           # Test suite completo
│
└── SINTESI_FORENSE.txt          # Report risultati (non committato)
```

## 🔒 Privacy e Sicurezza

### Dati Censurati
- ✅ Nomi staff ridotti a **3 lettere** (es: VISSANI → VIS)
- ✅ File originali **NON inclusi** in Git (`.gitignore`)
- ✅ Solo dati aggregati e anonimi online

### File NON Committati
- PDF originali con nomi completi
- CSV non censurati
- Report Excel con dati sensibili
- Log e file temporanei

## 📊 Risultati Analisi Forense

### Test Chi-Quadrato
- **Chi²**: 16.1735
- **P-value**: 0.006366 (0.64%)
- **Conclusione**: Evidenza forte di distribuzione NON casuale

### Staff Identificati
1. **PAC**: Score 82.30 (anomalia significativa, Z=1.71)
2. **MOR**: Score 78.29 (turni comodi: 55.8%)
3. **VIS**: Score 29.87 (più turni scomodi)

### Interpretazione
- Probabilità < 1% che distribuzione sia casuale
- Pattern riposi consecutivi sospetti per PAC (7 sequenze lunghe)
- Disparità matematicamente provata (52.43 punti tra PAC e VIS)

## 🔬 Metodi Matematici

### Test Statistici
- **Chi-Quadrato**: `scipy.stats.chi2_contingency()`
- **Z-Score**: `scipy.stats.norm.cdf()`
- **CV**: `(std / mean) × 100`

### Formula Score Favoritismo
```python
Score_Raw = (Turni_Comodi × 2) + (Seq_Lunghe × 3) - (Turni_Scomodi × 2)
Score_Norm = (Score_Raw / N_Turni) × 100
```

### Criteri Turni
- **Comodi**: Entrata ≥ 07:00, Uscita ≤ 17:00, Non festivi/weekend
- **Scomodi**: Entrata < 05:00, Uscita > 19:00, Festivi, Weekend

## 🧪 Test Pre-Deploy

```bash
# Esegui test completo
chmod +x TEST_PRE_DEPLOY.sh
./TEST_PRE_DEPLOY.sh

# Verifica:
# ✅ File essenziali
# ✅ Dipendenze Python
# ✅ Integrità dati
# ✅ Analisi forense
# ✅ Dashboard HTML
# ✅ Server HTTP
# ✅ Documentazione
```

## 📝 Note Importanti

### Contesto Dati
- **Periodo**: Anno 2025 completo (52 settimane)
- **Staff**: 6 persone (nomi censurati)
- **Turni analizzati**: 1348
- **Eventi**: Trasferimento 30 settembre, congedo lungo per 1 staff

### Limitazioni
- Analisi basata su dati forniti
- Censura nomi per privacy
- Alcuni periodi potrebbero avere dati incompleti

## 🛠️ Tecnologie

- **Frontend**: HTML5, CSS3, JavaScript
- **Grafici**: Chart.js 4.4.0
- **CSV Parsing**: PapaParse 5.4.1
- **Backend**: Python 3.11+
- **Analisi**: pandas, numpy, scipy
- **Deploy**: Render.com
- **VCS**: Git/GitHub

## 📧 Supporto

Per domande o problemi:
1. Verifica la documentazione
2. Esegui `TEST_PRE_DEPLOY.sh`
3. Controlla i log del server
4. Rivedi `SINTESI_FORENSE.txt`

## 📜 License

**Private** - Solo per uso interno

---

## 🚀 Quick Start

```bash
# 1. Clona e installa
git clone https://github.com/TUO_USERNAME/hr-dashboard.git
cd hr-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Avvia server
python3 server.py

# 3. Apri browser
open http://localhost:8000

# 4. Esplora dashboard!
```

---

**Creato con**: Python 🐍 | Chart.js 📊 | Matematica rigorosa 🔬

**Deploy**: Render.com 🚀 | Privacy garantita 🔒
