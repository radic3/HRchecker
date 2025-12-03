#!/usr/bin/env python3
"""
Script per censurare i nomi dello staff (prime 3 lettere)
"""

import pandas as pd
from pathlib import Path

def censura_nomi(nome):
    """Prendi solo prime 3 lettere del nome"""
    if pd.isna(nome):
        return nome
    return str(nome)[:3].upper()

def main():
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    
    print("🔒 CENSURA NOMI STAFF")
    print("=" * 60)
    
    # Carica dati
    df = pd.read_csv(base_path / 'dati_arricchiti.csv')
    
    print(f"\n📊 Dati caricati: {len(df)} righe")
    print(f"\n👥 Staff originali:")
    staff_originali = df['staff'].dropna().unique()
    for staff in sorted(staff_originali):
        print(f"   • {staff}")
    
    # Censura nomi
    df['staff'] = df['staff'].apply(censura_nomi)
    
    print(f"\n🔒 Staff censurati (prime 3 lettere):")
    staff_censurati = df['staff'].dropna().unique()
    for staff in sorted(staff_censurati):
        print(f"   • {staff}")
    
    # Salva file censurato
    output_file = base_path / 'dati_arricchiti_censurati.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ File salvato: {output_file.name}")
    print(f"   {len(df)} righe processate")
    
    # Crea anche versione per web
    output_web = base_path / 'dati_web.csv'
    df.to_csv(output_web, index=False)
    print(f"✅ File web salvato: {output_web.name}")
    
    # Statistiche
    print(f"\n📈 Statistiche censura:")
    print(f"   Staff unici: {len(staff_censurati)}")
    print(f"   Mapping:")
    
    # Ricrea mapping per info
    mappings = {
        'VISSANI': 'VIS',
        'PAGANO': 'PAG',
        'PACINI': 'PAC',
        'TAMBERI': 'TAM',
        'CIRCELLI': 'CIR',
        'MORALE': 'MOR'
    }
    
    for orig, cens in mappings.items():
        count = len(df[df['staff'] == cens])
        if count > 0:
            print(f"      {orig} → {cens} ({count} turni)")
    
    print("\n🔒 Privacy protetta!")

if __name__ == '__main__':
    main()

