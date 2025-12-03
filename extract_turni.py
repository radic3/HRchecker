#!/usr/bin/env python3
"""
Script per estrarre e analizzare i turni dai file PDF ROTA
"""

import re
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

try:
    import PyPDF2
except ImportError:
    print("Installazione di PyPDF2...")
    os.system("pip3 install PyPDF2")
    import PyPDF2

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
    # Esempio: ROTA 1 mod1_301224-050125 - PISA.pdf
    match = re.search(r'ROTA\s+(\d+)\s*(mod\d+)?_?(\d+)-(\d+)', filename)
    if match:
        week_num = match.group(1)
        mod = match.group(2) if match.group(2) else ""
        date_start = match.group(3)
        date_end = match.group(4)
        return {
            'settimana': week_num,
            'modifiche': mod,
            'data_inizio': date_start,
            'data_fine': date_end
        }
    return None

def parse_turni_from_text(text):
    """Estrae i turni dal testo"""
    turni = []
    
    # Pattern comuni per turni (da adattare in base al formato reale)
    # Cerca linee con orari tipo "07:00-15:00" o giorni della settimana
    giorni = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica',
              'lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom']
    
    lines = text.split('\n')
    current_day = None
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Cerca giorni
        for giorno in giorni:
            if giorno in line_lower:
                current_day = giorno
                break
        
        # Cerca orari (pattern: HH:MM-HH:MM o HH:MM)
        orari = re.findall(r'\b(\d{1,2})[:\.](\d{2})\b', line)
        if orari and current_day:
            turni.append({
                'giorno': current_day,
                'orari': orari,
                'testo': line.strip()
            })
    
    return turni

def main():
    # Trova tutti i file PDF
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    pdf_files = sorted(base_path.glob('ROTA*.pdf'))
    
    print(f"Trovati {len(pdf_files)} file PDF")
    print("-" * 60)
    
    all_data = []
    
    for pdf_file in pdf_files:
        print(f"\nProcessando: {pdf_file.name}")
        
        # Estrai informazioni dal nome file
        file_info = parse_filename(pdf_file.name)
        
        # Estrai testo dal PDF
        text = extract_text_from_pdf(pdf_file)
        
        # Parse turni
        turni = parse_turni_from_text(text)
        
        # Salva dati
        for turno in turni:
            row = {
                'file': pdf_file.name,
                'settimana': file_info['settimana'] if file_info else '',
                'modifiche': file_info['modifiche'] if file_info else '',
                'data_inizio': file_info['data_inizio'] if file_info else '',
                'data_fine': file_info['data_fine'] if file_info else '',
                'giorno': turno.get('giorno', ''),
                'testo_turno': turno.get('testo', ''),
            }
            all_data.append(row)
        
        # Mostra anteprima del testo estratto
        print(f"Caratteri estratti: {len(text)}")
        print(f"Turni trovati: {len(turni)}")
        
        # Mostra prime righe del testo per debug
        preview = text[:500] if text else "Nessun testo estratto"
        print(f"Anteprima testo:\n{preview}\n")
    
    # Crea DataFrame
    df = pd.DataFrame(all_data)
    
    # Salva in CSV
    output_csv = base_path / 'turni_estratti.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\n{'='*60}")
    print(f"✓ Dati salvati in: {output_csv}")
    print(f"✓ Totale righe: {len(df)}")
    print(f"\nAnteprima dati:")
    print(df.head(10))
    
    # Crea anche un Excel con formattazione
    try:
        output_excel = base_path / 'turni_estratti.xlsx'
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Turni', index=False)
            
            # Crea anche un foglio di riepilogo
            summary = df.groupby('settimana').size().reset_index(name='n_turni')
            summary.to_excel(writer, sheet_name='Riepilogo', index=False)
        
        print(f"✓ Excel salvato in: {output_excel}")
    except Exception as e:
        print(f"Nota: Non è stato possibile creare l'Excel: {e}")
    
    print("\n" + "="*60)
    print("Estrazione completata!")

if __name__ == '__main__':
    main()

