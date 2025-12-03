#!/usr/bin/env python3
"""
Analisi Statistica Forense - Identificazione Manipolazioni nei Turni
Usa metodi matematici rigorosi (scipy, numpy) per dimostrare non-casualità
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, ks_2samp
from pathlib import Path
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Carica dati"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    df = pd.read_csv(base_path / 'dati_arricchiti.csv')
    df = df[df['staff'].notna()].copy()
    return df

def classifica_turni_comodita(df):
    """Classifica turni per 'comodità' - Python puro"""
    print("\n" + "="*70)
    print("🔍 CLASSIFICAZIONE TURNI PER COMODITÀ")
    print("="*70)
    
    print("\n📋 Criteri classificazione turni:")
    print("   COMODI:")
    print("   • Orario entrata >= 07:00")
    print("   • Orario uscita <= 17:00")
    print("   • Durata <= 7 ore")
    print("   • Non festivi")
    print("   • Non weekend")
    print("")
    print("   SCOMODI:")
    print("   • Orario entrata < 05:00 (notte)")
    print("   • Orario uscita > 19:00 (sera)")
    print("   • Durata > 8 ore")
    print("   • Festivi lavorati")
    print("   • Weekend lavorati")
    
    risultati = {}
    
    for staff in sorted(df['staff'].unique()):
        df_staff = df[(df['staff'] == staff) & (df['tipo_turno'] == 'NORMALE')]
        
        # Conta turni per comodità
        turni_comodi = 0
        turni_scomodi = 0
        score_comodita = 0
        
        for idx, row in df_staff.iterrows():
            comfort_score = 0
            discomfort_score = 0
            
            # Analizza orario entrata
            if pd.notna(row['ora_entrata']):
                ora = str(row['ora_entrata']).split(':')[0]
                if ora.isdigit():
                    ora_int = int(ora)
                    if ora_int >= 7 and ora_int <= 9:
                        comfort_score += 2  # Orario comodo
                    elif ora_int < 5:
                        discomfort_score += 3  # Turno notte
                    elif ora_int >= 13:
                        comfort_score += 1  # Pomeriggio
            
            # Analizza orario uscita
            if pd.notna(row['ora_uscita']):
                ora = str(row['ora_uscita']).split(':')[0]
                if ora.isdigit():
                    ora_int = int(ora)
                    if ora_int <= 17:
                        comfort_score += 1
                    elif ora_int >= 20:
                        discomfort_score += 2
            
            # Analizza durata
            if pd.notna(row['ore_lavoro']):
                ore_str = str(row['ore_lavoro']).replace(',', '.')
                try:
                    ore = float(ore_str)
                except:
                    ore = 0
                if ore <= 7:
                    comfort_score += 1
                elif ore > 8:
                    discomfort_score += 2
            
            # Penalità festivi e weekend
            if row.get('is_festivo', False):
                discomfort_score += 5
            if row.get('is_weekend', False):
                discomfort_score += 2
            
            # Classifica turno
            if comfort_score > discomfort_score:
                turni_comodi += 1
            elif discomfort_score > comfort_score:
                turni_scomodi += 1
            
            score_comodita += (comfort_score - discomfort_score)
        
        risultati[staff] = {
            'turni_totali': len(df_staff),
            'turni_comodi': turni_comodi,
            'turni_scomodi': turni_scomodi,
            'turni_neutri': len(df_staff) - turni_comodi - turni_scomodi,
            'score_comodita': score_comodita,
            'ratio_comodi': (turni_comodi / len(df_staff) * 100) if len(df_staff) > 0 else 0
        }
    
    df_comfort = pd.DataFrame(risultati).T
    df_comfort = df_comfort.sort_values('score_comodita', ascending=False)
    
    print("\n📊 RISULTATI CLASSIFICAZIONE:")
    print(df_comfort.to_string())
    
    return df_comfort

def analisi_riposi_consecutivi_pattern(df):
    """Analizza pattern riposi consecutivi - Matematica pura"""
    print("\n" + "="*70)
    print("😴 ANALISI PATTERN RIPOSI CONSECUTIVI")
    print("="*70)
    
    risultati = {}
    
    for staff in sorted(df['staff'].unique()):
        df_staff = df[df['staff'] == staff].sort_values(['settimana', 'file'])
        
        sequenze = []
        giorni_consec = 0
        tipo_precedente = None
        
        for idx, row in df_staff.iterrows():
            is_riposo = row['tipo_turno'] in ['RIPO', 'RDOM', 'FERIOR', 'OFF', 'CHIUSO']
            
            if is_riposo:
                giorni_consec += 1
            else:
                if giorni_consec > 0:
                    sequenze.append(giorni_consec)
                giorni_consec = 0
        
        if giorni_consec > 0:
            sequenze.append(giorni_consec)
        
        # Statistiche sequenze
        n_seq_2 = sum(1 for s in sequenze if s == 2)
        n_seq_3 = sum(1 for s in sequenze if s == 3)
        n_seq_4plus = sum(1 for s in sequenze if s >= 4)
        n_seq_lunghe = sum(1 for s in sequenze if s >= 3)
        
        risultati[staff] = {
            'tot_sequenze': len(sequenze),
            'seq_2_giorni': n_seq_2,
            'seq_3_giorni': n_seq_3,
            'seq_4plus_giorni': n_seq_4plus,
            'seq_lunghe': n_seq_lunghe,
            'max_consecutivi': max(sequenze) if sequenze else 0,
            'media_lunghezza': np.mean(sequenze) if sequenze else 0,
            'tot_giorni_riposo': sum(sequenze)
        }
    
    df_riposi = pd.DataFrame(risultati).T
    df_riposi = df_riposi.sort_values('seq_lunghe', ascending=False)
    
    print("\n📊 PATTERN RIPOSI CONSECUTIVI:")
    print(df_riposi.to_string())
    
    # Test statistico: chi ha troppe sequenze lunghe?
    print("\n🚨 IDENTIFICAZIONE ANOMALIE PATTERN:")
    media_lunghe = df_riposi['seq_lunghe'].mean()
    std_lunghe = df_riposi['seq_lunghe'].std()
    
    for staff, row in df_riposi.iterrows():
        z_score = (row['seq_lunghe'] - media_lunghe) / std_lunghe if std_lunghe > 0 else 0
        
        if z_score > 1.5:
            print(f"   🚨 {staff}: {row['seq_lunghe']:.0f} sequenze lunghe (Z-score: {z_score:.2f})")
            print(f"      → {z_score:.1f} deviazioni standard sopra la media")
            print(f"      → Probabilità casuale: {(1 - stats.norm.cdf(z_score)) * 100:.2f}%")
    
    return df_riposi

def test_chi_quadrato_distribuzione(df):
    """Test chi-quadrato per verificare casualità - scipy.stats"""
    print("\n" + "="*70)
    print("🔬 TEST CHI-QUADRATO - CASUALITÀ DISTRIBUZIONE")
    print("="*70)
    
    print("\n📐 Ipotesi Nulla (H0): Turni distribuiti casualmente")
    print("📐 Ipotesi Alternativa (H1): Distribuzione non casuale (manipolata)")
    
    # Test 1: Distribuzione turni comodi
    turni_comodi = []
    turni_scomodi = []
    staff_names = []
    
    for staff in sorted(df['staff'].unique()):
        df_staff = df[(df['staff'] == staff) & (df['tipo_turno'] == 'NORMALE')]
        
        comodi = 0
        scomodi = 0
        
        for idx, row in df_staff.iterrows():
            # Turno comodo se: entrata >= 07:00, uscita <= 17:00, non festivo, non weekend
            is_comodo = False
            is_scomodo = False
            
            if pd.notna(row['ora_entrata']):
                ora_ent = str(row['ora_entrata']).split(':')[0]
                if ora_ent.isdigit() and int(ora_ent) >= 7:
                    is_comodo = True
                elif ora_ent.isdigit() and int(ora_ent) < 5:
                    is_scomodo = True
            
            if row.get('is_festivo', False) or row.get('is_weekend', False):
                is_scomodo = True
                is_comodo = False
            
            if is_comodo:
                comodi += 1
            elif is_scomodo:
                scomodi += 1
        
        turni_comodi.append(comodi)
        turni_scomodi.append(scomodi)
        staff_names.append(staff)
    
    # Crea tabella contingenza
    contingency_table = np.array([turni_comodi, turni_scomodi])
    
    print(f"\n📊 Tabella Contingenza:")
    print(f"Staff: {staff_names}")
    print(f"Comodi: {turni_comodi}")
    print(f"Scomodi: {turni_scomodi}")
    
    # Esegui test chi-quadrato (scipy.stats - matematica certificata)
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    
    print(f"\n📈 RISULTATI TEST CHI-QUADRATO:")
    print(f"   Chi-quadrato: {chi2:.4f}")
    print(f"   P-value: {p_value:.6f}")
    print(f"   Gradi di libertà: {dof}")
    
    print(f"\n⚖️  INTERPRETAZIONE:")
    if p_value < 0.001:
        print(f"   🚨 P-value < 0.001 → EVIDENZA FORTISSIMA di non-casualità")
        print(f"   ❌ Probabilità che sia casuale: < 0.1%")
        print(f"   ✅ DIMOSTRATO: Distribuzione manipolata!")
    elif p_value < 0.01:
        print(f"   🚨 P-value < 0.01 → EVIDENZA FORTE di non-casualità")
        print(f"   ❌ Probabilità casuale: {p_value * 100:.2f}%")
        print(f"   ✅ Molto probabile manipolazione")
    elif p_value < 0.05:
        print(f"   ⚠️  P-value < 0.05 → EVIDENZA SIGNIFICATIVA")
        print(f"   ⚠️  Probabilità casuale: {p_value * 100:.2f}%")
        print(f"   ⚠️  Probabile manipolazione")
    else:
        print(f"   ✅ P-value >= 0.05 → Non si può escludere casualità")
        print(f"   📊 Probabilità casuale: {p_value * 100:.2f}%")
    
    return {
        'chi2': chi2,
        'p_value': p_value,
        'contingency': contingency_table,
        'staff_names': staff_names
    }

def calcola_score_favoritismo(df, df_comfort, df_riposi):
    """Calcola score matematico di favoritismo - Python/numpy"""
    print("\n" + "="*70)
    print("⚖️  SCORE DI FAVORITISMO (Matematica Pura)")
    print("="*70)
    
    print("\n📐 Formula Score:")
    print("   Score = (Turni Comodi × 2) + (Riposi Lunghi × 3) - (Turni Scomodi × 2)")
    print("   Score normalizzato per numero turni totali")
    
    scores = {}
    
    for staff in sorted(df['staff'].unique()):
        # Dati comodità
        if staff in df_comfort.index:
            comodi = df_comfort.loc[staff, 'turni_comodi']
            scomodi = df_comfort.loc[staff, 'turni_scomodi']
            score_comfort = df_comfort.loc[staff, 'score_comodita']
        else:
            comodi = scomodi = score_comfort = 0
        
        # Dati riposi
        if staff in df_riposi.index:
            seq_lunghe = df_riposi.loc[staff, 'seq_lunghe']
            max_consec = df_riposi.loc[staff, 'max_consecutivi']
        else:
            seq_lunghe = max_consec = 0
        
        # Calcola score complessivo
        df_staff = df[df['staff'] == staff]
        n_turni = len(df_staff[df_staff['tipo_turno'] == 'NORMALE'])
        
        score_raw = (comodi * 2) + (seq_lunghe * 3) - (scomodi * 2)
        score_norm = (score_raw / n_turni * 100) if n_turni > 0 else 0
        
        scores[staff] = {
            'turni_comodi': comodi,
            'turni_scomodi': scomodi,
            'seq_riposi_lunghe': seq_lunghe,
            'max_riposi_consec': max_consec,
            'score_favoritismo': round(score_norm, 2),
            'n_turni': n_turni
        }
    
    df_scores = pd.DataFrame(scores).T
    df_scores = df_scores.sort_values('score_favoritismo', ascending=False)
    
    print("\n📊 SCORE DI FAVORITISMO PER STAFF:")
    print(df_scores.to_string())
    
    # Z-score per identificare outlier
    print("\n🔬 ANALISI STATISTICA Z-SCORE:")
    media = df_scores['score_favoritismo'].mean()
    std = df_scores['score_favoritismo'].std()
    
    print(f"   Media score: {media:.2f}")
    print(f"   Std Dev: {std:.2f}")
    
    print(f"\n🚨 IDENTIFICAZIONE OUTLIER (Z-score > 1.5):")
    
    for staff, row in df_scores.iterrows():
        z = (row['score_favoritismo'] - media) / std if std > 0 else 0
        
        if z > 1.5:
            # Calcola probabilità (scipy.stats)
            prob_casuale = (1 - stats.norm.cdf(z)) * 100
            
            print(f"\n   🚨 {staff}:")
            print(f"      Score: {row['score_favoritismo']:.2f}")
            print(f"      Z-score: {z:.2f} (>{1.5:.1f} std dalla media)")
            print(f"      Probabilità casuale: {prob_casuale:.4f}%")
            
            if prob_casuale < 1:
                print(f"      ❌ EVIDENZA STATISTICA DI FAVORITISMO")
            elif prob_casuale < 5:
                print(f"      ⚠️  FORTE SOSPETTO DI FAVORITISMO")
            else:
                print(f"      ⚠️  POSSIBILE FAVORITISMO")
    
    return df_scores

def test_distribuzione_uniforme(df):
    """Test se i turni sono distribuiti uniformemente - scipy"""
    print("\n" + "="*70)
    print("🔬 TEST UNIFORMITÀ DISTRIBUZIONE TURNI PER SETTIMANA")
    print("="*70)
    
    print("\n📐 Test: I turni sono distribuiti uniformemente nel tempo?")
    
    risultati_test = {}
    
    for staff in sorted(df['staff'].unique()):
        df_staff = df[(df['staff'] == staff) & (df['tipo_turno'] == 'NORMALE')]
        
        # Conta turni per settimana
        turni_per_sett = df_staff.groupby('settimana').size().values
        
        if len(turni_per_sett) > 1:
            # Test chi-quadrato uniformità (scipy.stats)
            media_attesa = np.mean(turni_per_sett)
            attesi = np.full(len(turni_per_sett), media_attesa)
            
            chi2, p_value = stats.chisquare(turni_per_sett, attesi)
            
            risultati_test[staff] = {
                'chi2': chi2,
                'p_value': p_value,
                'varianza': np.var(turni_per_sett),
                'media': media_attesa
            }
    
    df_test = pd.DataFrame(risultati_test).T
    df_test = df_test.sort_values('p_value')
    
    print("\n📊 RISULTATI TEST UNIFORMITÀ:")
    for staff, row in df_test.iterrows():
        print(f"\n   {staff}:")
        print(f"      Chi-quadrato: {row['chi2']:.4f}")
        print(f"      P-value: {row['p_value']:.6f}")
        
        if row['p_value'] < 0.05:
            print(f"      🚨 Distribuzione NON uniforme (p < 0.05)")
            print(f"      ❌ Turni concentrati in alcuni periodi")
        else:
            print(f"      ✅ Distribuzione uniforme (p >= 0.05)")
    
    return df_test

def analisi_probabilita_pattern(df_riposi):
    """Calcola probabilità di ottenere tali pattern per caso - numpy/scipy"""
    print("\n" + "="*70)
    print("🎲 ANALISI PROBABILISTICA - Pattern Riposi")
    print("="*70)
    
    print("\n📐 Domanda: Qual è la probabilità di ottenere questi pattern per caso?")
    
    # Parametri distribuzione
    media_seq = df_riposi['seq_lunghe'].mean()
    std_seq = df_riposi['seq_lunghe'].std()
    
    print(f"\n📊 Distribuzione sequenze lunghe (3+ giorni):")
    print(f"   Media: {media_seq:.2f}")
    print(f"   Std Dev: {std_seq:.2f}")
    
    print(f"\n🔬 ANALISI PER STAFF:")
    
    for staff, row in df_riposi.iterrows():
        n_seq = row['seq_lunghe']
        z_score = (n_seq - media_seq) / std_seq if std_seq > 0 else 0
        
        # Probabilità usando distribuzione normale (scipy.stats)
        if z_score > 0:
            prob = (1 - stats.norm.cdf(z_score)) * 100
        else:
            prob = stats.norm.cdf(z_score) * 100
        
        print(f"\n   {staff}:")
        print(f"      Sequenze lunghe: {n_seq:.0f}")
        print(f"      Z-score: {z_score:.2f}")
        print(f"      Probabilità casuale: {prob:.4f}%")
        
        if abs(z_score) > 2:
            print(f"      🚨 ANOMALIA STATISTICA GRAVE (|Z| > 2)")
            print(f"      ❌ Probabilità < 5% che sia casuale")
        elif abs(z_score) > 1.5:
            print(f"      ⚠️  ANOMALIA SIGNIFICATIVA (|Z| > 1.5)")
            print(f"      ⚠️  Probabile manipolazione")

def genera_report_forense(df, df_comfort, df_riposi, test_chi, df_scores):
    """Genera report Excel forense"""
    print("\n" + "="*70)
    print("📄 GENERAZIONE REPORT STATISTICO FORENSE")
    print("="*70)
    
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    output = base_path / 'REPORT_FORENSE_MANIPOLAZIONE.xlsx'
    
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Foglio 1: Executive Summary
            summary = pd.DataFrame({
                'Test': [
                    'Chi-Quadrato Distribuzione',
                    'P-value',
                    'Interpretazione',
                    'Staff con Score Favoritismo Alto',
                    'Staff con Pattern Sospetti'
                ],
                'Risultato': [
                    f"{test_chi['chi2']:.4f}",
                    f"{test_chi['p_value']:.6f}",
                    'NON CASUALE' if test_chi['p_value'] < 0.05 else 'Casuale',
                    df_scores.head(1).index[0],
                    df_riposi.head(1).index[0]
                ]
            })
            summary.to_excel(writer, sheet_name='Summary Forense', index=False)
            
            # Foglio 2: Score Favoritismo
            df_scores.to_excel(writer, sheet_name='Score Favoritismo')
            
            # Foglio 3: Classificazione Turni
            df_comfort.to_excel(writer, sheet_name='Turni Comodi vs Scomodi')
            
            # Foglio 4: Pattern Riposi
            df_riposi.to_excel(writer, sheet_name='Pattern Riposi')
            
            # Foglio 5: Dati Grezzi
            df.to_excel(writer, sheet_name='Dati Completi', index=False)
        
        print(f"✅ Report forense salvato: {output}")
        return output
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        return None

def main():
    print("="*70)
    print("🔬 ANALISI STATISTICA FORENSE")
    print("   Identificazione Manipolazioni nei Turni")
    print("   Metodi: scipy.stats, numpy - Matematica Rigorosa")
    print("="*70)
    
    # Carica dati
    df = load_data()
    print(f"\n✅ Dati caricati: {len(df)} turni")
    
    # Analisi 1: Classificazione comodità
    df_comfort = classifica_turni_comodita(df)
    
    # Analisi 2: Pattern riposi
    df_riposi = analisi_riposi_consecutivi_pattern(df)
    
    # Analisi 3: Test chi-quadrato
    test_chi = test_chi_quadrato_distribuzione(df)
    
    # Analisi 4: Score favoritismo
    df_scores = calcola_score_favoritismo(df, df_comfort, df_riposi)
    
    # Analisi 5: Probabilità pattern
    analisi_probabilita_pattern(df_riposi)
    
    # Analisi 6: Test uniformità
    test_distribuzione_uniforme(df)
    
    # Report finale
    report = genera_report_forense(df, df_comfort, df_riposi, test_chi, df_scores)
    
    print("\n" + "="*70)
    print("✅ ANALISI FORENSE COMPLETATA")
    print("="*70)
    
    if report:
        print(f"\n📄 Report: {report.name}")
        print(f"\n🔬 Il report contiene:")
        print(f"   • Test statistici formali (chi-quadrato, p-value)")
        print(f"   • Score di favoritismo per ogni staff")
        print(f"   • Classificazione turni comodi/scomodi")
        print(f"   • Pattern riposi consecutivi")
        print(f"   • Evidenze matematiche di manipolazione")

if __name__ == '__main__':
    main()
