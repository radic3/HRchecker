#!/usr/bin/env python3
"""
Analisi avanzata dei turni estratti
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Carica i dati dettagliati"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    csv_file = base_path / 'turni_dettagliati.csv'
    
    if not csv_file.exists():
        print("❌ Errore: Esegui prima extract_turni_avanzato.py!")
        return None
    
    df = pd.read_csv(csv_file)
    return df

def analisi_ore_lavoro(df):
    """Analisi dettagliata delle ore lavorate"""
    print("\n" + "="*70)
    print("📊 ANALISI ORE LAVORO")
    print("="*70)
    
    # Filtra solo turni con ore valide
    df_ore = df[df['ore_lavoro'].notna()].copy()
    
    # Statistiche generali
    print(f"\n🔢 STATISTICHE GENERALI:")
    print(f"   Totale ore lavorate: {df_ore['ore_lavoro'].sum():.1f} ore")
    print(f"   Media ore per turno: {df_ore['ore_lavoro'].mean():.2f} ore")
    print(f"   Mediana ore per turno: {df_ore['ore_lavoro'].median():.2f} ore")
    print(f"   Turno più corto: {df_ore['ore_lavoro'].min():.1f} ore")
    print(f"   Turno più lungo: {df_ore['ore_lavoro'].max():.1f} ore")
    
    # Ore per staff
    print(f"\n👥 ORE PER STAFF:")
    ore_staff = df_ore.groupby('staff').agg({
        'ore_lavoro': ['sum', 'mean', 'count']
    }).round(2)
    ore_staff.columns = ['Totale Ore', 'Media Ore/Turno', 'N. Turni']
    ore_staff = ore_staff.sort_values('Totale Ore', ascending=False)
    print(ore_staff)
    
    # Distribuzione ore per fascia
    print(f"\n📈 DISTRIBUZIONE TURNI PER FASCIA ORARIA:")
    fasce = {
        '1-4 ore': (0, 4),
        '5-6 ore': (5, 6),
        '7-8 ore': (7, 8),
        '9+ ore': (9, 100)
    }
    
    for fascia, (min_h, max_h) in fasce.items():
        count = len(df_ore[(df_ore['ore_lavoro'] > min_h) & (df_ore['ore_lavoro'] <= max_h)])
        perc = (count / len(df_ore) * 100)
        print(f"   {fascia}: {count} turni ({perc:.1f}%)")
    
    return ore_staff

def analisi_tipologie_turno(df):
    """Analisi delle tipologie di turno"""
    print("\n" + "="*70)
    print("📋 ANALISI TIPOLOGIE TURNO")
    print("="*70)
    
    # Conteggio per tipo
    tipi = df['tipo_turno'].value_counts()
    print(f"\n🏷️  DISTRIBUZIONE TIPI:")
    for tipo, count in tipi.items():
        perc = (count / len(df) * 100)
        print(f"   {tipo:12} : {count:4} turni ({perc:5.1f}%)")
    
    # Turni per staff e tipo
    print(f"\n👤 TIPI DI TURNO PER STAFF:")
    pivot = pd.crosstab(df['staff'], df['tipo_turno'])
    print(pivot)
    
    return tipi

def analisi_orari(df):
    """Analisi degli orari di lavoro"""
    print("\n" + "="*70)
    print("⏰ ANALISI ORARI")
    print("="*70)
    
    df_orari = df[df['ora_entrata'].notna()].copy()
    
    # Orari di entrata più comuni
    print(f"\n🌅 ORARI DI ENTRATA PIÙ COMUNI:")
    entrate = df_orari['ora_entrata'].value_counts().head(10)
    for orario, count in entrate.items():
        print(f"   {orario}: {count} volte")
    
    # Orari di uscita più comuni
    if 'ora_uscita' in df_orari.columns:
        print(f"\n🌆 ORARI DI USCITA PIÙ COMUNI:")
        uscite = df_orari['ora_uscita'].value_counts().head(10)
        for orario, count in uscite.items():
            print(f"   {orario}: {count} volte")
    
    # Analisi fasce orarie
    print(f"\n📊 ANALISI FASCE ORARIE ENTRATA:")
    df_orari['ora_entrata_int'] = df_orari['ora_entrata'].apply(
        lambda x: int(x.split(':')[0]) if pd.notna(x) and ':' in str(x) else None
    )
    
    fasce_orarie = {
        'Notte (00:00-05:59)': (0, 6),
        'Mattina presto (06:00-08:59)': (6, 9),
        'Mattina (09:00-11:59)': (9, 12),
        'Pomeriggio (12:00-17:59)': (12, 18),
        'Sera (18:00-23:59)': (18, 24)
    }
    
    for fascia, (start, end) in fasce_orarie.items():
        count = len(df_orari[
            (df_orari['ora_entrata_int'] >= start) & 
            (df_orari['ora_entrata_int'] < end)
        ])
        print(f"   {fascia}: {count} turni")

def analisi_temporale(df):
    """Analisi temporale dei turni"""
    print("\n" + "="*70)
    print("📅 ANALISI TEMPORALE")
    print("="*70)
    
    # Converti settimana in numero
    df['settimana_num'] = pd.to_numeric(df['settimana'], errors='coerce')
    
    # Turni per settimana
    turni_sett = df.groupby('settimana_num').size()
    
    print(f"\n📈 STATISTICHE PER SETTIMANA:")
    print(f"   Numero settimane coperte: {df['settimana_num'].nunique()}")
    print(f"   Media turni per settimana: {turni_sett.mean():.1f}")
    print(f"   Settimana con più turni: Settimana {turni_sett.idxmax()} ({turni_sett.max()} turni)")
    print(f"   Settimana con meno turni: Settimana {turni_sett.idxmin()} ({turni_sett.min()} turni)")
    
    # Ore per settimana
    if 'ore_lavoro' in df.columns:
        df_ore = df[df['ore_lavoro'].notna()]
        ore_sett = df_ore.groupby('settimana_num')['ore_lavoro'].sum()
        
        print(f"\n⏱️  ORE PER SETTIMANA:")
        print(f"   Media ore per settimana: {ore_sett.mean():.1f} ore")
        print(f"   Settimana più intensa: Settimana {ore_sett.idxmax()} ({ore_sett.max():.1f} ore)")
        print(f"   Settimana meno intensa: Settimana {ore_sett.idxmin()} ({ore_sett.min():.1f} ore)")

def analisi_settimane_modificate(df):
    """Analisi delle settimane con modifiche"""
    print("\n" + "="*70)
    print("✏️  ANALISI MODIFICHE")
    print("="*70)
    
    # Filtra settimane con modifiche
    df_mod = df[df['modifiche'].notna() & (df['modifiche'] != '')].copy()
    
    if len(df_mod) > 0:
        print(f"\n📝 STATISTICHE MODIFICHE:")
        print(f"   Settimane modificate: {df_mod['settimana'].nunique()}")
        print(f"   Turni in settimane modificate: {len(df_mod)}")
        print(f"   % turni modificati: {(len(df_mod)/len(df)*100):.1f}%")
        
        print(f"\n🔄 TIPOLOGIE DI MODIFICHE:")
        mods = df_mod['modifiche'].value_counts()
        for mod, count in mods.items():
            print(f"   {mod}: {count} settimane")
        
        # Settimane con modifiche
        sett_mod = df_mod.groupby('settimana')['modifiche'].first().sort_index()
        print(f"\n📋 ELENCO SETTIMANE MODIFICATE:")
        for sett, mod in sett_mod.items():
            print(f"   Settimana {sett}: {mod}")
    else:
        print("\n✅ Nessuna modifica trovata")

def crea_report_excel_completo(df, ore_staff):
    """Crea report Excel super dettagliato"""
    print("\n" + "="*70)
    print("📄 GENERAZIONE REPORT EXCEL COMPLETO")
    print("="*70)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output_file = base_path / 'REPORT_FINALE_COMPLETO.xlsx'
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Foglio 1: Dashboard - Riepilogo generale
            summary_data = {
                'Metrica': [
                    'Totale Turni',
                    'Totale Ore Lavorate',
                    'Media Ore/Turno',
                    'Numero Staff',
                    'Numero Settimane',
                    'Settimane con Modifiche'
                ],
                'Valore': [
                    len(df),
                    df[df['ore_lavoro'].notna()]['ore_lavoro'].sum(),
                    df[df['ore_lavoro'].notna()]['ore_lavoro'].mean(),
                    df['staff'].nunique(),
                    df['settimana'].nunique(),
                    len(df[df['modifiche'].notna() & (df['modifiche'] != '')])
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Dashboard', index=False)
            
            # Foglio 2: Tutti i turni
            df.to_excel(writer, sheet_name='Tutti i Turni', index=False)
            
            # Foglio 3: Ore per Staff
            ore_staff.to_excel(writer, sheet_name='Ore per Staff')
            
            # Foglio 4: Pivot Settimana-Staff (Ore)
            df_ore = df[df['ore_lavoro'].notna()].copy()
            df_ore['settimana_num'] = pd.to_numeric(df_ore['settimana'], errors='coerce')
            pivot_ore = df_ore.pivot_table(
                values='ore_lavoro',
                index='staff',
                columns='settimana_num',
                aggfunc='sum',
                fill_value=0
            ).round(1)
            pivot_ore.to_excel(writer, sheet_name='Ore Settimana-Staff')
            
            # Foglio 5: Pivot Settimana-Staff (N. Turni)
            pivot_turni = df.pivot_table(
                values='linea_completa',
                index='staff',
                columns='settimana_num',
                aggfunc='count',
                fill_value=0
            )
            pivot_turni.to_excel(writer, sheet_name='Turni Settimana-Staff')
            
            # Foglio 6: Tipologie Turno
            tipi_df = df['tipo_turno'].value_counts().to_frame('Conteggio')
            tipi_df['Percentuale'] = (tipi_df['Conteggio'] / len(df) * 100).round(1)
            tipi_df.to_excel(writer, sheet_name='Tipologie Turno')
            
            # Foglio 7: Orari Entrata
            df_entrata = df[df['ora_entrata'].notna()]
            if len(df_entrata) > 0:
                entrata_df = df_entrata['ora_entrata'].value_counts().to_frame('Frequenza')
                entrata_df.to_excel(writer, sheet_name='Orari Entrata')
            
            # Foglio 8: Orari Uscita
            df_uscita = df[df['ora_uscita'].notna()]
            if len(df_uscita) > 0:
                uscita_df = df_uscita['ora_uscita'].value_counts().to_frame('Frequenza')
                uscita_df.to_excel(writer, sheet_name='Orari Uscita')
            
            # Foglio 9: Settimane Modificate
            df_mod = df[df['modifiche'].notna() & (df['modifiche'] != '')]
            if len(df_mod) > 0:
                df_mod.to_excel(writer, sheet_name='Settimane Modificate', index=False)
            
            # Foglio 10: Statistiche per Staff
            stats_staff = df.groupby('staff').agg({
                'linea_completa': 'count',
                'tipo_turno': lambda x: x.value_counts().index[0] if len(x) > 0 else '',
                'ore_lavoro': ['sum', 'mean']
            }).round(2)
            stats_staff.columns = ['N. Turni', 'Tipo Più Comune', 'Totale Ore', 'Media Ore']
            stats_staff.to_excel(writer, sheet_name='Statistiche Staff')
        
        print(f"✅ Report completo salvato: {output_file}")
        print(f"\n📊 Il file contiene 10 fogli con analisi dettagliate!")
        return output_file
        
    except Exception as e:
        print(f"❌ Errore nel salvataggio: {e}")
        return None

def main():
    print("="*70)
    print("🚀 ANALISI AVANZATA TURNI DI LAVORO")
    print("="*70)
    
    # Carica dati
    df = load_data()
    if df is None:
        return
    
    print(f"\n✅ Dati caricati: {len(df)} turni, {len(df.columns)} colonne")
    print(f"📅 Periodo: da settimana {df['settimana'].min()} a settimana {df['settimana'].max()}")
    print(f"👥 Staff: {', '.join(sorted(df['staff'].unique()))}")
    
    # Esegui tutte le analisi
    ore_staff = analisi_ore_lavoro(df)
    analisi_tipologie_turno(df)
    analisi_orari(df)
    analisi_temporale(df)
    analisi_settimane_modificate(df)
    
    # Genera report finale
    report_file = crea_report_excel_completo(df, ore_staff)
    
    print("\n" + "="*70)
    print("✅ ANALISI COMPLETATA!")
    print("="*70)
    
    if report_file:
        print(f"\n📁 File generato: {report_file.name}")
        print("\n💡 Suggerimenti:")
        print("   • Apri il file Excel per esplorare tutti i dati")
        print("   • Usa i filtri per analizzare periodi specifici")
        print("   • Crea grafici dai dati pivot")
        print("   • Confronta le prestazioni tra staff")

if __name__ == '__main__':
    main()

