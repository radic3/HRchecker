#!/usr/bin/env python3
"""
Analisi di Equità e Compliance HR - Revisore Risorse Umane
Analizza distribuzione turni, festivi, riposi consecutivi e identifica anomalie
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import calendar
import warnings
warnings.filterwarnings('ignore')

# Festività italiane 2025
FESTIVITA_2025 = {
    '01/01/2025': 'Capodanno',
    '06/01/2025': 'Epifania',
    '20/04/2025': 'Pasqua',
    '21/04/2025': 'Lunedì dell\'Angelo',
    '25/04/2025': 'Festa della Liberazione',
    '01/05/2025': 'Festa del Lavoro',
    '02/06/2025': 'Festa della Repubblica',
    '15/08/2025': 'Ferragosto',
    '01/11/2025': 'Ognissanti',
    '08/12/2025': 'Immacolata Concezione',
    '25/12/2025': 'Natale',
    '26/12/2025': 'Santo Stefano'
}

def load_data():
    """Carica i dati dettagliati"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    csv_file = base_path / 'turni_dettagliati.csv'
    
    if not csv_file.exists():
        print("❌ Errore: File turni_dettagliati.csv non trovato!")
        return None
    
    df = pd.read_csv(csv_file)
    return df

def parse_date_range(row):
    """Estrae le date dal periodo della settimana"""
    try:
        data_inizio = row['data_inizio']
        data_fine = row['data_fine']
        
        # Formato: DDMMYY
        if pd.notna(data_inizio) and len(str(data_inizio)) >= 6:
            d_start = str(data_inizio).zfill(6)
            d_end = str(data_fine).zfill(6)
            
            # Parse: DDMMYY -> datetime
            day_s, month_s, year_s = d_start[:2], d_start[2:4], d_start[4:6]
            day_e, month_e, year_e = d_end[:2], d_end[2:4], d_end[4:6]
            
            start = datetime(2000 + int(year_s), int(month_s), int(day_s))
            end = datetime(2000 + int(year_e), int(month_e), int(day_e))
            
            return start, end
    except:
        pass
    
    return None, None

def genera_calendario_completo(df):
    """Genera calendario completo con tutti i giorni e turni"""
    print("\n" + "="*70)
    print("📅 GENERAZIONE CALENDARIO COMPLETO")
    print("="*70)
    
    calendario = []
    
    # Processa ogni settimana
    for settimana in sorted(df['settimana'].dropna().unique()):
        df_sett = df[df['settimana'] == settimana]
        
        # Prendi primo record per date
        row = df_sett.iloc[0]
        start, end = parse_date_range(row)
        
        if start and end:
            # Genera tutti i giorni della settimana
            current = start
            while current <= end:
                data_str = current.strftime('%d/%m/%Y')
                giorno_settimana = calendar.day_name[current.weekday()]
                is_festivo = data_str in FESTIVITA_2025
                nome_festivo = FESTIVITA_2025.get(data_str, '')
                is_weekend = current.weekday() >= 5  # Sabato=5, Domenica=6
                
                # Per ogni membro staff, identifica il turno
                for staff in df['staff'].unique():
                    df_staff_day = df_sett[df_sett['staff'] == staff]
                    
                    if len(df_staff_day) > 0:
                        # Prendi il primo turno trovato per quel giorno
                        turno_info = df_staff_day.iloc[0]
                        
                        calendario.append({
                            'data': data_str,
                            'data_dt': current,
                            'giorno_settimana': giorno_settimana,
                            'settimana': settimana,
                            'staff': staff,
                            'tipo_turno': turno_info['tipo_turno'],
                            'ore_lavoro': turno_info['ore_lavoro'],
                            'is_festivo': is_festivo,
                            'nome_festivo': nome_festivo,
                            'is_weekend': is_weekend,
                            'is_lavorato': turno_info['tipo_turno'] == 'NORMALE',
                            'is_riposo': turno_info['tipo_turno'] in ['RIPO', 'RDOM'],
                            'is_ferie': turno_info['tipo_turno'] == 'FERIOR',
                            'is_off': turno_info['tipo_turno'] in ['OFF', 'CHIUSO']
                        })
                
                current += timedelta(days=1)
    
    df_cal = pd.DataFrame(calendario)
    print(f"✅ Calendario generato: {len(df_cal)} giorni per {df_cal['staff'].nunique()} persone")
    
    return df_cal

def analisi_festivi_lavorati(df_cal):
    """Analizza chi ha lavorato i festivi"""
    print("\n" + "="*70)
    print("🎄 ANALISI FESTIVI LAVORATI")
    print("="*70)
    
    # Filtra solo festivi
    df_festivi = df_cal[df_cal['is_festivo'] == True].copy()
    
    if len(df_festivi) == 0:
        print("\n⚠️  Nessun festivo trovato nel periodo analizzato")
        return None
    
    print(f"\n📊 Festivi nel periodo: {len(FESTIVITA_2025)} giorni")
    
    # Conta festivi lavorati per staff
    festivi_lavorati = df_festivi[df_festivi['is_lavorato'] == True].groupby('staff').agg({
        'data': 'count',
        'nome_festivo': lambda x: ', '.join(sorted(set(x)))
    }).rename(columns={'data': 'N. Festivi Lavorati', 'nome_festivo': 'Quali Festivi'})
    
    festivi_lavorati = festivi_lavorati.sort_values('N. Festivi Lavorati', ascending=False)
    
    print("\n🏆 FESTIVI LAVORATI PER STAFF:")
    print(festivi_lavorati)
    
    # Analisi equità
    media = festivi_lavorati['N. Festivi Lavorati'].mean()
    std = festivi_lavorati['N. Festivi Lavorati'].std()
    
    print(f"\n📈 Statistiche:")
    print(f"   Media festivi lavorati: {media:.2f}")
    print(f"   Deviazione standard: {std:.2f}")
    print(f"   Min: {festivi_lavorati['N. Festivi Lavorati'].min()}")
    print(f"   Max: {festivi_lavorati['N. Festivi Lavorati'].max()}")
    print(f"   Differenza Max-Min: {festivi_lavorati['N. Festivi Lavorati'].max() - festivi_lavorati['N. Festivi Lavorati'].min()}")
    
    # Alert squilibri
    threshold = media * 0.3  # 30% di scostamento
    print(f"\n⚠️  ALERT SQUILIBRI (scostamento > 30% dalla media):")
    for staff, row in festivi_lavorati.iterrows():
        diff = abs(row['N. Festivi Lavorati'] - media)
        if diff > threshold:
            perc = (diff / media * 100)
            print(f"   ⚠️  {staff}: {row['N. Festivi Lavorati']} festivi (scostamento: {perc:.1f}%)")
    
    return festivi_lavorati

def analisi_riposi_consecutivi(df_cal):
    """Analizza i riposi consecutivi per ogni staff"""
    print("\n" + "="*70)
    print("😴 ANALISI RIPOSI CONSECUTIVI")
    print("="*70)
    
    risultati = {}
    
    for staff in sorted(df_cal['staff'].unique()):
        df_staff = df_cal[df_cal['staff'] == staff].sort_values('data_dt')
        
        sequenze_riposo = []
        giorni_consecutivi = 0
        
        for idx, row in df_staff.iterrows():
            if row['is_riposo'] or row['is_off'] or row['is_ferie']:
                giorni_consecutivi += 1
            else:
                if giorni_consecutivi > 0:
                    sequenze_riposo.append(giorni_consecutivi)
                giorni_consecutivi = 0
        
        # Ultima sequenza
        if giorni_consecutivi > 0:
            sequenze_riposo.append(giorni_consecutivi)
        
        # Conta sequenze per lunghezza
        riposi_2 = sum(1 for x in sequenze_riposo if x == 2)
        riposi_3 = sum(1 for x in sequenze_riposo if x == 3)
        riposi_4plus = sum(1 for x in sequenze_riposo if x >= 4)
        riposi_singoli = sum(1 for x in sequenze_riposo if x == 1)
        
        risultati[staff] = {
            'Riposi 1 giorno': riposi_singoli,
            'Riposi 2 giorni': riposi_2,
            'Riposi 3 giorni': riposi_3,
            'Riposi 4+ giorni': riposi_4plus,
            'Totale Sequenze': len(sequenze_riposo),
            'Giorni Riposo Totali': sum(sequenze_riposo),
            'Media Giorni/Sequenza': np.mean(sequenze_riposo) if sequenze_riposo else 0,
            'Max Consecutivi': max(sequenze_riposo) if sequenze_riposo else 0
        }
    
    df_riposi = pd.DataFrame(risultati).T
    df_riposi = df_riposi.sort_values('Totale Sequenze', ascending=False)
    
    print("\n📊 RIPOSI CONSECUTIVI PER STAFF:")
    print(df_riposi.to_string())
    
    # Analisi equità
    print("\n📈 ANALISI EQUITÀ RIPOSI:")
    for col in ['Riposi 2 giorni', 'Riposi 3 giorni', 'Riposi 4+ giorni']:
        media = df_riposi[col].mean()
        std = df_riposi[col].std()
        print(f"\n   {col}:")
        print(f"   Media: {media:.2f}, Std: {std:.2f}")
        
        # Identifica outliers
        for staff, val in df_riposi[col].items():
            if abs(val - media) > std * 1.5:
                print(f"   ⚠️  {staff}: {val} (scostamento significativo)")
    
    return df_riposi

def analisi_equita_generale(df_cal):
    """Analisi completa dell'equità nella distribuzione"""
    print("\n" + "="*70)
    print("⚖️  ANALISI EQUITÀ GENERALE")
    print("="*70)
    
    metriche = {}
    
    for staff in sorted(df_cal['staff'].unique()):
        df_staff = df_cal[df_cal['staff'] == staff]
        
        metriche[staff] = {
            'Giorni Totali': len(df_staff),
            'Giorni Lavorati': df_staff['is_lavorato'].sum(),
            'Giorni Riposo': df_staff['is_riposo'].sum(),
            'Giorni Ferie': df_staff['is_ferie'].sum(),
            'Giorni OFF': df_staff['is_off'].sum(),
            'Weekend Lavorati': df_staff[df_staff['is_weekend'] & df_staff['is_lavorato']].shape[0],
            'Festivi Lavorati': df_staff[df_staff['is_festivo'] & df_staff['is_lavorato']].shape[0],
            'Ore Totali': df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum(),
            'Media Ore/Giorno Lav': df_staff[df_staff['is_lavorato']]['ore_lavoro'].mean()
        }
    
    df_metriche = pd.DataFrame(metriche).T
    df_metriche = df_metriche.round(2)
    
    print("\n📊 METRICHE COMPLETE PER STAFF:")
    print(df_metriche.to_string())
    
    # Calcola indici di equità
    print("\n⚖️  INDICI DI EQUITÀ (Coefficiente di Variazione):")
    print("   (Più basso = più equo, <10% = ottimo, 10-20% = accettabile, >20% = squilibrato)")
    print()
    
    for col in df_metriche.columns:
        if df_metriche[col].std() > 0:
            cv = (df_metriche[col].std() / df_metriche[col].mean()) * 100
            status = "✅ OTTIMO" if cv < 10 else ("⚠️  ACCETTABILE" if cv < 20 else "❌ SQUILIBRATO")
            print(f"   {col:25} : CV = {cv:5.2f}% {status}")
    
    return df_metriche

def confronti_diretti(df_cal, df_metriche):
    """Confronti diretti tra coppie di colleghi"""
    print("\n" + "="*70)
    print("🔍 CONFRONTI DIRETTI TRA COLLEGHI")
    print("="*70)
    
    staff_list = sorted(df_cal['staff'].unique())
    
    # Esempi specifici richiesti
    confronti = [
        ('VISSANI', 'PAGANO'),
        ('PAGANO', 'PACINI'),
        ('TAMBERI', 'MORALE'),
        ('CIRCELLI', 'VISSANI')
    ]
    
    for staff1, staff2 in confronti:
        if staff1 in staff_list and staff2 in staff_list:
            print(f"\n{'='*70}")
            print(f"📊 CONFRONTO: {staff1} vs {staff2}")
            print('='*70)
            
            # Prendi metriche
            m1 = df_metriche.loc[staff1]
            m2 = df_metriche.loc[staff2]
            
            # Confronto metrica per metrica
            for metrica in df_metriche.columns:
                val1 = m1[metrica]
                val2 = m2[metrica]
                diff = val1 - val2
                
                if val2 != 0:
                    perc_diff = (diff / val2) * 100
                    simbolo = ">" if diff > 0 else ("<" if diff < 0 else "=")
                    
                    # Alert se differenza > 20%
                    alert = " ⚠️  SIGNIFICATIVO!" if abs(perc_diff) > 20 else ""
                    
                    print(f"   {metrica:25}: {staff1}={val1:7.2f} {simbolo} {staff2}={val2:7.2f} " +
                          f"(diff: {diff:+7.2f}, {perc_diff:+6.1f}%){alert}")

def identifica_anomalie(df_cal, df_metriche):
    """Identifica anomalie e violazioni delle best practice HR"""
    print("\n" + "="*70)
    print("🚨 IDENTIFICAZIONE ANOMALIE E VIOLAZIONI")
    print("="*70)
    
    anomalie = []
    
    # 1. Troppi giorni consecutivi senza riposo
    print("\n1️⃣  Controllo giorni lavorativi consecutivi eccessivi (>6):")
    for staff in sorted(df_cal['staff'].unique()):
        df_staff = df_cal[df_cal['staff'] == staff].sort_values('data_dt')
        
        giorni_lavoro_consecutivi = 0
        max_consecutivi = 0
        
        for idx, row in df_staff.iterrows():
            if row['is_lavorato']:
                giorni_lavoro_consecutivi += 1
                max_consecutivi = max(max_consecutivi, giorni_lavoro_consecutivi)
            else:
                giorni_lavoro_consecutivi = 0
        
        if max_consecutivi > 6:
            print(f"   ⚠️  {staff}: {max_consecutivi} giorni lavorativi consecutivi")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Troppi giorni consecutivi',
                'Dettaglio': f'{max_consecutivi} giorni',
                'Gravità': 'ALTA' if max_consecutivi > 9 else 'MEDIA'
            })
    
    # 2. Squilibrio festivi
    print("\n2️⃣  Controllo equità festivi:")
    festivi_per_staff = df_cal[df_cal['is_festivo'] & df_cal['is_lavorato']].groupby('staff').size()
    if len(festivi_per_staff) > 0:
        media_festivi = festivi_per_staff.mean()
        for staff, count in festivi_per_staff.items():
            if abs(count - media_festivi) > 2:
                print(f"   ⚠️  {staff}: {count} festivi (media: {media_festivi:.1f})")
                anomalie.append({
                    'Staff': staff,
                    'Tipo': 'Squilibrio festivi',
                    'Dettaglio': f'{count} vs media {media_festivi:.1f}',
                    'Gravità': 'MEDIA'
                })
    
    # 3. Ore totali sbilanciate
    print("\n3️⃣  Controllo equità ore totali:")
    ore_per_staff = df_metriche['Ore Totali']
    media_ore = ore_per_staff.mean()
    for staff, ore in ore_per_staff.items():
        diff_perc = abs((ore - media_ore) / media_ore * 100)
        if diff_perc > 15:
            print(f"   ⚠️  {staff}: {ore:.1f} ore (media: {media_ore:.1f}, diff: {diff_perc:.1f}%)")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Squilibrio ore totali',
                'Dettaglio': f'{diff_perc:.1f}% dalla media',
                'Gravità': 'ALTA' if diff_perc > 25 else 'MEDIA'
            })
    
    # 4. Weekend lavorati
    print("\n4️⃣  Controllo equità weekend lavorati:")
    weekend_per_staff = df_metriche['Weekend Lavorati']
    media_weekend = weekend_per_staff.mean()
    for staff, count in weekend_per_staff.items():
        diff = abs(count - media_weekend)
        if diff > 3:
            print(f"   ⚠️  {staff}: {count} weekend (media: {media_weekend:.1f})")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Squilibrio weekend',
                'Dettaglio': f'{count} vs media {media_weekend:.1f}',
                'Gravità': 'BASSA'
            })
    
    # Riepilogo anomalie
    if anomalie:
        print(f"\n📋 RIEPILOGO ANOMALIE TROVATE: {len(anomalie)}")
        df_anomalie = pd.DataFrame(anomalie)
        print(df_anomalie.to_string(index=False))
        return df_anomalie
    else:
        print("\n✅ Nessuna anomalia significativa rilevata!")
        return None

def genera_report_hr(df_cal, df_metriche, festivi_lavorati, riposi_consecutivi, anomalie):
    """Genera report Excel completo per HR"""
    print("\n" + "="*70)
    print("📄 GENERAZIONE REPORT HR COMPLETO")
    print("="*70)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output_file = base_path / 'REPORT_HR_EQUITA_COMPLIANCE.xlsx'
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Foglio 1: Executive Summary
            summary = pd.DataFrame({
                'Metrica': [
                    'Periodo Analizzato',
                    'Numero Staff',
                    'Giorni Totali Analizzati',
                    'Festivi nel Periodo',
                    'Anomalie Rilevate',
                    'Livello Equità Generale'
                ],
                'Valore': [
                    f"{df_cal['data_dt'].min().strftime('%d/%m/%Y')} - {df_cal['data_dt'].max().strftime('%d/%m/%Y')}",
                    df_cal['staff'].nunique(),
                    len(df_cal['data'].unique()),
                    len(FESTIVITA_2025),
                    len(anomalie) if anomalie is not None else 0,
                    'Da valutare'
                ]
            })
            summary.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Foglio 2: Calendario Completo
            df_cal_export = df_cal.copy()
            df_cal_export['data_dt'] = df_cal_export['data_dt'].dt.strftime('%d/%m/%Y')
            df_cal_export.to_excel(writer, sheet_name='Calendario Completo', index=False)
            
            # Foglio 3: Metriche Equità
            df_metriche.to_excel(writer, sheet_name='Metriche Equità')
            
            # Foglio 4: Festivi Lavorati
            if festivi_lavorati is not None:
                festivi_lavorati.to_excel(writer, sheet_name='Festivi Lavorati')
            
            # Foglio 5: Riposi Consecutivi
            if riposi_consecutivi is not None:
                riposi_consecutivi.to_excel(writer, sheet_name='Riposi Consecutivi')
            
            # Foglio 6: Anomalie
            if anomalie is not None:
                anomalie.to_excel(writer, sheet_name='Anomalie Rilevate', index=False)
            
            # Foglio 7: Confronti Diretti (Matrice)
            confronti_matrix = pd.DataFrame(index=df_metriche.index, columns=['Ore Totali', 'Festivi', 'Weekend', 'Riposi'])
            for staff in df_metriche.index:
                confronti_matrix.loc[staff, 'Ore Totali'] = df_metriche.loc[staff, 'Ore Totali']
                confronti_matrix.loc[staff, 'Festivi'] = df_metriche.loc[staff, 'Festivi Lavorati']
                confronti_matrix.loc[staff, 'Weekend'] = df_metriche.loc[staff, 'Weekend Lavorati']
                confronti_matrix.loc[staff, 'Riposi'] = df_metriche.loc[staff, 'Giorni Riposo']
            confronti_matrix.to_excel(writer, sheet_name='Confronti Matrix')
        
        print(f"✅ Report HR salvato: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Errore nel salvataggio: {e}")
        return None

def main():
    print("="*70)
    print("⚖️  ANALISI EQUITÀ HR E COMPLIANCE")
    print("   Revisore Risorse Umane - Analisi Scrupolosa")
    print("="*70)
    
    # Carica dati
    df = load_data()
    if df is None:
        return
    
    print(f"\n✅ Dati caricati: {len(df)} turni")
    
    # Genera calendario completo
    df_cal = genera_calendario_completo(df)
    
    # Esegui tutte le analisi
    festivi_lavorati = analisi_festivi_lavorati(df_cal)
    riposi_consecutivi = analisi_riposi_consecutivi(df_cal)
    df_metriche = analisi_equita_generale(df_cal)
    confronti_diretti(df_cal, df_metriche)
    anomalie = identifica_anomalie(df_cal, df_metriche)
    
    # Genera report finale
    report_file = genera_report_hr(df_cal, df_metriche, festivi_lavorati, riposi_consecutivi, anomalie)
    
    print("\n" + "="*70)
    print("✅ ANALISI HR COMPLETATA!")
    print("="*70)
    
    if report_file:
        print(f"\n📄 Report salvato: {report_file.name}")
        print("\n💡 Il report contiene:")
        print("   • Executive Summary")
        print("   • Calendario Completo con festivi")
        print("   • Metriche di Equità")
        print("   • Analisi Festivi Lavorati")
        print("   • Riposi Consecutivi")
        print("   • Anomalie Rilevate")
        print("   • Matrice Confronti")

if __name__ == '__main__':
    main()

