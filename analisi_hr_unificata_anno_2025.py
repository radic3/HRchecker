#!/usr/bin/env python3
"""
Analisi HR Unificata - ANNO COMPLETO 2025
Unisce i 3 periodi e genera report finale integrato
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_all_data():
    """Carica tutti i dati dell'anno"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    df = pd.read_csv(base_path / 'turni_completi_52_settimane.csv')
    
    # Classifica per periodo
    df['periodo'] = df['settimana'].apply(lambda x: 
        'Periodo 1 (Gen-Apr)' if x <= 17 else
        'Periodo 2 (Mag-Ago)' if x <= 35 else
        'Periodo 3 (Set-Dic)'
    )
    
    return df

def analisi_per_periodo(df):
    """Analisi separata per ogni periodo"""
    print("\n" + "="*70)
    print("📊 ANALISI PER PERIODO - CONFRONTO 3 QUADRIMESTRI")
    print("="*70)
    
    risultati = {}
    
    for periodo in ['Periodo 1 (Gen-Apr)', 'Periodo 2 (Mag-Ago)', 'Periodo 3 (Set-Dic)']:
        df_periodo = df[df['periodo'] == periodo]
        
        print(f"\n{'='*70}")
        print(f"📅 {periodo}")
        print('='*70)
        
        stats_periodo = {}
        for staff in sorted(df['staff'].unique()):
            df_staff = df_periodo[df_periodo['staff'] == staff]
            
            ore = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum()
            turni_norm = len(df_staff[df_staff['tipo_turno'] == 'NORMALE'])
            riposi = len(df_staff[df_staff['tipo_turno'].isin(['RIPO', 'RDOM'])])
            
            stats_periodo[staff] = {
                'Turni': len(df_staff),
                'Ore': round(ore, 1),
                'Turni Normali': turni_norm,
                'Riposi': riposi
            }
        
        df_stats = pd.DataFrame(stats_periodo).T
        print(df_stats.to_string())
        
        # Calcola CV
        if len(df_stats) > 0 and df_stats['Ore'].mean() > 0:
            cv_ore = (df_stats['Ore'].std() / df_stats['Ore'].mean()) * 100
            cv_riposi = (df_stats['Riposi'].std() / df_stats['Riposi'].mean()) * 100 if df_stats['Riposi'].mean() > 0 else 0
            
            print(f"\n   CV Ore: {cv_ore:.2f}% | CV Riposi: {cv_riposi:.2f}%")
            
            risultati[periodo] = {
                'stats': df_stats,
                'cv_ore': cv_ore,
                'cv_riposi': cv_riposi
            }
    
    return risultati

def analisi_anno_totale(df):
    """Analisi sull'anno completo"""
    print("\n" + "="*70)
    print("📊 ANALISI ANNO TOTALE 2025 (TUTTE LE 52 SETTIMANE)")
    print("="*70)
    
    metriche_totali = {}
    
    for staff in sorted(df['staff'].unique()):
        df_staff = df[df['staff'] == staff]
        
        # Conta tutto
        turni_norm = len(df_staff[df_staff['tipo_turno'] == 'NORMALE'])
        riposi = len(df_staff[df_staff['tipo_turno'].isin(['RIPO', 'RDOM'])])
        ferie = len(df_staff[df_staff['tipo_turno'] == 'FERIOR'])
        off = len(df_staff[df_staff['tipo_turno'].isin(['OFF', 'CHIUSO'])])
        
        ore_totali = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum()
        
        metriche_totali[staff] = {
            'Turni Totali': len(df_staff),
            'Turni Normali': turni_norm,
            'Riposi': riposi,
            'Ferie': ferie,
            'OFF': off,
            'Ore Totali': round(ore_totali, 1),
            'Media Ore/Turno': round(ore_totali / turni_norm, 2) if turni_norm > 0 else 0
        }
    
    df_totale = pd.DataFrame(metriche_totali).T
    
    print("\n📋 METRICHE TOTALI ANNO 2025:")
    print(df_totale.to_string())
    
    # CV per ogni metrica
    print("\n⚖️  INDICI DI EQUITÀ ANNO:")
    cv_results = {}
    for col in ['Turni Normali', 'Riposi', 'Ferie', 'Ore Totali']:
        if df_totale[col].std() > 0 and df_totale[col].mean() > 0:
            cv = (df_totale[col].std() / df_totale[col].mean()) * 100
            status = "✅ OTTIMO" if cv < 10 else ("⚠️  ACCETTABILE" if cv < 20 else "❌ SQUILIBRATO")
            cv_results[col] = cv
            print(f"   {col:20}: CV = {cv:6.2f}% {status}")
    
    return df_totale, cv_results

def confronti_anno_completo(df_totale):
    """Confronti finali sull'anno completo"""
    print("\n" + "="*70)
    print("🔍 CONFRONTI FINALI - ANNO COMPLETO 2025")
    print("="*70)
    
    confronti = [
        ('VISSANI', 'PAGANO'),
        ('PAGANO', 'PACINI'),
        ('TAMBERI', 'MORALE'),
        ('CIRCELLI', 'VISSANI')
    ]
    
    risultati = []
    
    for staff1, staff2 in confronti:
        if staff1 in df_totale.index and staff2 in df_totale.index:
            print(f"\n{'='*70}")
            print(f"📊 {staff1} vs {staff2} - ANNO COMPLETO")
            print('='*70)
            
            disparita = 0
            
            for metrica in ['Ore Totali', 'Turni Normali', 'Riposi', 'Ferie']:
                val1 = df_totale.loc[staff1, metrica]
                val2 = df_totale.loc[staff2, metrica]
                diff = val1 - val2
                
                if val2 != 0:
                    perc = (diff / val2) * 100
                    simbolo = ">" if diff > 0 else ("<" if diff < 0 else "=")
                    
                    if abs(perc) > 25:
                        alert = " 🚨 DISPARITÀ GRAVE!"
                        disparita += 2
                    elif abs(perc) > 15:
                        alert = " ❌ DISPARITÀ"
                        disparita += 1
                    elif abs(perc) > 10:
                        alert = " ⚠️  Attenzione"
                    else:
                        alert = " ✅"
                    
                    print(f"   {metrica:15}: {staff1}={val1:7.1f} {simbolo} {staff2}={val2:7.1f} " +
                          f"(diff: {diff:+7.1f}, {perc:+6.1f}%){alert}")
            
            # Conclusione
            print(f"\n   📊 GIUDIZIO: ", end="")
            if disparita == 0:
                print("✅ DISTRIBUZIONE EQUA")
                status = "EQUO"
            elif disparita <= 2:
                print(f"⚠️  LEGGERO SQUILIBRIO ({disparita} alert)")
                status = "ATTENZIONE"
            else:
                print(f"❌ SQUILIBRIO SIGNIFICATIVO ({disparita} alert)")
                status = "SQUILIBRATO"
            
            risultati.append({
                'Confronto': f'{staff1} vs {staff2}',
                'Alert': disparita,
                'Status': status
            })
    
    return pd.DataFrame(risultati)

def genera_report_unificato(df, df_totale, cv_results, confronti):
    """Genera report Excel unificato finale"""
    print("\n" + "="*70)
    print("📄 GENERAZIONE REPORT UNIFICATO FINALE")
    print("="*70)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output_file = base_path / 'REPORT_HR_UNIFICATO_2025_COMPLETO.xlsx'
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Foglio 1: Executive Summary
            summary = pd.DataFrame({
                'Metrica': [
                    'Anno', 'Settimane Totali', 'Turni Totali', 'Staff', 
                    'Periodo Analizzato', 'Anomalie Critiche'
                ],
                'Valore': [
                    2025,
                    df['settimana'].nunique(),
                    len(df),
                    df['staff'].nunique(),
                    'Gen-Dic 2025 (52 settimane)',
                    'Vedere fogli dettaglio'
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Foglio 2: Metriche Totali Anno
            df_totale.to_excel(writer, sheet_name='Metriche Anno Totale')
            
            # Foglio 3: Indici CV
            df_cv = pd.DataFrame(list(cv_results.items()), columns=['Metrica', 'CV%'])
            df_cv['Status'] = df_cv['CV%'].apply(
                lambda x: 'OTTIMO' if x < 10 else ('ACCETTABILE' if x < 20 else 'SQUILIBRATO')
            )
            df_cv = df_cv.sort_values('CV%', ascending=False)
            df_cv.to_excel(writer, sheet_name='Indici Equità', index=False)
            
            # Foglio 4: Confronti Anno
            confronti.to_excel(writer, sheet_name='Confronti Diretti', index=False)
            
            # Foglio 5: Tutti i turni
            df.to_excel(writer, sheet_name='Tutti Turni Anno', index=False)
            
            # Foglio 6: Statistiche per Periodo
            stats_per_periodo = df.groupby(['periodo', 'staff']).agg({
                'linea_completa': 'count',
                'ore_lavoro': 'sum'
            }).round(1)
            stats_per_periodo.columns = ['N_Turni', 'Ore']
            stats_per_periodo.to_excel(writer, sheet_name='Stats per Periodo')
            
            # Foglio 7: Pivot Settimana-Staff (Ore)
            pivot_ore = df[df['ore_lavoro'].notna()].pivot_table(
                values='ore_lavoro',
                index='staff',
                columns='settimana',
                aggfunc='sum',
                fill_value=0
            ).round(1)
            pivot_ore.to_excel(writer, sheet_name='Ore per Settimana')
            
            # Foglio 8: Pivot Settimana-Staff (Turni)
            pivot_turni = df.pivot_table(
                values='linea_completa',
                index='staff',
                columns='settimana',
                aggfunc='count',
                fill_value=0
            )
            pivot_turni.to_excel(writer, sheet_name='Turni per Settimana')
        
        print(f"✅ Report unificato salvato: {output_file}")
        print(f"\n📊 Contiene 8 fogli con analisi anno completo!")
        return output_file
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("="*70)
    print("⚖️  ANALISI HR UNIFICATA - ANNO COMPLETO 2025")
    print("   Tutte le 52 settimane + Confronto 3 Periodi")
    print("="*70)
    
    # Carica tutti i dati
    df = load_all_data()
    print(f"\n✅ Dati caricati: {len(df)} turni, {df['settimana'].nunique()} settimane")
    
    # Analisi per periodo
    risultati_periodi = analisi_per_periodo(df)
    
    # Analisi anno totale
    df_totale, cv_results = analisi_anno_totale(df)
    
    # Confronti finali
    confronti = confronti_anno_completo(df_totale)
    
    # Report unificato
    report_file = genera_report_unificato(df, df_totale, cv_results, confronti)
    
    print("\n" + "="*70)
    print("✅ ANALISI UNIFICATA COMPLETATA!")
    print("="*70)
    
    print(f"\n📊 RIEPILOGO:")
    print(f"   Periodo 1 (Gen-Apr): Settimane 1-17")
    print(f"   Periodo 2 (Mag-Ago): Settimane 18-35")
    print(f"   Periodo 3 (Set-Dic): Settimane 36-52")
    print(f"   TOTALE: 52 settimane, {len(df)} turni")
    
    if report_file:
        print(f"\n📄 Report finale: {report_file.name}")

if __name__ == '__main__':
    main()

