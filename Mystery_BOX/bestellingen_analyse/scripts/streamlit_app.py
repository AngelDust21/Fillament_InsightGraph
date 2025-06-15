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
    }
}

# Selecteer categorie
selected_category = st.sidebar.selectbox(
    "Selecteer een categorie:",
    list(categories.keys())
)

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

# Toon geselecteerde visualisatie
st.markdown(f"### {selected_viz}")
fig = categories[selected_category][selected_viz]()
st.pyplot(fig)

# Download knop voor de visualisatie
buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
buf.seek(0)

st.download_button(
    label="📥 Download Visualisatie",
    data=buf,
    file_name=f"{selected_viz.lower().replace(' ', '_')}.png",
    mime="image/png"
)

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
    
    ### Data:
    - Bron: `Bestellingen.csv`
    - Periode: """ + f"{df_bestellingen['besteldatum'].min().strftime('%d-%m-%Y')} tot {df_bestellingen['besteldatum'].max().strftime('%d-%m-%Y')}" + """
    - Totaal orders: """ + f"{aantal_bestellingen:,}" + """
    - Totaal producten: """ + f"{len(df_filtered):,}" + """
    """) 