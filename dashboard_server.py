#!/usr/bin/env python3
"""
Dashboard HR Server - Flask Web Application
Tutti i calcoli in Python puro (matematica deterministica)
"""

from flask import Flask, render_template_string, jsonify, request, send_file
import pandas as pd
import numpy as np
from pathlib import Path
import json

app = Flask(__name__)

# Carica dati globali
BASE_PATH = Path('/Users/radice/Downloads/ROTA Chicca')
DATA = None

def load_data_global():
    """Carica dati all'avvio"""
    global DATA
    
    # Prova file Excel utente
    excel_file = BASE_PATH / 'Tutti Turni Anno-completi.xlsx'
    csv_file = BASE_PATH / 'turni_completi_52_settimane.csv'
    
    if excel_file.exists():
        print(f"✅ Caricato: {excel_file}")
        DATA = pd.read_excel(excel_file)
    elif csv_file.exists():
        print(f"✅ Caricato: {csv_file}")
        DATA = pd.read_csv(csv_file)
    else:
        print("❌ Nessun file dati trovato")
        DATA = None
    
    if DATA is not None:
        if 'settimana' in DATA.columns:
            DATA['settimana'] = pd.to_numeric(DATA['settimana'], errors='coerce')
        print(f"📊 Dati caricati: {len(DATA)} turni, {DATA['staff'].nunique()} staff")

# Funzioni calcolo (PYTHON PURO - MATEMATICA)
def calc_metriche_staff(staff_name, df=None):
    """Calcola metriche per uno staff - PYTHON pandas (non AI)"""
    if df is None:
        df = DATA
    
    df_staff = df[df['staff'] == staff_name]
    
    # Conta turni per tipo (Python len())
    turni_normali = len(df_staff[df_staff['tipo_turno'] == 'NORMALE'])
    riposi = len(df_staff[df_staff['tipo_turno'].isin(['RIPO', 'RDOM'])])
    ferie = len(df_staff[df_staff['tipo_turno'] == 'FERIOR'])
    off = len(df_staff[df_staff['tipo_turno'].isin(['OFF', 'CHIUSO'])])
    
    # Somma ore (pandas.sum() - matematica)
    ore_totali = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum()
    ore_media = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].mean()
    
    return {
        'staff': staff_name,
        'turni_totali': int(len(df_staff)),
        'turni_normali': int(turni_normali),
        'riposi': int(riposi),
        'ferie': int(ferie),
        'off': int(off),
        'ore_totali': round(float(ore_totali), 1),
        'ore_media': round(float(ore_media), 2) if pd.notna(ore_media) else 0
    }

def calc_cv(values):
    """Calcola CV - numpy (matematica IEEE)"""
    if len(values) == 0 or np.mean(values) == 0:
        return 0
    return float((np.std(values) / np.mean(values)) * 100)

@app.route('/')
def index():
    """Pagina principale"""
    if DATA is None:
        return "<h1>❌ Errore: Nessun file dati trovato</h1><p>Assicurati che turni_completi_52_settimane.csv sia presente.</p>"
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/overview')
def api_overview():
    """API: Dati overview"""
    if DATA is None:
        return jsonify({'error': 'No data'}), 404
    
    # Calcoli Python puri
    staff_list = sorted(DATA['staff'].unique())
    metriche_all = [calc_metriche_staff(staff) for staff in staff_list]
    
    return jsonify({
        'total_turni': int(len(DATA)),
        'total_ore': round(float(DATA['ore_lavoro'].sum()), 1),
        'settimane': int(DATA['settimana'].nunique()),
        'staff_count': len(staff_list),
        'staff_list': staff_list,
        'metriche_staff': metriche_all
    })

@app.route('/api/compare/<staff1>/<staff2>')
def api_compare(staff1, staff2):
    """API: Confronto tra due staff"""
    m1 = calc_metriche_staff(staff1)
    m2 = calc_metriche_staff(staff2)
    
    return jsonify({
        'staff1': staff1,
        'staff2': staff2,
        'metriche1': m1,
        'metriche2': m2
    })

@app.route('/api/cv')
def api_cv():
    """API: Calcola CV per tutte le metriche"""
    staff_list = sorted(DATA['staff'].unique())
    
    cv_results = {}
    for metrica in ['ore_totali', 'turni_totali', 'riposi', 'ferie']:
        values = []
        for staff in staff_list:
            m = calc_metriche_staff(staff)
            values.append(m[metrica])
        
        cv = calc_cv(values)
        mean_val = np.mean(values)
        std_val = np.std(values)
        
        cv_results[metrica] = {
            'cv': round(cv, 2),
            'mean': round(float(mean_val), 2),
            'std': round(float(std_val), 2),
            'status': 'OTTIMO' if cv < 10 else ('ACCETTABILE' if cv < 20 else 'SQUILIBRATO')
        }
    
    return jsonify(cv_results)

@app.route('/api/data')
def api_data():
    """API: Tutti i dati (limitato a 1000 righe per performance)"""
    df_json = DATA.head(1000).to_dict('records')
    return jsonify(df_json)

# Template HTML minimo
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard HR</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #1f77b4; }
        .alert { padding: 15px; border-radius: 5px; margin: 15px 0; background: #d4edda; color: #155724; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard HR - Analisi Turni 2025</h1>
        <div class="alert">
            🔒 <strong>Calcoli Python Puri</strong> - Accedi all'API per dati JSON<br>
            📊 API Disponibili:
            <ul>
                <li><a href="/api/overview">/api/overview</a> - Dati generali</li>
                <li><a href="/api/compare/VISSANI/PAGANO">/api/compare/STAFF1/STAFF2</a> - Confronti</li>
                <li><a href="/api/cv">/api/cv</a> - Indici di equità</li>
                <li><a href="/api/data">/api/data</a> - Tutti i dati</li>
            </ul>
        </div>
        <p>✅ Server Flask attivo - Usa l'API per integrazioni o apri <a href="dashboard_hr.html">dashboard_hr.html</a> per interfaccia visiva</p>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    load_data_global()
    
    if DATA is not None:
        print("\n" + "="*70)
        print("🚀 AVVIO DASHBOARD HR")
        print("="*70)
        print(f"\n✅ Dati caricati: {len(DATA)} turni")
        print(f"\n🌐 Apri il browser all'indirizzo:")
        print(f"   http://localhost:5000")
        print(f"\n📊 API REST disponibili per integrazioni")
        print(f"\n⏹️  Premi CTRL+C per fermare il server")
        print("="*70 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Impossibile avviare: nessun file dati trovato")

