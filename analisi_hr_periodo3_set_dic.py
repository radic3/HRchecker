#!/usr/bin/env python3
"""
Analisi HR Periodo 3: SETTEMBRE-DICEMBRE 2025 (Settimane 36-52)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Festività SETTEMBRE-DICEMBRE 2025
FESTIVITA_PERIODO3 = {
    '2025-11-01': 'Ognissanti',
    '2025-12-08': 'Immacolata Concezione',
    '2025-12-25': 'Natale',
    '2025-12-26': 'Santo Stefano'
}

def load_data_periodo3():
    """Carica dati per settimane 36-52"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    df = pd.read_csv(base_path / 'turni_completi_52_settimane.csv')
    
    # Filtra settimane 36-52
    df = df[(df['settimana'] >= 36) & (df['settimana'] <= 52)]
    
    print(f"✅ Dati Periodo 3 caricati: {len(df)} turni")
    print(f"   Settimane: {sorted(df['settimana'].unique())}")
    
    return df

def analisi_statistiche_periodo3(df):
    """Statistiche per il periodo settembre-dicembre"""
    print("\n" + "="*70)
    print("📊 STATISTICHE PERIODO 3 (SETTEMBRE-DICEMBRE)")
    print("="*70)
    
    metriche = {}
    
    for staff in sorted(df['staff'].unique()):
        df_staff = df[df['staff'] == staff]
        
        # Conta turni per tipo
        turni_normali = len(df_staff[df_staff['tipo_turno'] == 'NORMALE'])
        turni_riposo = len(df_staff[df_staff['tipo_turno'].isin(['RIPO', 'RDOM'])])
        turni_ferie = len(df_staff[df_staff['tipo_turno'] == 'FERIOR'])
        turni_off = len(df_staff[df_staff['tipo_turno'].isin(['OFF', 'CHIUSO'])])
        
        # Ore
        ore_totali = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum()
        ore_medie = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].mean()
        
        metriche[staff] = {
            'Turni Totali': len(df_staff),
            'Turni Normali': turni_normali,
            'Riposi': turni_riposo,
            'Ferie': turni_ferie,
            'OFF/Chiuso': turni_off,
            'Ore Totali': round(ore_totali, 1),
            'Media Ore/Turno': round(ore_medie, 2)
        }
    
    df_stats = pd.DataFrame(metriche).T
    
    print("\n📋 STATISTICHE PER STAFF (Settimane 36-52):")
    print(df_stats.to_string())
    
    # Calcola CV per equità
    print("\n⚖️  INDICI DI EQUITÀ:")
    for col in ['Turni Normali', 'Riposi', 'Ore Totali']:
        if df_stats[col].std() > 0 and df_stats[col].mean() > 0:
            cv = (df_stats[col].std() / df_stats[col].mean()) * 100
            status = "✅" if cv < 10 else ("⚠️" if cv < 20 else "❌")
            print(f"   {col:20}: CV = {cv:6.2f}% {status}")
    
    return df_stats

def confronti_periodo3(df_stats):
    """Confronti diretti per periodo 3"""
    print("\n" + "="*70)
    print("🔍 CONFRONTI DIRETTI - PERIODO 3")
    print("="*70)
    
    confronti = [
        ('VISSANI', 'PAGANO'),
        ('PAGANO', 'PACINI'),
        ('TAMBERI', 'MORALE'),
        ('CIRCELLI', 'VISSANI')
    ]
    
    for staff1, staff2 in confronti:
        if staff1 in df_stats.index and staff2 in df_stats.index:
            print(f"\n📊 {staff1} vs {staff2}:")
            
            for metrica in ['Ore Totali', 'Turni Normali', 'Riposi']:
                val1 = df_stats.loc[staff1, metrica]
                val2 = df_stats.loc[staff2, metrica]
                diff = val1 - val2
                
                if val2 != 0:
                    perc = (diff / val2) * 100
                    simbolo = ">" if diff > 0 else ("<" if diff < 0 else "=")
                    alert = " ❌" if abs(perc) > 20 else (" ⚠️" if abs(perc) > 10 else " ✅")
                    
                    print(f"   {metrica:15}: {val1:6.1f} {simbolo} {val2:6.1f} ({perc:+6.1f}%){alert}")

def genera_report_periodo3(df, df_stats):
    """Genera report Excel per periodo 3"""
    print("\n" + "="*70)
    print("📄 GENERAZIONE REPORT PERIODO 3")
    print("="*70)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output_file = base_path / 'REPORT_HR_PERIODO3_SET_DIC.xlsx'
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Foglio 1: Summary
            summary = pd.DataFrame({
                'Metrica': ['Periodo', 'Settimane', 'Turni', 'Staff'],
                'Valore': ['Settembre-Dicembre 2025', '36-52', len(df), df['staff'].nunique()]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Foglio 2: Tutti turni periodo
            df.to_excel(writer, sheet_name='Turni Periodo 3', index=False)
            
            # Foglio 3: Statistiche
            df_stats.to_excel(writer, sheet_name='Statistiche Staff')
            
            # Foglio 4: Pivot settimana-staff (ore)
            pivot_ore = df[df['ore_lavoro'].notna()].pivot_table(
                values='ore_lavoro',
                index='staff',
                columns='settimana',
                aggfunc='sum',
                fill_value=0
            ).round(1)
            pivot_ore.to_excel(writer, sheet_name='Ore per Settimana')
        
        print(f"✅ Report salvato: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Errore: {e}")
        return None

def main():
    print("="*70)
    print("📊 ANALISI HR - PERIODO 3: SETTEMBRE-DICEMBRE 2025")
    print("   Settimane 36-52 (4 mesi)")
    print("="*70)
    
    # Carica dati
    df = load_data_periodo3()
    
    # Analisi
    df_stats = analisi_statistiche_periodo3(df)
    confronti_periodo3(df_stats)
    
    # Report
    report_file = genera_report_periodo3(df, df_stats)
    
    print("\n" + "="*70)
    print("✅ ANALISI PERIODO 3 COMPLETATA!")
    print("="*70)
    
    if report_file:
        print(f"\n📄 Report: {report_file.name}")

if __name__ == '__main__':
    main()

