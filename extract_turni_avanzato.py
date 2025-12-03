#!/usr/bin/env python3
"""
Script avanzato per estrarre turni dai PDF ROTA con parsing dettagliato
"""

import re
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import PyPDF2

# Nomi del personale (da aggiornare se necessario)
STAFF_NAMES = ['VISSANI', 'PACINI', 'CIRCELLI', 'PAGANO', 'TAMBERI', 'MORALE']

# Tipi di turno
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
        print(f"Errore nell'estrazione di {pdf_path}: {e}")
    return text

def parse_filename(filename):
    """Estrae informazioni dal nome del file"""
    match = re.search(r'ROTA\s+(\d+)\s*(mod\d+|MOD\d+)?[_\s]?(\d+)-(\d+)', filename, re.IGNORECASE)
    if match:
        week_num = match.group(1)
        mod = match.group(2).lower() if match.group(2) else ""
        date_start = match.group(3)
        date_fine = match.group(4)
        return {
            'settimana': week_num,
            'modifiche': mod,
            'data_inizio': date_start,
            'data_fine': date_fine
        }
    return None

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
                # Estrai orari nel formato HH:MM
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

def calcola_ore_per_staff(df):
    """Calcola le ore lavorate per ogni membro dello staff"""
    if 'ore_lavoro' in df.columns and 'staff' in df.columns:
        # Rimuovi valori None
        df_clean = df[df['ore_lavoro'].notna()].copy()
        
        ore_per_staff = df_clean.groupby('staff').agg({
            'ore_lavoro': ['sum', 'mean', 'count']
        }).round(2)
        
        ore_per_staff.columns = ['Totale Ore', 'Media Ore/Turno', 'N. Turni']
        return ore_per_staff
    return None

def analizza_distribuzione_turni(df):
    """Analizza la distribuzione dei turni"""
    stats = {}
    
    if 'tipo_turno' in df.columns:
        stats['Distribuzione Tipi Turno'] = df['tipo_turno'].value_counts()
    
    if 'staff' in df.columns:
        stats['Turni per Staff'] = df['staff'].value_counts()
    
    if 'ora_entrata' in df.columns:
        df_clean = df[df['ora_entrata'].notna()]
        if len(df_clean) > 0:
            stats['Orari Entrata Più Comuni'] = df_clean['ora_entrata'].value_counts().head(10)
    
    return stats

def main():
    print("="*70)
    print("ESTRAZIONE AVANZATA TURNI DA PDF")
    print("="*70)
    
    # Trova tutti i file PDF
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    pdf_files = sorted(base_path.glob('ROTA*.pdf'))
    
    print(f"\nTrovati {len(pdf_files)} file PDF\n")
    print("-" * 70)
    
    all_turni = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processando: {pdf_file.name}")
        
        # Estrai informazioni dal nome file
        file_info = parse_filename(pdf_file.name)
        if file_info:
            file_info['file'] = pdf_file.name
        else:
            file_info = {'file': pdf_file.name}
        
        # Estrai testo dal PDF
        text = extract_text_from_pdf(pdf_file)
        
        # Parse turni
        turni = extract_turni_dettagliati(text, file_info)
        all_turni.extend(turni)
        
        print(f"  ✓ Estratti {len(turni)} turni")
        
        # Mostra alcuni turni di esempio
        if turni and i <= 3:  # Solo per i primi 3 file
            print(f"  📋 Esempi:")
            for turno in turni[:3]:
                print(f"     - {turno['staff']}: {turno['tipo_turno']} " +
                      f"({turno['ora_entrata']}-{turno['ora_uscita']}, {turno['ore_lavoro']}h)")
    
    print(f"\n{'='*70}")
    print(f"TOTALE TURNI ESTRATTI: {len(all_turni)}")
    print("="*70)
    
    # Crea DataFrame
    df = pd.DataFrame(all_turni)
    
    # Salva CSV
    output_csv = base_path / 'turni_dettagliati.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV salvato: {output_csv}")
    
    # Calcola statistiche
    print("\n" + "="*70)
    print("STATISTICHE RAPIDE")
    print("="*70)
    
    # Ore per staff
    ore_staff = calcola_ore_per_staff(df)
    if ore_staff is not None:
        print("\n📊 ORE PER STAFF:")
        print(ore_staff)
    
    # Distribuzione turni
    stats = analizza_distribuzione_turni(df)
    for titolo, dati in stats.items():
        print(f"\n📊 {titolo.upper()}:")
        print(dati)
    
    # Salva Excel completo
    print(f"\n{'='*70}")
    print("GENERAZIONE EXCEL DETTAGLIATO")
    print("="*70)
    
    try:
        output_excel = base_path / 'turni_dettagliati.xlsx'
        
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            # Foglio 1: Tutti i turni
            df.to_excel(writer, sheet_name='Tutti i Turni', index=False)
            
            # Foglio 2: Ore per staff
            if ore_staff is not None:
                ore_staff.to_excel(writer, sheet_name='Ore per Staff')
            
            # Foglio 3: Riepilogo per settimana e staff
            if 'settimana' in df.columns and 'staff' in df.columns and 'ore_lavoro' in df.columns:
                pivot = df[df['ore_lavoro'].notna()].pivot_table(
                    values='ore_lavoro',
                    index='staff',
                    columns='settimana',
                    aggfunc='sum',
                    fill_value=0
                ).round(2)
                pivot.to_excel(writer, sheet_name='Ore per Settimana-Staff')
            
            # Foglio 4: Turni per tipo
            if 'tipo_turno' in df.columns:
                tipo_counts = df['tipo_turno'].value_counts().to_frame('Conteggio')
                tipo_counts.to_excel(writer, sheet_name='Tipi di Turno')
            
            # Foglio 5: Orari più comuni
            if 'ora_entrata' in df.columns:
                df_clean = df[df['ora_entrata'].notna()]
                if len(df_clean) > 0:
                    orari_counts = df_clean['ora_entrata'].value_counts().to_frame('Frequenza')
                    orari_counts.to_excel(writer, sheet_name='Orari Entrata')
        
        print(f"✓ Excel dettagliato salvato: {output_excel}")
        
    except Exception as e:
        print(f"⚠️  Errore nel salvataggio Excel: {e}")
    
    print("\n" + "="*70)
    print("✅ ESTRAZIONE COMPLETATA CON SUCCESSO!")
    print("="*70)
    print(f"\n📁 File generati:")
    print(f"   • turni_dettagliati.csv")
    print(f"   • turni_dettagliati.xlsx (con {len(all_turni)} turni)")
    print(f"\n📊 Anteprima dati:")
    print(df.head(10)[['staff', 'tipo_turno', 'ore_lavoro', 'ora_entrata', 'ora_uscita']])

if __name__ == '__main__':
    main()

