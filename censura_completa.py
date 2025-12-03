#!/usr/bin/env python3
"""
Script per censurare TUTTI i nomi (anche in linea_completa)
"""

import pandas as pd
from pathlib import Path

def censura_completa(testo):
    """Sostituisce tutti i cognomi con 3 lettere in qualsiasi testo"""
    if pd.isna(testo):
        return testo
    
    testo = str(testo)
    
    # Mapping cognomi → censurati
    mappings = {
        'VISSANI': 'VIS',
        'PAGANO': 'PAG',
        'PACINI': 'PAC',
        'TAMBERI': 'TAM',
        'CIRCELLI': 'CIR',
        'MORALE': 'MOR'
    }
    
    # Sostituisci tutti i cognomi
    for cognome, censurato in mappings.items():
        testo = testo.replace(cognome, censurato)
    
    return testo

def main():
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    
    print("🔒 CENSURA COMPLETA - TUTTI I NOMI")
    print("=" * 70)
    
    # File da processare
    files = ['dati_web.csv', 'dati_arricchiti_censurati.csv']
    
    for filename in files:
        filepath = base_path / filename
        
        if not filepath.exists():
            print(f"\n⚠️  File non trovato: {filename}")
            continue
        
        print(f"\n📄 Processando: {filename}")
        
        # Carica CSV
        df = pd.read_csv(filepath)
        
        print(f"   Righe: {len(df)}")
        print(f"   Colonne: {len(df.columns)}")
        
        # Censura tutte le colonne di testo
        for col in df.columns:
            if df[col].dtype == 'object':  # Colonne di testo
                print(f"   🔒 Censurando colonna: {col}")
                df[col] = df[col].apply(censura_completa)
        
        # Salva file censurato
        df.to_csv(filepath, index=False)
        print(f"   ✅ Salvato: {filename}")
    
    print("\n" + "=" * 70)
    print("✅ CENSURA COMPLETA TERMINATA")
    print("=" * 70)
    
    # Verifica
    print("\n🔍 VERIFICA FINALE:")
    df_test = pd.read_csv(base_path / 'dati_web.csv')
    
    # Controlla se ci sono ancora cognomi completi
    test_text = ' '.join(df_test.astype(str).values.flatten())
    
    cognomi = ['VISSANI', 'PAGANO', 'PACINI', 'TAMBERI', 'CIRCELLI', 'MORALE']
    found = []
    
    for cognome in cognomi:
        if cognome in test_text:
            found.append(cognome)
    
    if found:
        print(f"   ❌ ATTENZIONE: Trovati ancora: {', '.join(found)}")
    else:
        print(f"   ✅ PERFETTO: Nessun cognome completo trovato!")
        print(f"   ✅ Solo 3 lettere: VIS, PAG, PAC, TAM, CIR, MOR")

if __name__ == '__main__':
    main()

