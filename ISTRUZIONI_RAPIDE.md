# 🚀 GUIDA RAPIDA - Analisi Turni ROTA

## ✅ Come Iniziare in 30 Secondi

### Apri il Terminale e digita:

```bash
cd "/Users/radice/Downloads/ROTA Chicca"
./ESEGUI_TUTTO.sh
```

**Fatto!** Il sistema analizzerà tutti i 54 PDF e genererà i report.

---

## 📊 Cosa Otterrai

Dopo l'esecuzione (circa 1-2 minuti), avrai questi file:

### 🎯 File Principale: **REPORT_FINALE_COMPLETO.xlsx**

Questo è il file che devi aprire! Contiene:

- ✅ **Dashboard** con i numeri chiave
- ✅ **1381 turni** estratti e organizzati
- ✅ **Ore lavorate** per ogni persona
- ✅ **Statistiche** per settimana e per staff
- ✅ **Orari** più comuni di entrata/uscita
- ✅ **Tipologie** di turno (normale, riposo, ferie, ecc.)
- ✅ **Modifiche** ai turni identificate

---

## 📈 Numeri Chiave Estratti

Dal tuo anno di turni (2025):

| Metrica | Valore |
|---------|--------|
| **Turni Totali** | 1381 |
| **Ore Lavorate** | 5571 ore |
| **Staff Analizzato** | 6 persone |
| **Settimane Coperte** | 52 settimane |
| **Media Ore/Turno** | 6.66 ore |

### 👥 Ore per Persona

| Staff | Ore Totali | N. Turni | Media Ore |
|-------|-----------|----------|-----------|
| CIRCELLI | 1073 h | 160 | 6.71 h |
| TAMBERI | 1039 h | 157 | 6.62 h |
| VISSANI | 999 h | 151 | 6.62 h |
| PAGANO | 978 h | 144 | 6.79 h |
| MORALE | 756.5 h | 113 | 6.69 h |
| PACINI | 725.5 h | 111 | 6.54 h |

---

## 💡 Cosa Fare con i Dati

### Opzione 1: Usa Excel (Facile)
1. Apri `REPORT_FINALE_COMPLETO.xlsx`
2. Naviga tra i vari fogli
3. Usa i filtri per analizzare periodi specifici
4. Crea grafici dai dati pivot

### Opzione 2: Analisi Personalizzate (Avanzato)
1. Apri `turni_dettagliati.csv` con Excel o Python
2. Crea le tue formule e calcoli
3. Esporta in altri formati se necessario

---

## 🔄 Aggiornare i Dati

Se aggiungi nuovi PDF o modifichi quelli esistenti:

```bash
cd "/Users/radice/Downloads/ROTA Chicca"
./ESEGUI_TUTTO.sh
```

Il sistema rielaborerà tutto automaticamente!

---

## ❓ Problemi Comuni

### "Permission denied"
```bash
chmod +x ESEGUI_TUTTO.sh
```

### "Comando non trovato"
Assicurati di essere nella cartella giusta:
```bash
cd "/Users/radice/Downloads/ROTA Chicca"
```

### "Modulo non trovato"
Ricrea l'ambiente virtuale:
```bash
python3 -m venv venv
source venv/bin/activate
pip install PyPDF2 pandas openpyxl
```

---

## 📞 Bisogno di Aiuto?

Leggi il file **README.md** per dettagli completi su:
- Analisi disponibili
- Personalizzazione degli script
- Struttura dei dati
- Suggerimenti avanzati

---

## 🎉 Fatto!

Ora hai tutti i tuoi turni del 2025 organizzati e analizzati!

**Apri `REPORT_FINALE_COMPLETO.xlsx` e inizia a esplorare i dati!** 📊

