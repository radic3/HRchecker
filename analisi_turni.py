#!/usr/bin/env python3
"""
Script per analizzare i turni estratti dai PDF ROTA
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import re

def load_data():
    """Carica i dati dal CSV"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    csv_file = base_path / 'turni_estratti.csv'
    
    if not csv_file.exists():
        print("Errore: Prima esegui extract_turni.py per estrarre i dati!")
        return None
    
    df = pd.read_csv(csv_file)
    return df

def analisi_base(df):
    """Statistiche base"""
    print("\n" + "="*60)
    print("ANALISI BASE")
    print("="*60)
    
    print(f"\nTotale settimane: {df['settimana'].nunique()}")
    print(f"Totale turni registrati: {len(df)}")
    print(f"\nSettimane con modifiche: {df[df['modifiche'] != '']['settimana'].nunique()}")
    
    print("\nDistribuzione turni per giorno della settimana:")
    if 'giorno' in df.columns:
        print(df['giorno'].value_counts())

def analisi_orari(df):
    """Analizza gli orari di lavoro"""
    print("\n" + "="*60)
    print("ANALISI ORARI")
    print("="*60)
    
    # Estrae pattern orari dal testo
    orari_pattern = r'(\d{1,2})[:\.](\d{2})\s*-\s*(\d{1,2})[:\.](\d{2})'
    
    turni_orari = []
    for idx, row in df.iterrows():
        if pd.notna(row.get('testo_turno', '')):
            matches = re.findall(orari_pattern, str(row['testo_turno']))
            for match in matches:
                ora_inizio = f"{match[0].zfill(2)}:{match[1]}"
                ora_fine = f"{match[2].zfill(2)}:{match[3]}"
                
                # Calcola durata
                try:
                    h_inizio = int(match[0])
                    m_inizio = int(match[1])
                    h_fine = int(match[2])
                    m_fine = int(match[3])
                    
                    minuti_inizio = h_inizio * 60 + m_inizio
                    minuti_fine = h_fine * 60 + m_fine
                    
                    if minuti_fine < minuti_inizio:
                        minuti_fine += 24 * 60
                    
                    durata_ore = (minuti_fine - minuti_inizio) / 60
                    
                    turni_orari.append({
                        'settimana': row['settimana'],
                        'giorno': row.get('giorno', ''),
                        'ora_inizio': ora_inizio,
                        'ora_fine': ora_fine,
                        'durata_ore': durata_ore
                    })
                except:
                    pass
    
    if turni_orari:
        df_orari = pd.DataFrame(turni_orari)
        print(f"\nTurni con orari identificati: {len(df_orari)}")
        print(f"\nDurata media turno: {df_orari['durata_ore'].mean():.2f} ore")
        print(f"Durata minima turno: {df_orari['durata_ore'].min():.2f} ore")
        print(f"Durata massima turno: {df_orari['durata_ore'].max():.2f} ore")
        
        print("\nOrari di inizio più comuni:")
        print(df_orari['ora_inizio'].value_counts().head(5))
        
        print("\nOrari di fine più comuni:")
        print(df_orari['ora_fine'].value_counts().head(5))
        
        return df_orari
    else:
        print("\nNessun orario strutturato trovato nei dati")
        return None

def analisi_modifiche(df):
    """Analizza le modifiche ai turni"""
    print("\n" + "="*60)
    print("ANALISI MODIFICHE")
    print("="*60)
    
    df_mod = df[df['modifiche'] != ''].copy()
    
    if len(df_mod) > 0:
        print(f"\nSettimane con modifiche: {df_mod['settimana'].nunique()}")
        print(f"Totale turni modificati: {len(df_mod)}")
        
        print("\nTipologia modifiche:")
        print(df_mod['modifiche'].value_counts())
    else:
        print("\nNessuna modifica trovata")

def analisi_temporale(df):
    """Analisi temporale dei turni"""
    print("\n" + "="*60)
    print("ANALISI TEMPORALE")
    print("="*60)
    
    # Converti settimana in numero
    df['settimana_num'] = pd.to_numeric(df['settimana'], errors='coerce')
    
    # Turni per settimana
    turni_per_settimana = df.groupby('settimana_num').size()
    
    print(f"\nMedia turni per settimana: {turni_per_settimana.mean():.2f}")
    print(f"\nSettimana con più turni: {turni_per_settimana.idxmax()} ({turni_per_settimana.max()} turni)")
    print(f"Settimana con meno turni: {turni_per_settimana.idxmin()} ({turni_per_settimana.min()} turni)")

def genera_report_excel(df, df_orari=None):
    """Genera un report Excel completo"""
    print("\n" + "="*60)
    print("GENERAZIONE REPORT EXCEL")
    print("="*60)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output_file = base_path / 'report_analisi_turni.xlsx'
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Foglio 1: Tutti i dati
            df.to_excel(writer, sheet_name='Dati Completi', index=False)
            
            # Foglio 2: Riepilogo per settimana
            df['settimana_num'] = pd.to_numeric(df['settimana'], errors='coerce')
            summary = df.groupby('settimana_num').agg({
                'file': 'first',
                'giorno': 'count',
                'modifiche': lambda x: (x != '').sum()
            }).rename(columns={'giorno': 'n_turni', 'modifiche': 'n_modifiche'})
            summary.to_excel(writer, sheet_name='Riepilogo Settimane')
            
            # Foglio 3: Distribuzione giorni
            if 'giorno' in df.columns:
                giorni_dist = df['giorno'].value_counts().to_frame('conteggio')
                giorni_dist.to_excel(writer, sheet_name='Distribuzione Giorni')
            
            # Foglio 4: Analisi orari
            if df_orari is not None and not df_orari.empty:
                df_orari.to_excel(writer, sheet_name='Analisi Orari', index=False)
                
                # Statistiche orari
                stats_orari = pd.DataFrame({
                    'Metrica': ['Media ore/turno', 'Min ore/turno', 'Max ore/turno', 
                                'Totale turni analizzati'],
                    'Valore': [
                        df_orari['durata_ore'].mean(),
                        df_orari['durata_ore'].min(),
                        df_orari['durata_ore'].max(),
                        len(df_orari)
                    ]
                })
                stats_orari.to_excel(writer, sheet_name='Statistiche Orari', index=False)
            
            # Foglio 5: Modifiche
            df_mod = df[df['modifiche'] != '']
            if len(df_mod) > 0:
                df_mod.to_excel(writer, sheet_name='Settimane Modificate', index=False)
        
        print(f"✓ Report salvato in: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Errore nella generazione del report: {e}")
        return None

def main():
    print("="*60)
    print("ANALISI TURNI DI LAVORO")
    print("="*60)
    
    # Carica dati
    df = load_data()
    if df is None:
        return
    
    print(f"\nDati caricati: {len(df)} righe, {len(df.columns)} colonne")
    
    # Esegui analisi
    analisi_base(df)
    df_orari = analisi_orari(df)
    analisi_modifiche(df)
    analisi_temporale(df)
    
    # Genera report Excel
    report_file = genera_report_excel(df, df_orari)
    
    print("\n" + "="*60)
    print("ANALISI COMPLETATA!")
    print("="*60)
    if report_file:
        print(f"\nPuoi trovare il report dettagliato in: {report_file}")

if __name__ == '__main__':
    main()

