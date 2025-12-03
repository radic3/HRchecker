#!/usr/bin/env python3
"""
Script completo per estrarre TUTTE le 52 settimane dai PDF ROTA
Con parsing migliorato per gestire tutti i formati di nome file
"""

import re
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import PyPDF2

# Nomi del personale
STAFF_NAMES = ['VISSANI', 'PACINI', 'CIRCELLI', 'PAGANO', 'TAMBERI', 'MORALE']
TURNO_TYPES = ['RIPO', 'FEST', 'ROL', 'FERIOR', 'RDOM', 'OFF', 'CHIUSO']

def extract_text_from_pdf(pdf_path):
    """Estrae il testo da un file PDF"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"  ⚠️  Errore nell'estrazione di {pdf_path}: {e}")
    return text

def parse_filename_improved(filename):
    """Parsing migliorato per estrarre il numero di settimana da TUTTI i formati"""
    
    # Prova diversi pattern per catturare il numero di settimana
    patterns = [
        r'ROTA\s*(\d+)\s*[_\s]*(mod\d+|MOD\d+)?[_\s]*(\d{6})-(\d{6})',  # ROTA 1 mod1_301224-050125
        r'ROTA\s*(\d+)\s*[_\s]*(mod\d+|MOD\d+)?_(\d+)[-.](\d+)',        # ROTA 10 _03.03-09.03
        r'ROTA\s*(\d+)\s*(MOD\d+|mod\d+)?_(\d+)-(\d+)',                 # ROTA 15 MOD1_07.04
        r'ROTA\s*(\d+)[_\s]+(\d+)',                                      # ROTA 17_210425
    ]
    
    week_num = None
    mod = ""
    date_start = None
    date_end = None
    
    for pattern in patterns:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            week_num = match.group(1)
            
            # Estrai mod se presente
            if len(match.groups()) >= 2 and match.group(2):
                if 'mod' in match.group(2).lower():
                    mod = match.group(2).lower()
            
            # Estrai date se presenti
            if len(match.groups()) >= 4:
                date_start = match.group(3) if match.group(3) else match.group(3)
                date_end = match.group(4) if match.group(4) else match.group(4)
            
            break
    
    # Se non troviamo il numero, provalo a estrarre direttamente
    if not week_num:
        simple_match = re.search(r'ROTA\s*(\d+)', filename, re.IGNORECASE)
        if simple_match:
            week_num = simple_match.group(1)
    
    return {
        'settimana': week_num,
        'modifiche': mod,
        'data_inizio': date_start,
        'data_fine': date_end
    }

def parse_date_from_text(text):
    """Estrae la data dall'inizio del testo (formato DD/MM/YY)"""
    match = re.search(r'(\d{2})/(\d{2})/(\d{2})', text)
    if match:
        return f"{match.group(1)}/{match.group(2)}/20{match.group(3)}"
    return None

def extract_turni_dettagliati(text, file_info):
    """Estrae i turni in modo dettagliato dal testo"""
    turni = []
    
    # Cerca la data all'inizio
    data_rota = parse_date_from_text(text)
    
    # Split per linee
    lines = text.split('\n')
    
    for line in lines:
        # Salta linee vuote o troppo corte
        if len(line.strip()) < 10:
            continue
        
        # Cerca pattern di turno con nome staff
        for staff_name in STAFF_NAMES:
            if staff_name in line:
                # Estrai orari nel formato HH:MM o HH.MM
                orari = re.findall(r'(\d{1,2})[:\.,](\d{2})', line)
                
                # Estrai numero di ore (formato X,Y o X.Y)
                ore_match = re.search(r'(\d+)[,\.](\d+)\s+\d{1,2}[:\.]\d{2}', line)
                ore_lavoro = None
                if ore_match:
                    ore_lavoro = float(f"{ore_match.group(1)}.{ore_match.group(2)}")
                
                # Identifica tipo di turno
                tipo_turno = "NORMALE"
                for turno_type in TURNO_TYPES:
                    if turno_type in line:
                        tipo_turno = turno_type
                        break
                
                # Estrai orari di entrata/uscita se presenti
                entrata = None
                uscita = None
                if len(orari) >= 2:
                    entrata = f"{orari[0][0].zfill(2)}:{orari[0][1]}"
                    uscita = f"{orari[1][0].zfill(2)}:{orari[1][1]}"
                
                # Crea record turno
                turno = {
                    'file': file_info.get('file', ''),
                    'settimana': file_info.get('settimana', ''),
                    'modifiche': file_info.get('modifiche', ''),
                    'data_inizio': file_info.get('data_inizio', ''),
                    'data_fine': file_info.get('data_fine', ''),
                    'data_rota': data_rota,
                    'staff': staff_name,
                    'tipo_turno': tipo_turno,
                    'ore_lavoro': ore_lavoro,
                    'ora_entrata': entrata,
                    'ora_uscita': uscita,
                    'linea_completa': line.strip()
                }
                turni.append(turno)
    
    return turni

def main():
    print("="*70)
    print("🔧 ESTRAZIONE COMPLETA - TUTTE LE 52 SETTIMANE")
    print("="*70)
    
    # Trova tutti i file PDF
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    pdf_files = sorted(base_path.glob('ROTA*.pdf'))
    
    print(f"\nTrovati {len(pdf_files)} file PDF\n")
    print("-" * 70)
    
    all_turni = []
    settimane_processate = set()
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] {pdf_file.name}")
        
        # Estrai informazioni dal nome file con parsing migliorato
        file_info = parse_filename_improved(pdf_file.name)
        file_info['file'] = pdf_file.name
        
        settimana = file_info.get('settimana', 'N/A')
        print(f"  📅 Settimana: {settimana} | Mod: {file_info.get('modifiche', '-')}")
        
        if settimana and settimana != 'N/A':
            settimane_processate.add(settimana)
        
        # Estrai testo dal PDF
        text = extract_text_from_pdf(pdf_file)
        
        # Parse turni
        turni = extract_turni_dettagliati(text, file_info)
        all_turni.extend(turni)
        
        print(f"  ✓ Estratti {len(turni)} turni")
    
    print(f"\n{'='*70}")
    print(f"RIEPILOGO ESTRAZIONE")
    print("="*70)
    print(f"Totale turni estratti: {len(all_turni)}")
    print(f"Settimane identificate: {len(settimane_processate)}")
    print(f"Settimane presenti: {sorted(settimane_processate)}")
    
    # Crea DataFrame
    df = pd.DataFrame(all_turni)
    
    # Converti settimana in numero
    df['settimana'] = pd.to_numeric(df['settimana'], errors='coerce')
    
    print(f"\n📊 Distribuzione turni per settimana:")
    sett_counts = df['settimana'].value_counts().sort_index()
    for sett, count in sett_counts.items():
        if pd.notna(sett):
            print(f"   Settimana {int(sett):2d}: {count:3d} turni")
    
    print(f"\n⚠️  Turni senza settimana identificata: {df['settimana'].isna().sum()}")
    
    # Salva CSV
    output_csv = base_path / 'turni_completi_52_settimane.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\n✅ CSV salvato: {output_csv}")
    
    # Salva Excel
    try:
        output_excel = base_path / 'turni_completi_52_settimane.xlsx'
        df.to_excel(output_excel, index=False)
        print(f"✅ Excel salvato: {output_excel}")
    except:
        print(f"⚠️  Excel non salvato (possibile problema con la dimensione)")
    
    print("\n" + "="*70)
    print("✅ ESTRAZIONE COMPLETATA!")
    print("="*70)

if __name__ == '__main__':
    main()

