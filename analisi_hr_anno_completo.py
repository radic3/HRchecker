#!/usr/bin/env python3
"""
Analisi HR Completa - TUTTE le 52 settimane dell'anno 2025
Analisi di equità, festivi, riposi consecutivi e anomalie
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import calendar
import warnings
warnings.filterwarnings('ignore')

# Festività italiane 2025
FESTIVITA_2025 = {
    '2025-01-01': 'Capodanno',
    '2025-01-06': 'Epifania',
    '2025-04-20': 'Pasqua',
    '2025-04-21': 'Lunedì dell\'Angelo',
    '2025-04-25': 'Festa della Liberazione',
    '2025-05-01': 'Festa del Lavoro',
    '2025-06-02': 'Festa della Repubblica',
    '2025-08-15': 'Ferragosto',
    '2025-11-01': 'Ognissanti',
    '2025-12-08': 'Immacolata Concezione',
    '2025-12-25': 'Natale',
    '2025-12-26': 'Santo Stefano'
}

def load_data():
    """Carica i dati completi con tutte le 52 settimane"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    csv_file = base_path / 'turni_completi_52_settimane.csv'
    
    if not csv_file.exists():
        print("❌ Errore: Esegui prima extract_turni_completo.py!")
        return None
    
    df = pd.read_csv(csv_file)
    print(f"✅ Dati caricati: {len(df)} turni da {df['settimana'].nunique()} settimane")
    return df

def parse_date_from_filename(data_inizio, data_fine):
    """Converte date dal formato DDMMYY a datetime"""
    try:
        if pd.notna(data_inizio) and pd.notna(data_fine):
            # Formato: DDMMYY o DD.MM.YY
            d_start = str(data_inizio).replace('.', '').zfill(6)
            d_end = str(data_fine).replace('.', '').zfill(6)
            
            if len(d_start) >= 6 and len(d_end) >= 6:
                day_s, month_s, year_s = d_start[:2], d_start[2:4], d_start[4:6]
                day_e, month_e, year_e = d_end[:2], d_end[2:4], d_end[4:6]
                
                start = datetime(2000 + int(year_s), int(month_s), int(day_s))
                end = datetime(2000 + int(year_e), int(month_e), int(day_e))
                
                return start, end
    except Exception as e:
        pass
    
    return None, None

def genera_calendario_anno_completo(df):
    """Genera calendario completo per tutto l'anno"""
    print("\n" + "="*70)
    print("📅 GENERAZIONE CALENDARIO ANNO COMPLETO")
    print("="*70)
    
    calendario = []
    staff_set = set(df['staff'].unique())
    
    # Processa ogni settimana
    for settimana in sorted(df['settimana'].dropna().unique()):
        df_sett = df[df['settimana'] == settimana]
        
        # Prendi primo record per date
        row = df_sett.iloc[0]
        start, end = parse_date_from_filename(row['data_inizio'], row['data_fine'])
        
        if start and end:
            current = start
            day_num = 0
            
            while current <= end and day_num < 7:  # Max 7 giorni per settimana
                data_str = current.strftime('%Y-%m-%d')
                giorno_settimana = calendar.day_name[current.weekday()]
                is_festivo = data_str in FESTIVITA_2025
                nome_festivo = FESTIVITA_2025.get(data_str, '')
                is_weekend = current.weekday() >= 5
                
                # Per ogni membro staff, cerca il turno per quel giorno
                for staff in staff_set:
                    df_staff_day = df_sett[df_sett['staff'] == staff]
                    
                    if len(df_staff_day) > 0:
                        # Se ci sono più turni, prendi il primo
                        turno_info = df_staff_day.iloc[0]
                        
                        calendario.append({
                            'data': data_str,
                            'data_formattata': current.strftime('%d/%m/%Y'),
                            'anno': current.year,
                            'mese': current.month,
                            'giorno_mese': current.day,
                            'giorno_settimana': giorno_settimana,
                            'numero_settimana': int(settimana),
                            'staff': staff,
                            'tipo_turno': turno_info['tipo_turno'],
                            'ore_lavoro': turno_info['ore_lavoro'],
                            'ora_entrata': turno_info['ora_entrata'],
                            'ora_uscita': turno_info['ora_uscita'],
                            'is_festivo': is_festivo,
                            'nome_festivo': nome_festivo,
                            'is_weekend': is_weekend,
                            'is_lavorato': turno_info['tipo_turno'] == 'NORMALE',
                            'is_riposo': turno_info['tipo_turno'] in ['RIPO', 'RDOM'],
                            'is_ferie': turno_info['tipo_turno'] == 'FERIOR',
                            'is_off': turno_info['tipo_turno'] in ['OFF', 'CHIUSO']
                        })
                
                current += timedelta(days=1)
                day_num += 1
    
    df_cal = pd.DataFrame(calendario)
    df_cal['data_dt'] = pd.to_datetime(df_cal['data'])
    
    print(f"✅ Calendario generato:")
    print(f"   Periodo: {df_cal['data_dt'].min().strftime('%d/%m/%Y')} - {df_cal['data_dt'].max().strftime('%d/%m/%Y')}")
    print(f"   Giorni totali: {len(df_cal['data'].unique())} giorni")
    print(f"   Settimane: {df_cal['numero_settimana'].nunique()}")
    print(f"   Staff: {df_cal['staff'].nunique()}")
    print(f"   Record totali: {len(df_cal)}")
    
    return df_cal

def analisi_festivi_anno_completo(df_cal):
    """Analizza festivi lavorati su tutto l'anno"""
    print("\n" + "="*70)
    print("🎄 ANALISI FESTIVI - ANNO COMPLETO")
    print("="*70)
    
    # Trova tutti i festivi nel calendario
    df_festivi = df_cal[df_cal['is_festivo'] == True].copy()
    
    print(f"\n📊 Festivi totali nell'anno: {len(df_festivi['nome_festivo'].unique())}")
    print(f"Giorni festivi nel calendario: {len(df_festivi) // df_cal['staff'].nunique()}")
    
    # Festivi lavorati per staff
    festivi_lavorati = df_festivi[df_festivi['is_lavorato']].groupby('staff').agg({
        'data': 'count',
        'nome_festivo': lambda x: list(sorted(set(x)))
    }).rename(columns={'data': 'N. Festivi Lavorati', 'nome_festivo': 'Quali Festivi'})
    
    # Aggiungi anche chi non ha lavorato festivi
    for staff in df_cal['staff'].unique():
        if staff not in festivi_lavorati.index:
            festivi_lavorati.loc[staff] = [0, []]
    
    festivi_lavorati = festivi_lavorati.sort_values('N. Festivi Lavorati', ascending=False)
    
    print("\n🏆 FESTIVI LAVORATI PER STAFF:")
    for staff, row in festivi_lavorati.iterrows():
        festivi_list = row['Quali Festivi']
        if isinstance(festivi_list, list) and len(festivi_list) > 0:
            festivi_str = ', '.join(festivi_list[:3])
            if len(festivi_list) > 3:
                festivi_str += f" e altri {len(festivi_list)-3}"
        else:
            festivi_str = "Nessuno"
        print(f"   {staff:12}: {int(row['N. Festivi Lavorati']):2d} festivi - {festivi_str}")
    
    # Statistiche equità
    conteggi = festivi_lavorati['N. Festivi Lavorati'].astype(int)
    media = conteggi.mean()
    std = conteggi.std()
    
    print(f"\n📈 Statistiche:")
    print(f"   Media festivi lavorati: {media:.2f}")
    print(f"   Deviazione standard: {std:.2f}")
    print(f"   Min: {conteggi.min()}")
    print(f"   Max: {conteggi.max()}")
    print(f"   Differenza Max-Min: {conteggi.max() - conteggi.min()}")
    
    # Calcola CV
    if media > 0:
        cv = (std / media) * 100
        status = "✅ OTTIMO" if cv < 10 else ("⚠️  ACCETTABILE" if cv < 20 else "❌ SQUILIBRATO")
        print(f"   Coefficiente di Variazione: {cv:.2f}% {status}")
    
    # Alert squilibri
    threshold = max(2, media * 0.3)
    print(f"\n⚠️  ALERT SQUILIBRI (scostamento > ±30% o > ±2):")
    alert_trovati = False
    for staff, row in festivi_lavorati.iterrows():
        diff = abs(row['N. Festivi Lavorati'] - media)
        if diff > threshold:
            perc = (diff / media * 100) if media > 0 else 0
            alert_trovati = True
            print(f"   🚨 {staff}: {int(row['N. Festivi Lavorati'])} festivi (scostamento: {perc:.1f}%)")
    
    if not alert_trovati:
        print("   ✅ Nessuno squilibrio significativo")
    
    return festivi_lavorati

def analisi_riposi_anno_completo(df_cal):
    """Analisi riposi consecutivi su tutto l'anno"""
    print("\n" + "="*70)
    print("😴 ANALISI RIPOSI CONSECUTIVI - ANNO COMPLETO")
    print("="*70)
    
    risultati = {}
    
    for staff in sorted(df_cal['staff'].unique()):
        df_staff = df_cal[df_cal['staff'] == staff].sort_values('data_dt')
        
        sequenze_riposo = []
        giorni_consecutivi = 0
        sequenze_lavoro = []
        giorni_lavoro_consecutivi = 0
        
        for idx, row in df_staff.iterrows():
            # Conta riposi
            if row['is_riposo'] or row['is_off'] or row['is_ferie']:
                giorni_consecutivi += 1
                if giorni_lavoro_consecutivi > 0:
                    sequenze_lavoro.append(giorni_lavoro_consecutivi)
                giorni_lavoro_consecutivi = 0
            else:
                if giorni_consecutivi > 0:
                    sequenze_riposo.append(giorni_consecutivi)
                giorni_consecutivi = 0
                if row['is_lavorato']:
                    giorni_lavoro_consecutivi += 1
        
        # Ultime sequenze
        if giorni_consecutivi > 0:
            sequenze_riposo.append(giorni_consecutivi)
        if giorni_lavoro_consecutivi > 0:
            sequenze_lavoro.append(giorni_lavoro_consecutivi)
        
        # Conta sequenze per lunghezza
        riposi_1 = sum(1 for x in sequenze_riposo if x == 1)
        riposi_2 = sum(1 for x in sequenze_riposo if x == 2)
        riposi_3 = sum(1 for x in sequenze_riposo if x == 3)
        riposi_4plus = sum(1 for x in sequenze_riposo if x >= 4)
        
        risultati[staff] = {
            'Riposi 1 giorno': riposi_1,
            'Riposi 2 giorni': riposi_2,
            'Riposi 3 giorni': riposi_3,
            'Riposi 4+ giorni': riposi_4plus,
            'Totale Sequenze Riposo': len(sequenze_riposo),
            'Giorni Riposo Totali': sum(sequenze_riposo) if sequenze_riposo else 0,
            'Media Giorni/Sequenza': round(np.mean(sequenze_riposo), 2) if sequenze_riposo else 0,
            'Max Riposo Consecutivo': max(sequenze_riposo) if sequenze_riposo else 0,
            'Max Lavoro Consecutivo': max(sequenze_lavoro) if sequenze_lavoro else 0
        }
    
    df_riposi = pd.DataFrame(risultati).T
    df_riposi = df_riposi.astype(int, errors='ignore')
    
    print("\n📊 RIPOSI CONSECUTIVI - STATISTICHE COMPLETE:")
    print(df_riposi.to_string())
    
    # Analisi equità riposi
    print("\n📈 ANALISI EQUITÀ RIPOSI:")
    media_totali = df_riposi['Giorni Riposo Totali'].mean()
    print(f"   Media giorni riposo: {media_totali:.2f}")
    
    for staff, row in df_riposi.iterrows():
        diff_perc = ((row['Giorni Riposo Totali'] - media_totali) / media_totali * 100) if media_totali > 0 else 0
        status = "✅" if abs(diff_perc) < 20 else "⚠️" if abs(diff_perc) < 30 else "❌"
        print(f"   {staff:12}: {int(row['Giorni Riposo Totali']):3d} giorni ({diff_perc:+6.1f}%) {status}")
    
    # Alert giorni lavorativi consecutivi eccessivi
    print(f"\n🚨 ALERT GIORNI LAVORATIVI CONSECUTIVI:")
    for staff, row in df_riposi.iterrows():
        max_consec = row['Max Lavoro Consecutivo']
        if max_consec > 7:
            gravita = "🔴 CRITICA" if max_consec > 14 else "🟠 ALTA" if max_consec > 10 else "🟡 MEDIA"
            print(f"   {staff:12}: {int(max_consec):3d} giorni consecutivi {gravita}")
    
    return df_riposi

def analisi_equita_anno_completo(df_cal):
    """Analisi equità completa anno"""
    print("\n" + "="*70)
    print("⚖️  ANALISI EQUITÀ - ANNO COMPLETO")
    print("="*70)
    
    metriche = {}
    
    for staff in sorted(df_cal['staff'].unique()):
        df_staff = df_cal[df_cal['staff'] == staff]
        
        # Conta giorni per categoria
        giorni_lavorati = df_staff['is_lavorato'].sum()
        giorni_riposo = df_staff['is_riposo'].sum()
        giorni_ferie = df_staff['is_ferie'].sum()
        giorni_off = df_staff['is_off'].sum()
        
        # Weekend e festivi lavorati
        weekend_lavorati = df_staff[df_staff['is_weekend'] & df_staff['is_lavorato']].shape[0]
        festivi_lavorati = df_staff[df_staff['is_festivo'] & df_staff['is_lavorato']].shape[0]
        
        # Ore
        ore_totali = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum()
        media_ore_giorno = df_staff[df_staff['is_lavorato'] & df_staff['ore_lavoro'].notna()]['ore_lavoro'].mean()
        
        metriche[staff] = {
            'Giorni Calendario': len(df_staff),
            'Giorni Lavorati': int(giorni_lavorati),
            'Giorni Riposo': int(giorni_riposo),
            'Giorni Ferie': int(giorni_ferie),
            'Giorni OFF/Chiuso': int(giorni_off),
            'Weekend Lavorati': int(weekend_lavorati),
            'Festivi Lavorati': int(festivi_lavorati),
            'Ore Totali': round(ore_totali, 1),
            'Media Ore/Giorno Lav': round(media_ore_giorno, 2) if pd.notna(media_ore_giorno) else 0
        }
    
    df_metriche = pd.DataFrame(metriche).T
    
    print("\n📊 METRICHE COMPLETE PER STAFF:")
    print(df_metriche.to_string())
    
    # Calcola e mostra CV per ogni metrica
    print("\n⚖️  COEFFICIENTI DI VARIAZIONE (Indici di Equità):")
    print("   " + "="*60)
    print(f"   {'Metrica':<30} {'CV':>8} {'Status':>20}")
    print("   " + "="*60)
    
    cv_results = {}
    for col in df_metriche.columns:
        if df_metriche[col].std() > 0 and df_metriche[col].mean() > 0:
            cv = (df_metriche[col].std() / df_metriche[col].mean()) * 100
            status = "✅ OTTIMO" if cv < 10 else ("⚠️  ACCETTABILE" if cv < 20 else "❌ SQUILIBRATO")
            cv_results[col] = cv
            print(f"   {col:<30} {cv:7.2f}% {status:>20}")
    
    print("   " + "="*60)
    print(f"\n   Legenda: <10%=Ottimo | 10-20%=Accettabile | >20%=Squilibrato")
    
    return df_metriche, cv_results

def confronti_dettagliati_anno(df_cal, df_metriche):
    """Confronti dettagliati tra tutti i colleghi"""
    print("\n" + "="*70)
    print("🔍 CONFRONTI DIRETTI - ANNO COMPLETO")
    print("="*70)
    
    confronti_richiesti = [
        ('VISSANI', 'PAGANO'),
        ('PAGANO', 'PACINI'),
        ('TAMBERI', 'MORALE'),
        ('CIRCELLI', 'VISSANI'),
        ('CIRCELLI', 'TAMBERI'),
        ('MORALE', 'PACINI')
    ]
    
    risultati_confronti = []
    
    for staff1, staff2 in confronti_richiesti:
        if staff1 not in df_metriche.index or staff2 not in df_metriche.index:
            continue
        
        print(f"\n{'='*70}")
        print(f"📊 CONFRONTO: {staff1} vs {staff2}")
        print('='*70)
        
        m1 = df_metriche.loc[staff1]
        m2 = df_metriche.loc[staff2]
        
        disparita_count = 0
        
        for metrica in ['Ore Totali', 'Giorni Lavorati', 'Giorni Riposo', 
                        'Weekend Lavorati', 'Festivi Lavorati']:
            val1 = m1[metrica]
            val2 = m2[metrica]
            diff = val1 - val2
            
            if val2 != 0:
                perc_diff = (diff / val2) * 100
                simbolo = ">" if diff > 0 else ("<" if diff < 0 else "=")
                
                # Determina gravità
                if abs(perc_diff) > 20:
                    alert = " 🚨 DISPARITÀ SIGNIFICATIVA!"
                    disparita_count += 1
                elif abs(perc_diff) > 10:
                    alert = " ⚠️  Attenzione"
                else:
                    alert = " ✅"
                
                print(f"   {metrica:20}: {staff1}={val1:7.1f} {simbolo} {staff2}={val2:7.1f} " +
                      f"(diff: {diff:+7.1f}, {perc_diff:+6.1f}%){alert}")
        
        # Conclusione
        print(f"\n   📊 CONCLUSIONE: ", end="")
        if disparita_count == 0:
            print("✅ Distribuzione EQUA")
        elif disparita_count <= 2:
            print(f"⚠️  {disparita_count} disparità riscontrate")
        else:
            print(f"❌ SQUILIBRIO SIGNIFICATIVO ({disparita_count} metriche sbilanciate)")
        
        risultati_confronti.append({
            'Staff1': staff1,
            'Staff2': staff2,
            'Disparità': disparita_count,
            'Status': 'EQUO' if disparita_count == 0 else 'SQUILIBRATO'
        })
    
    return pd.DataFrame(risultati_confronti)

def identifica_anomalie_anno(df_cal, df_metriche, df_riposi):
    """Identifica tutte le anomalie sull'anno completo"""
    print("\n" + "="*70)
    print("🚨 IDENTIFICAZIONE ANOMALIE - ANNO COMPLETO")
    print("="*70)
    
    anomalie = []
    
    # 1. Giorni consecutivi eccessivi
    print("\n1️⃣  Giorni lavorativi consecutivi:")
    for staff, row in df_riposi.iterrows():
        max_consec = row['Max Lavoro Consecutivo']
        if max_consec > 7:
            gravita = "CRITICA" if max_consec > 14 else "ALTA" if max_consec > 10 else "MEDIA"
            print(f"   🚨 {staff}: {int(max_consec)} giorni - Gravità: {gravita}")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Giorni consecutivi eccessivi',
                'Valore': f'{int(max_consec)} giorni',
                'Gravità': gravita
            })
    
    # 2. Squilibrio riposi totali
    print("\n2️⃣  Squilibrio riposi totali:")
    media_riposi = df_metriche['Giorni Riposo'].mean()
    for staff, val in df_metriche['Giorni Riposo'].items():
        diff_perc = ((val - media_riposi) / media_riposi * 100) if media_riposi > 0 else 0
        if abs(diff_perc) > 30:
            print(f"   🚨 {staff}: {int(val)} giorni ({diff_perc:+.1f}% vs media {media_riposi:.1f})")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Squilibrio riposi',
                'Valore': f'{int(val)} giorni ({diff_perc:+.1f}%)',
                'Gravità': 'ALTA' if abs(diff_perc) > 50 else 'MEDIA'
            })
    
    # 3. Squilibrio ore totali
    print("\n3️⃣  Squilibrio ore totali:")
    media_ore = df_metriche['Ore Totali'].mean()
    for staff, ore in df_metriche['Ore Totali'].items():
        diff_perc = ((ore - media_ore) / media_ore * 100)
        if abs(diff_perc) > 20:
            print(f"   🚨 {staff}: {ore:.1f} ore ({diff_perc:+.1f}% vs media {media_ore:.1f})")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Squilibrio ore totali',
                'Valore': f'{ore:.1f} ore ({diff_perc:+.1f}%)',
                'Gravità': 'ALTA' if abs(diff_perc) > 30 else 'MEDIA'
            })
    
    # 4. Festivi squilibrati
    print("\n4️⃣  Squilibrio festivi:")
    media_festivi = df_metriche['Festivi Lavorati'].mean()
    for staff, fest in df_metriche['Festivi Lavorati'].items():
        diff = abs(fest - media_festivi)
        if diff >= 2:
            print(f"   🚨 {staff}: {int(fest)} festivi (media: {media_festivi:.1f})")
            anomalie.append({
                'Staff': staff,
                'Tipo': 'Squilibrio festivi',
                'Valore': f'{int(fest)} festivi vs {media_festivi:.1f}',
                'Gravità': 'MEDIA'
            })
    
    if anomalie:
        df_anomalie = pd.DataFrame(anomalie)
        print(f"\n📋 TOTALE ANOMALIE TROVATE: {len(df_anomalie)}")
        
        # Conta per gravità
        gravi = len(df_anomalie[df_anomalie['Gravità'] == 'CRITICA'])
        alte = len(df_anomalie[df_anomalie['Gravità'] == 'ALTA'])
        medie = len(df_anomalie[df_anomalie['Gravità'] == 'MEDIA'])
        
        print(f"   🔴 Critiche: {gravi}")
        print(f"   🟠 Alte: {alte}")
        print(f"   🟡 Medie: {medie}")
        
        return df_anomalie
    else:
        print("\n✅ Nessuna anomalia rilevata")
        return None

def genera_report_hr_completo(df, df_cal, df_metriche, festivi, riposi, anomalie, confronti, cv_results):
    """Genera report Excel super completo"""
    print("\n" + "="*70)
    print("📄 GENERAZIONE REPORT EXCEL - ANNO COMPLETO")
    print("="*70)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output_file = base_path / 'REPORT_HR_ANNO_COMPLETO_2025.xlsx'
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Foglio 1: Executive Summary
            periodo_min = df_cal['data_dt'].min().strftime('%d/%m/%Y')
            periodo_max = df_cal['data_dt'].max().strftime('%d/%m/%Y')
            
            summary = pd.DataFrame({
                'Metrica': [
                    'Periodo Analizzato',
                    'Numero Settimane',
                    'Giorni Calendario',
                    'Numero Staff',
                    'Totale Turni Estratti',
                    'Festivi nell\'Anno',
                    'Anomalie Critiche',
                    'Anomalie Alte',
                    'Anomalie Medie',
                    'Livello Equità Generale'
                ],
                'Valore': [
                    f"{periodo_min} - {periodo_max}",
                    df['settimana'].nunique(),
                    len(df_cal['data'].unique()),
                    df_cal['staff'].nunique(),
                    len(df),
                    len(FESTIVITA_2025),
                    len(anomalie[anomalie['Gravità'] == 'CRITICA']) if anomalie is not None else 0,
                    len(anomalie[anomalie['Gravità'] == 'ALTA']) if anomalie is not None else 0,
                    len(anomalie[anomalie['Gravità'] == 'MEDIA']) if anomalie is not None else 0,
                    'VEDERE FOGLI DETTAGLIO'
                ]
            })
            summary.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Foglio 2: Calendario Anno Completo
            df_cal_export = df_cal.copy()
            df_cal_export = df_cal_export.sort_values(['staff', 'data_dt'])
            df_cal_export['data_dt'] = df_cal_export['data_dt'].dt.strftime('%d/%m/%Y')
            df_cal_export.to_excel(writer, sheet_name='Calendario Anno', index=False)
            
            # Foglio 3: Metriche Equità
            df_metriche.to_excel(writer, sheet_name='Metriche Equità')
            
            # Foglio 4: Indici CV
            df_cv = pd.DataFrame(list(cv_results.items()), columns=['Metrica', 'Coefficiente Variazione'])
            df_cv['Status'] = df_cv['Coefficiente Variazione'].apply(
                lambda x: 'OTTIMO' if x < 10 else ('ACCETTABILE' if x < 20 else 'SQUILIBRATO')
            )
            df_cv = df_cv.sort_values('Coefficiente Variazione', ascending=False)
            df_cv.to_excel(writer, sheet_name='Indici Equità (CV)', index=False)
            
            # Foglio 5: Festivi Anno
            if festivi is not None:
                festivi.to_excel(writer, sheet_name='Festivi Anno')
            
            # Foglio 6: Riposi Consecutivi
            if riposi is not None:
                riposi.to_excel(writer, sheet_name='Riposi Consecutivi')
            
            # Foglio 7: Anomalie
            if anomalie is not None:
                anomalie_sorted = anomalie.sort_values(['Gravità', 'Staff'])
                anomalie_sorted.to_excel(writer, sheet_name='Anomalie Rilevate', index=False)
            
            # Foglio 8: Confronti Diretti
            if confronti is not None:
                confronti.to_excel(writer, sheet_name='Confronti Diretti', index=False)
            
            # Foglio 9: Riepilogo per Mese
            df_cal_mese = df_cal.copy()
            df_cal_mese = df_cal_mese[df_cal_mese['is_lavorato']]
            if len(df_cal_mese) > 0:
                pivot_mese = df_cal_mese.groupby(['staff', 'mese']).agg({
                    'ore_lavoro': 'sum',
                    'data': 'count'
                }).round(1)
                pivot_mese.columns = ['Ore', 'Giorni']
                pivot_mese = pivot_mese.reset_index()
                pivot_wide = pivot_mese.pivot(index='staff', columns='mese', values='Ore')
                pivot_wide.columns = [f'Mese_{int(c)}' for c in pivot_wide.columns]
                pivot_wide.to_excel(writer, sheet_name='Ore per Mese')
            
            # Foglio 10: Turni per Settimana-Staff
            pivot_sett = df_cal[df_cal['is_lavorato']].groupby(['staff', 'numero_settimana']).size().reset_index(name='N_Turni')
            pivot_sett_wide = pivot_sett.pivot(index='staff', columns='numero_settimana', values='N_Turni')
            pivot_sett_wide = pivot_sett_wide.fillna(0).astype(int)
            pivot_sett_wide.columns = [f'Sett_{int(c)}' for c in pivot_sett_wide.columns]
            pivot_sett_wide.to_excel(writer, sheet_name='Turni per Settimana')
        
        print(f"✅ Report salvato: {output_file}")
        print(f"\n📊 Contiene 10 fogli con analisi anno completo!")
        return output_file
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("="*70)
    print("⚖️  ANALISI HR - ANNO COMPLETO 2025")
    print("   Revisore Risorse Umane - 52 Settimane")
    print("="*70)
    
    # Carica dati
    df = load_data()
    if df is None:
        return
    
    print(f"\n📋 Settimane nel dataset: {sorted(df['settimana'].dropna().unique())}")
    
    # Genera calendario completo
    df_cal = genera_calendario_anno_completo(df)
    
    # Esegui tutte le analisi
    festivi_lavorati = analisi_festivi_anno_completo(df_cal)
    riposi_consecutivi = analisi_riposi_anno_completo(df_cal)
    df_metriche, cv_results = analisi_equita_anno_completo(df_cal)
    confronti = confronti_dettagliati_anno(df_cal, df_metriche)
    anomalie = identifica_anomalie_anno(df_cal, df_metriche, riposi_consecutivi)
    
    # Genera report Excel
    report_file = genera_report_hr_completo(df, df_cal, df_metriche, festivi_lavorati, 
                                            riposi_consecutivi, anomalie, confronti, cv_results)
    
    print("\n" + "="*70)
    print("✅ ANALISI ANNO COMPLETO TERMINATA!")
    print("="*70)
    
    if report_file:
        print(f"\n📄 Report salvato: {report_file.name}")
        print(f"\n📊 Statistiche finali:")
        print(f"   Settimane analizzate: {df['settimana'].nunique()}")
        print(f"   Giorni calendario: {len(df_cal['data'].unique())}")
        print(f"   Turni totali: {len(df)}")
        print(f"   Anomalie trovate: {len(anomalie) if anomalie is not None else 0}")

if __name__ == '__main__':
    main()

