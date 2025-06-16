"""
Streamlit Web UI voor Bestellingen Analyse
Toont alle 18 visualisaties in een interactieve webinterface
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import warnings
import io
warnings.filterwarnings('ignore')

# Importeer alle visualisatie functies
from visualisaties import (
    gf1_top_producten_barplot,
    gf2_omzet_tijdlijn,
    gf3_geografische_spreiding,
    gf4_klanten_segmentatie_matrix,
    gf5_bestellingen_heatmap,
    gf6_product_categorie_donut,
    gf7_betaalmethode_analyse,
    gf8_kaas_brood_combinaties,
    gf9_verkooppatronen,
    gf10_prijsevolutie,
    gf11_toekomstvoorspelling,
    gf12_lange_termijn,
    gf13_seizoens_feestdagen,
    gf14_leadtime_analyse,
    gf15_product_combinaties,
    gf16_klant_lifetime_value,
    gf17_winstgevendheid,
    gf18_klanten_belonen
)

# Importeer code uitleg functies
from code_uitleg import get_code_uitleg, get_alle_analyses, get_algemeen_concept, ALGEMENE_CONCEPTEN

# Importeer grafiek uitleg functies
from grafiek_uitleg import get_grafiek_uitleg, get_alle_visualisaties

# Importeer basis data voor stats
from data_analyse import df_bestellingen, df_filtered

# Configuratie
st.set_page_config(
    page_title="Bestellingen Analyse Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS voor mooiere styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #1f77b4;
    }
    .stAlert {
        background-color: #e3f2fd;
        border: 1px solid #1976d2;
    }
</style>
""", unsafe_allow_html=True)

# Hoofdtitel
st.title("🧀 Delicatessenzaak Bestellingen Analyse Dashboard")
st.markdown("---")

# Sidebar voor navigatie
st.sidebar.title("📊 Navigatie")
st.sidebar.markdown("Kies een analyse categorie:")

# Definieer categorieën met hun visualisaties
categories = {
    "📈 Basis Analyses (DF1-DF4)": {
        "GF1: Top 20 Producten": gf1_top_producten_barplot,
        "GF2: Omzet Tijdlijn": gf2_omzet_tijdlijn,
        "GF3: Geografische Spreiding": gf3_geografische_spreiding,
        "GF4: Klanten Segmentatie": gf4_klanten_segmentatie_matrix
    },
    "🔥 Operationele Inzichten (DF5-DF8)": {
        "GF5: Bestellingen Heatmap": gf5_bestellingen_heatmap,
        "GF6: Product Categorieën": gf6_product_categorie_donut,
        "GF7: Betaalmethoden": gf7_betaalmethode_analyse,
        "GF8: Kaas + Brood Combinaties": gf8_kaas_brood_combinaties
    },
    "📊 Geavanceerde Analyses (DF9-DF12)": {
        "GF9: Verkooppatronen": gf9_verkooppatronen,
        "GF10: Prijsevolutie": gf10_prijsevolutie,
        "GF11: Toekomstvoorspelling": gf11_toekomstvoorspelling,
        "GF12: 55-jaar Voorspelling": gf12_lange_termijn
    },
    "🎯 Marketing & Strategie (DF13-DF15)": {
        "GF13: Seizoens & Feestdagen": gf13_seizoens_feestdagen,
        "GF14: Bestelpatronen": gf14_leadtime_analyse,
        "GF15: Cross-selling": gf15_product_combinaties
    },
    "💰 Klant & Winst Analyses (DF16-DF18)": {
        "GF16: Customer Lifetime Value": gf16_klant_lifetime_value,
        "GF17: Winstgevendheid": gf17_winstgevendheid,
        "GF18: Klanten Belonen": gf18_klanten_belonen
    },
    "💻 Code Uitleg & Documentatie": {
        "type": "code_uitleg"  # Speciale type voor code uitleg
    }
}

# Selecteer categorie
selected_category = st.sidebar.selectbox(
    "Selecteer een categorie:",
    list(categories.keys())
)

# Check of dit de code uitleg categorie is
if selected_category == "💻 Code Uitleg & Documentatie":
    # Toon code uitleg opties
    uitleg_opties = ["🔬 Wetenschappelijke Code Uitleg"] + list(ALGEMENE_CONCEPTEN.keys())
    selected_option = st.sidebar.radio(
        "Selecteer een optie:",
        uitleg_opties
    )
else:
    # Selecteer specifieke visualisatie
    selected_viz = st.sidebar.radio(
        "Selecteer een visualisatie:",
        list(categories[selected_category].keys())
    )

# Toon algemene statistieken in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Algemene Statistieken")

# Bereken stats
totale_omzet = df_bestellingen['totaal_bedrag'].sum()
aantal_bestellingen = len(df_bestellingen)
gemiddelde_bestelling = totale_omzet / aantal_bestellingen

# Toon stats
st.sidebar.metric("Totale Omzet", f"€{totale_omzet:,.2f}")
st.sidebar.metric("Aantal Bestellingen", f"{aantal_bestellingen:,}")
st.sidebar.metric("Gemiddelde Bestelling", f"€{gemiddelde_bestelling:,.2f}")

# Toon geselecteerde inhoud
if selected_category == "💻 Code Uitleg & Documentatie":
    # Toon code uitleg
    if selected_option == "🔬 Wetenschappelijke Code Uitleg":
        # Laat gebruiker een analyse selecteren
        st.markdown("### 🔬 Wetenschappelijke Code Documentatie")
        
        # Info box over de uitleg types met aangepaste styling
        st.markdown("""
        <div style='background-color: #4A0E4E; color: #F5F5F5; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid #81689D;'>
            <strong>💡 Kies je uitleg niveau:</strong><br>
            • <strong>Voor Iedereen</strong>: Gebalanceerde uitleg met context<br>
            • <strong>Wetenschappelijk</strong>: Volledig technisch met formules<br>
            • <strong>Basis</strong>: Simpele taal met voorbeelden
        </div>
        """, unsafe_allow_html=True)
        
        # Selecteer specifieke analyse
        analyses = get_alle_analyses()
        selected_analyse = st.selectbox(
            "Selecteer een analyse voor uitleg:",
            analyses
        )
        
        # Haal code en uitleg op
        uitleg_data = get_code_uitleg(selected_analyse)
        
        # Toon de analyse naam en bijbehorende grafiek
        st.markdown(f"## {selected_analyse}")
        st.info(f"**📊 {uitleg_data.get('grafiek', 'Grafiek informatie niet beschikbaar')}**")
        
        # Maak twee kolommen
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 💻 Code")
            st.code(uitleg_data['code'], language='python')
        
        with col2:
            st.markdown("### 📝 Uitleg")
            st.markdown(uitleg_data.get('uitleg', 'Uitleg niet beschikbaar'))
        
    else:
        # Toon algemeen concept
        st.markdown(f"### 📚 {selected_option}")
        
        concept_uitleg = get_algemeen_concept(selected_option)
        st.markdown(concept_uitleg)
else:
    # Toon normale visualisatie
    st.markdown(f"### {selected_viz}")
    
    # Maak twee kolommen voor knoppen
    col1, col2 = st.columns([1, 5])
    
    with col1:
        # Bonus knop voor grafiek uitleg
        if st.button("🎓 Grafiek Uitleg", key="uitleg_btn"):
            st.session_state.show_uitleg = not st.session_state.get('show_uitleg', False)
    
    # Toon grafiek uitleg als de knop is ingedrukt
    if st.session_state.get('show_uitleg', False):
        with st.expander("📊 Uitgebreide Grafiek Uitleg", expanded=True):
            uitleg = get_grafiek_uitleg(selected_viz)
            
            # Maak 4 secties voor de uitleg
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 👁️ Wat zie je?")
                st.markdown(uitleg.get('wat_zie_je', 'Geen uitleg beschikbaar'))
                
                st.markdown("### 📖 Hoe lees je dit?")
                st.markdown(uitleg.get('hoe_lezen', 'Geen uitleg beschikbaar'))
            
            with col2:
                st.markdown("### 💡 Wat betekent dit?")
                st.markdown(uitleg.get('betekenis', 'Geen uitleg beschikbaar'))
                
                st.markdown("### ✅ Conclusies & Acties")
                st.markdown(uitleg.get('conclusies', 'Geen uitleg beschikbaar'))
    
    # Toon de grafiek
    fig = categories[selected_category][selected_viz]()
    st.pyplot(fig)

    # Download knop voor de visualisatie
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)

    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        st.download_button(
            label="📥 Download Grafiek",
            data=buf,
            file_name=f"{selected_viz.lower().replace(' ', '_')}.png",
            mime="image/png"
        )
    
    with col2:
        # Knop om code uitleg te zien
        if st.button("💻 Zie Code", key="code_btn"):
            st.session_state.show_code = not st.session_state.get('show_code', False)
    
    # Toon code uitleg als gevraagd
    if st.session_state.get('show_code', False):
        with st.expander("💻 Code & Formules", expanded=True):
            # Map visualisatie naam naar analyse naam
            viz_to_analyse = {
                "GF1: Top 20 Producten": "DF1: Top 20 Producten",
                "GF2: Omzet Tijdlijn": "DF2: Omzet Tijdlijn",
                "GF3: Geografische Spreiding": "DF3: Geografische Spreiding",
                "GF4: Klanten Segmentatie": "DF4: Klanten Segmentatie (RFM)",
                "GF5: Bestellingen Heatmap": "DF5: Bestellingen Heatmap",
                "GF6: Product Categorieën": "DF6: Product Categorieën",
                "GF7: Betaalmethoden": "DF7: Betaalmethoden",
                "GF8: Kaas + Brood Combinaties": "DF8: Kaas + Brood Combinaties",
                "GF9: Verkooppatronen": "DF9: Verkooppatronen",
                "GF10: Prijsevolutie": "DF10: Prijsevolutie",
                "GF11: Toekomstvoorspelling": "DF11: Voorspellingen",
                "GF12: 55-jaar Voorspelling": "DF12: Lange Termijn",
                "GF13: Seizoens & Feestdagen": "DF13: Seizoens & Feestdagen",
                "GF14: Bestelpatronen": "DF14: Bestelpatronen",
                "GF15: Cross-selling": "DF15: Product Combinaties (Market Basket)",
                "GF16: Customer Lifetime Value": "DF16: Customer Lifetime Value",
                "GF17: Winstgevendheid": "DF17: Winstgevendheid",
                "GF18: Klanten Belonen": "DF18: Loyaliteitsprogramma"
            }
            
            analyse_naam = viz_to_analyse.get(selected_viz, selected_viz)
            code_data = get_code_uitleg(analyse_naam)
            
            # Toon welke grafiek dit is
            st.info(f"**📊 {code_data.get('grafiek', 'Grafiek informatie niet beschikbaar')}**")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 💻 Code")
                st.code(code_data.get('code', 'Code niet beschikbaar'), language='python')
            
            with col2:
                st.markdown("#### 📝 Uitleg")
                st.markdown(code_data.get('uitleg', 'Uitleg niet beschikbaar'))

    # Sluit de figure om geheugen te besparen
    plt.close(fig)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🧀 Delicatessenzaak Bestellingen Analyse | 
        Gemaakt met Streamlit | 
        Data bijgewerkt tot: """ + datetime.now().strftime('%d-%m-%Y') + """</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Instructies voor gebruiker in expander
with st.expander("ℹ️ Gebruiksinstructies"):
    st.markdown("""
    ### Hoe gebruik je dit dashboard?
    
    1. **Navigatie**: Gebruik de sidebar links om tussen categorieën en visualisaties te navigeren
    2. **Categorieën**: De analyses zijn gegroepeerd in 5 logische categorieën
    3. **Download**: Elke grafiek kan gedownload worden als PNG voor presentaties
    4. **Statistieken**: Algemene KPI's zijn zichtbaar in de sidebar
    
    ### Tips:
    - Gebruik fullscreen mode (rechtsboven) voor beste weergave
    - Grafieken zijn interactief - hover voor meer details
    - Download grafieken in hoge resolutie voor rapporten
    """)

# Developer info in expander
with st.expander("👨‍💻 Technische Details"):
    st.markdown("""
    ### Architectuur:
    - **Data Cleaning**: `data_cleaning.py` - Bereidt ruwe CSV data voor
    - **Data Analyse**: `data_analyse.py` - Voert alle berekeningen uit (DF1-DF18)
    - **Visualisaties**: `visualisaties.py` - Genereert alle grafieken (GF1-GF18)
    - **Web UI**: `streamlit_app.py` - Deze webinterface
    - **Code Uitleg**: `code_uitleg.py` - Wetenschappelijke formule documentatie
    - **Grafiek Uitleg**: `grafiek_uitleg.py` - Grafiek interpretatie gids
    
    ### Data:
    - Bron: `Bestellingen.csv`
    - Periode: """ + f"{df_bestellingen['besteldatum'].min().strftime('%d-%m-%Y')} tot {df_bestellingen['besteldatum'].max().strftime('%d-%m-%Y')}" + """
    - Totaal orders: """ + f"{aantal_bestellingen:,}" + """
    - Totaal producten: """ + f"{len(df_filtered):,}" + """
    """) 