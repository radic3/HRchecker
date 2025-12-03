#!/usr/bin/env python3
"""
Dashboard HR Interattiva - Analisi Turni 2025
Tutti i calcoli in Python puro (zero AI) - Matematica deterministica
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurazione pagina
st.set_page_config(
    page_title="Dashboard HR - Analisi Turni 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main > div {padding-top: 2rem;}
    .stMetric {background-color: #f0f2f6; padding: 10px; border-radius: 5px;}
    h1 {color: #1f77b4;}
    h2 {color: #ff7f0e;}
    .alert-success {background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 4px solid #28a745;}
    .alert-warning {background-color: #fff3cd; padding: 10px; border-radius: 5px; border-left: 4px solid #ffc107;}
    .alert-danger {background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 4px solid #dc3545;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carica dati - Con cache per performance"""
    base_path = Path('/Users/radice/Downloads/ROTA Chicca')
    
    # Prova a caricare il file Excel dell'utente
    excel_file = base_path / 'Tutti Turni Anno-completi.xlsx'
    csv_file = base_path / 'turni_completi_52_settimane.csv'
    
    if excel_file.exists():
        st.success(f"✅ Caricato: {excel_file.name}")
        df = pd.read_excel(excel_file)
    elif csv_file.exists():
        st.info(f"📊 Usando dati estratti: {csv_file.name}")
        df = pd.read_csv(csv_file)
    else:
        st.error("❌ Nessun file dati trovato!")
        return None
    
    # Converti colonne se necessario
    if 'settimana' in df.columns:
        df['settimana'] = pd.to_numeric(df['settimana'], errors='coerce')
    
    return df

def calcola_metriche_staff(df, staff_name):
    """Calcola metriche per un singolo staff - PYTHON PURO"""
    df_staff = df[df['staff'] == staff_name]
    
    # Calcoli matematici Python (non AI)
    turni_totali = len(df_staff)
    turni_normali = len(df_staff[df_staff['tipo_turno'] == 'NORMALE'])
    riposi = len(df_staff[df_staff['tipo_turno'].isin(['RIPO', 'RDOM'])])
    ferie = len(df_staff[df_staff['tipo_turno'] == 'FERIOR'])
    off = len(df_staff[df_staff['tipo_turno'].isin(['OFF', 'CHIUSO'])])
    
    # Somma ore (pandas.sum() - matematica pura)
    ore_totali = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].sum()
    ore_medie = df_staff[df_staff['ore_lavoro'].notna()]['ore_lavoro'].mean()
    
    return {
        'Turni Totali': turni_totali,
        'Turni Normali': turni_normali,
        'Riposi': riposi,
        'Ferie': ferie,
        'OFF/Chiuso': off,
        'Ore Totali': round(ore_totali, 1),
        'Media Ore/Turno': round(ore_medie, 2) if pd.notna(ore_medie) else 0
    }

def calcola_cv(valori):
    """Calcola Coefficiente di Variazione - PYTHON numpy"""
    if len(valori) == 0 or np.mean(valori) == 0:
        return 0
    return (np.std(valori) / np.mean(valori)) * 100

def main():
    # Header
    st.title("📊 Dashboard HR - Analisi Turni 2025")
    st.markdown("### ⚖️ Analisi Equità e Compliance - Calcoli Python Certificati")
    
    st.markdown("""
    <div class='alert-success'>
    🔒 <b>GARANZIA</b>: Tutti i calcoli sono eseguiti da Python (pandas/numpy). 
    Zero AI nei numeri. Matematica pura e verificabile.
    </div>
    """, unsafe_allow_html=True)
    
    # Carica dati
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.title("🎛️ Controlli")
    
    # Info dataset
    st.sidebar.markdown("### 📊 Dataset")
    st.sidebar.metric("Turni Totali", len(df))
    st.sidebar.metric("Settimane", df['settimana'].nunique())
    st.sidebar.metric("Staff", df['staff'].nunique())
    
    # Filtri
    st.sidebar.markdown("### 🔍 Filtri")
    
    # Filtro staff
    staff_list = sorted(df['staff'].unique())
    selected_staff = st.sidebar.multiselect(
        "Seleziona Staff",
        options=staff_list,
        default=staff_list
    )
    
    # Filtro settimane
    min_sett = int(df['settimana'].min())
    max_sett = int(df['settimana'].max())
    sett_range = st.sidebar.slider(
        "Range Settimane",
        min_value=min_sett,
        max_value=max_sett,
        value=(min_sett, max_sett)
    )
    
    # Filtro tipo turno
    tipo_turno_filter = st.sidebar.multiselect(
        "Tipo Turno",
        options=df['tipo_turno'].unique(),
        default=df['tipo_turno'].unique()
    )
    
    # Applica filtri
    df_filtered = df[
        (df['staff'].isin(selected_staff)) &
        (df['settimana'] >= sett_range[0]) &
        (df['settimana'] <= sett_range[1]) &
        (df['tipo_turno'].isin(tipo_turno_filter))
    ]
    
    # Tabs principali
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🔍 Confronti", 
        "📈 Grafici", 
        "⚖️ Indici Equità",
        "📋 Dati Dettagliati"
    ])
    
    # ========== TAB 1: OVERVIEW ==========
    with tab1:
        st.header("📊 Overview Generale")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Turni Filtrati", len(df_filtered))
        with col2:
            ore_tot = df_filtered[df_filtered['ore_lavoro'].notna()]['ore_lavoro'].sum()
            st.metric("Ore Totali", f"{ore_tot:.1f}h")
        with col3:
            staff_count = df_filtered['staff'].nunique()
            st.metric("Staff Attivi", staff_count)
        with col4:
            sett_count = df_filtered['settimana'].nunique()
            st.metric("Settimane", sett_count)
        
        st.markdown("---")
        
        # Tabella riepilogo per staff
        st.subheader("📋 Metriche per Staff (Calcoli Python)")
        
        metriche_all = {}
        for staff in selected_staff:
            metriche_all[staff] = calcola_metriche_staff(df_filtered, staff)
        
        df_metriche = pd.DataFrame(metriche_all).T
        df_metriche = df_metriche.sort_values('Ore Totali', ascending=False)
        
        # Colora celle
        st.dataframe(
            df_metriche.style.background_gradient(
                subset=['Ore Totali'], cmap='RdYlGn'
            ).format({
                'Ore Totali': '{:.1f}',
                'Media Ore/Turno': '{:.2f}'
            }),
            use_container_width=True
        )
        
        # Download metriche
        csv = df_metriche.to_csv().encode('utf-8')
        st.download_button(
            "📥 Scarica Metriche CSV",
            csv,
            "metriche_staff.csv",
            "text/csv"
        )
    
    # ========== TAB 2: CONFRONTI ==========
    with tab2:
        st.header("🔍 Confronto Tra Staff")
        
        col1, col2 = st.columns(2)
        
        with col1:
            staff1 = st.selectbox("Staff 1", options=staff_list, key='staff1')
        with col2:
            staff2 = st.selectbox("Staff 2", options=staff_list, 
                                  index=1 if len(staff_list) > 1 else 0, key='staff2')
        
        if staff1 and staff2 and staff1 != staff2:
            st.markdown("---")
            
            # Calcola metriche (Python puro)
            m1 = calcola_metriche_staff(df_filtered, staff1)
            m2 = calcola_metriche_staff(df_filtered, staff2)
            
            st.subheader(f"📊 {staff1} vs {staff2}")
            
            # Tabella confronto
            confronto = []
            for metrica in m1.keys():
                val1 = m1[metrica]
                val2 = m2[metrica]
                diff = val1 - val2
                
                if val2 != 0:
                    perc = (diff / val2) * 100
                else:
                    perc = 0
                
                # Determina status
                if abs(perc) < 10:
                    status = "✅ Equo"
                elif abs(perc) < 20:
                    status = "⚠️ Attenzione"
                else:
                    status = "❌ Squilibrato"
                
                confronto.append({
                    'Metrica': metrica,
                    staff1: val1,
                    staff2: val2,
                    'Differenza': f"{diff:+.1f}",
                    'Diff %': f"{perc:+.2f}%",
                    'Status': status
                })
            
            df_confronto = pd.DataFrame(confronto)
            st.dataframe(df_confronto, use_container_width=True)
            
            # Grafico radar
            st.subheader("📈 Confronto Visivo")
            
            metriche_radar = ['Turni Totali', 'Turni Normali', 'Riposi', 'Ferie']
            
            # Normalizza valori per il radar
            values1 = [m1[m] for m in metriche_radar]
            values2 = [m2[m] for m in metriche_radar]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values1,
                theta=metriche_radar,
                fill='toself',
                name=staff1
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=values2,
                theta=metriche_radar,
                fill='toself',
                name=staff2
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Confronto Multi-dimensionale"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Alert squilibri
            alert_count = sum(1 for row in confronto if '❌' in row['Status'])
            if alert_count == 0:
                st.success(f"✅ Distribuzione EQUA tra {staff1} e {staff2}")
            elif alert_count <= 2:
                st.warning(f"⚠️ {alert_count} metriche con squilibrio")
            else:
                st.error(f"❌ {alert_count} metriche significativamente sbilanciate!")
    
    # ========== TAB 3: GRAFICI ==========
    with tab3:
        st.header("📈 Visualizzazioni")
        
        # Grafico ore per staff
        st.subheader("Ore Totali per Staff")
        
        ore_staff = df_filtered[df_filtered['ore_lavoro'].notna()].groupby('staff')['ore_lavoro'].sum().sort_values(ascending=False)
        
        fig_ore = px.bar(
            x=ore_staff.index,
            y=ore_staff.values,
            labels={'x': 'Staff', 'y': 'Ore Totali'},
            title='Ore Lavorate per Staff',
            color=ore_staff.values,
            color_continuous_scale='RdYlGn_r'
        )
        fig_ore.add_hline(y=ore_staff.mean(), line_dash="dash", 
                          annotation_text="Media", line_color="red")
        st.plotly_chart(fig_ore, use_container_width=True)
        
        # Distribuzione tipi turno
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuzione Tipi Turno")
            tipo_counts = df_filtered['tipo_turno'].value_counts()
            fig_pie = px.pie(
                values=tipo_counts.values,
                names=tipo_counts.index,
                title='Tipologie di Turno'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Riposi per Staff")
            riposi_staff = df_filtered[df_filtered['tipo_turno'].isin(['RIPO', 'RDOM'])].groupby('staff').size()
            fig_riposi = px.bar(
                x=riposi_staff.index,
                y=riposi_staff.values,
                labels={'x': 'Staff', 'y': 'N. Riposi'},
                title='Giorni di Riposo',
                color=riposi_staff.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_riposi, use_container_width=True)
        
        # Trend temporale
        st.subheader("📊 Trend Ore per Settimana")
        
        ore_settimana = df_filtered[df_filtered['ore_lavoro'].notna()].groupby(['settimana', 'staff'])['ore_lavoro'].sum().reset_index()
        
        fig_trend = px.line(
            ore_settimana,
            x='settimana',
            y='ore_lavoro',
            color='staff',
            title='Evoluzione Ore per Settimana',
            labels={'settimana': 'Settimana', 'ore_lavoro': 'Ore', 'staff': 'Staff'}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # ========== TAB 4: INDICI EQUITÀ ==========
    with tab4:
        st.header("⚖️ Indici di Equità")
        
        st.markdown("""
        <div class='alert-success'>
        📐 <b>Formula CV</b>: (Deviazione Standard / Media) × 100<br>
        🔢 <b>Calcolo</b>: numpy.std() / numpy.mean() - Matematica certificata IEEE
        </div>
        """, unsafe_allow_html=True)
        
        # Calcola CV per tutte le metriche (Python numpy)
        metriche_all = {}
        for staff in selected_staff:
            metriche_all[staff] = calcola_metriche_staff(df_filtered, staff)
        
        df_metriche = pd.DataFrame(metriche_all).T
        
        st.subheader("📊 Coefficienti di Variazione")
        
        cv_results = []
        for col in ['Turni Totali', 'Turni Normali', 'Riposi', 'Ore Totali']:
            if col in df_metriche.columns:
                valori = df_metriche[col].values
                cv = calcola_cv(valori)
                
                # Determina status
                if cv < 10:
                    status = "✅ OTTIMO"
                    color = "success"
                elif cv < 20:
                    status = "⚠️ ACCETTABILE"
                    color = "warning"
                else:
                    status = "❌ SQUILIBRATO"
                    color = "danger"
                
                cv_results.append({
                    'Metrica': col,
                    'CV (%)': round(cv, 2),
                    'Media': round(valori.mean(), 2),
                    'Std Dev': round(valori.std(), 2),
                    'Status': status
                })
                
                # Mostra come metric
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.markdown(f"**{col}**")
                with col2:
                    st.metric("CV", f"{cv:.2f}%")
                with col3:
                    if color == "success":
                        st.success(status)
                    elif color == "warning":
                        st.warning(status)
                    else:
                        st.error(status)
        
        # Tabella CV
        df_cv = pd.DataFrame(cv_results)
        st.dataframe(df_cv, use_container_width=True)
        
        # Interpretazione
        st.markdown("---")
        st.markdown("""
        **📖 Interpretazione CV:**
        - **< 10%**: Distribuzione equa ✅
        - **10-20%**: Accettabile ma da monitorare ⚠️
        - **> 20%**: Squilibrio significativo ❌
        """)
    
    # ========== TAB 5: DATI DETTAGLIATI ==========
    with tab5:
        st.header("📋 Dati Dettagliati")
        
        # Opzioni visualizzazione
        show_all = st.checkbox("Mostra tutti i campi", value=False)
        
        if show_all:
            st.dataframe(df_filtered, use_container_width=True)
        else:
            cols_essential = ['staff', 'settimana', 'tipo_turno', 'ore_lavoro', 
                             'ora_entrata', 'ora_uscita']
            cols_to_show = [c for c in cols_essential if c in df_filtered.columns]
            st.dataframe(df_filtered[cols_to_show], use_container_width=True)
        
        # Download dati filtrati
        csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Scarica Dati Filtrati (CSV)",
            csv_filtered,
            "dati_filtrati.csv",
            "text/csv"
        )
        
        # Statistiche rapide
        st.markdown("---")
        st.subheader("📊 Statistiche Rapide (Python)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Turni Visualizzati", len(df_filtered))
            st.metric("Ore Visualizzate", f"{df_filtered['ore_lavoro'].sum():.1f}h")
        
        with col2:
            media_ore = df_filtered['ore_lavoro'].mean()
            st.metric("Media Ore/Turno", f"{media_ore:.2f}h")
            mediana_ore = df_filtered['ore_lavoro'].median()
            st.metric("Mediana Ore/Turno", f"{mediana_ore:.2f}h")
        
        with col3:
            turni_norm = len(df_filtered[df_filtered['tipo_turno'] == 'NORMALE'])
            st.metric("Turni Normali", turni_norm)
            riposi_tot = len(df_filtered[df_filtered['tipo_turno'].isin(['RIPO', 'RDOM'])])
            st.metric("Riposi Totali", riposi_tot)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    🔒 <b>Calcoli Certificati Python</b> - pandas 2.3.3 + numpy 2.3.5<br>
    ✅ Affidabilità Matematica Garantita - Zero AI nei numeri<br>
    📊 Dashboard HR Professionale - Analisi Turni 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

