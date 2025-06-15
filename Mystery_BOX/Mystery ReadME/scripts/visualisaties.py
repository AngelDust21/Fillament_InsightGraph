"""
Visualisaties voor Bestellingen Analyse
GF1 t/m GF4 implementatie - gebruikt DFs uit data_analyse.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
import warnings
import os
warnings.filterwarnings('ignore')

# Configuratie voor mooiere grafieken
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

print("📊 Start visualisaties genereren...")
print("-" * 50)

# Importeer alles uit data_analyse
print("📈 Data importeren uit data_analyse.py...")
from data_analyse import (
    df1_top20_alfabetisch,
    df2_maanden, 
    df3_geo,
    df4_klanten,
    df5_uren,
    df6_categorie,
    df7_betaal,
    df8_brood_bij_kaas,
    df_filtered,
    df_bestellingen,
    bepaal_categorie,
    # Import DF9-DF18 resultaten
    df9_dag_omzet, df9_maand_omzet, df9_beste_uur, df9_beste_dag, df9_beste_maand,
    df10_kaas_jaar_trend, df10_vlees_jaar_trend, df10_kaas_jaarlijkse_groei, df10_vlees_jaarlijkse_groei,
    df11_omzet_per_jaar, df11_huidige_jaar, df11_groei_percentages,
    df12_scenarios, df12_kaas_prijs_nu, df12_vlees_prijs_nu,
    df13_maand_analyse, df13_feestdagen,
    df14_leadtime_data, df14_weekdag_orders, df14_gem_waarde_weekdag, df14_tijd_tussen,
    df15_combinaties, df15_categorie_combinaties, df15_attachment_rate, df15_multi_product_pct, df15_gem_producten_per_order,
    df16_ltv_segmenten, df16_cohort_analyse,
    df17_winst_per_categorie, df17_product_winst, df17_categorie_data, df17_totale_omzet, df17_totale_winst, df17_gem_marge,
    df18_vip_klanten, df18_loyale_klanten, df18_frequente_klanten, df18_rising_stars, df18_te_reactiveren
)

print("✅ Data succesvol geïmporteerd!")
print("-" * 50)

# GF1: Top 20 Producten Barplot
def gf1_top_producten_barplot():
    """GF1: Horizontale barplot van top 20 producten (alfabetisch)"""
    print("\n🎨 GF1: Top 20 Producten Barplot genereren...")
    
    # Bepaal categorieën voor kleuren
    categories = [bepaal_categorie(product) for product in df1_top20_alfabetisch.index]
    
    # Kleurenpalet
    categorie_kleuren = {
        'Kaas': '#FFD700',      # Goud
        'Vlees': '#DC143C',     # Crimson
        'Brood': '#8B4513',     # Bruin
        'Tapas': '#FF6347',     # Tomaat
        'Delicatessen': '#6B8E23', # Olijfgroen
        'Overig': '#4682B4'     # Staalblauw
    }
    
    # Maak de figuur
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Kleuren per product
    kleuren = [categorie_kleuren.get(cat, '#4682B4') for cat in categories]
    
    # Plot horizontale bars
    bars = ax.barh(df1_top20_alfabetisch.index, df1_top20_alfabetisch['totale_omzet'], color=kleuren)
    
    # Voeg waarde labels toe
    for bar, omzet in zip(bars, df1_top20_alfabetisch['totale_omzet']):
        ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
                f'€{omzet:,.0f}', va='center', fontsize=9)
    
    # Opmaak
    ax.set_xlabel('Totale Omzet (€)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Product', fontsize=12, fontweight='bold')
    ax.set_title('Top 20 Producten - Alfabetisch Gesorteerd', fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Legenda
    legend_elements = [Patch(facecolor=kleur, label=cat) 
                      for cat, kleur in categorie_kleuren.items()]
    ax.legend(handles=legend_elements, loc='lower right', title='Categorie')
    
    plt.tight_layout()
    return fig

# GF2: Omzet Tijdlijn per Maand
def gf2_omzet_tijdlijn():
    """GF2: Lijndiagram met maandelijkse omzet"""
    print("\n🎨 GF2: Omzet Tijdlijn genereren...")
    
    # Reset index voor plotting
    df2_plot = df2_maanden.reset_index()
    df2_plot['datum'] = pd.to_datetime(df2_plot['besteldatum'].astype(str))
    
    # Maak de figuur
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot de lijn
    ax.plot(df2_plot['datum'], df2_plot['totale_omzet'], 
            linewidth=3, color='#2E86AB', marker='o', markersize=8)
    
    # Voeg trendlijn toe
    z = np.polyfit(range(len(df2_plot)), df2_plot['totale_omzet'], 1)
    p = np.poly1d(z)
    ax.plot(df2_plot['datum'], p(range(len(df2_plot))), 
            "--", color='red', alpha=0.8, linewidth=2, label='Trendlijn')
    
    # Markeer piekmaanden
    for idx, row in df2_plot.iterrows():
        if row['totale_omzet'] > df2_plot['totale_omzet'].mean() * 2:
            ax.annotate(f"€{row['totale_omzet']:,.0f}", 
                       xy=(row['datum'], row['totale_omzet']), 
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=9, alpha=0.7,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
    
    # Opmaak
    ax.set_xlabel('Maand', fontsize=12, fontweight='bold')
    ax.set_ylabel('Totale Omzet (€)', fontsize=12, fontweight='bold')
    ax.set_title('Maandelijkse Omzet Evolutie', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Format y-as
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'€{x:,.0f}'))
    
    # Roteer x-as labels
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    return fig

# GF3: Geografische Spreiding Top 15 Woonplaatsen
def gf3_geografische_spreiding():
    """GF3: Staafdiagram van top 15 woonplaatsen"""
    print("\n🎨 GF3: Geografische Spreiding genereren...")
    
    # Reset index voor plotting
    df3_plot = df3_geo.reset_index()
    
    # Maak de figuur met twee subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Kleurenpalet
    colors1 = plt.cm.get_cmap('viridis')(np.linspace(0, 1, len(df3_plot)))
    colors2 = plt.cm.get_cmap('plasma')(np.linspace(0, 1, len(df3_plot)))
    
    # Subplot 1: Totale omzet
    bars1 = ax1.bar(range(len(df3_plot)), df3_plot['totale_omzet'], color=colors1)
    
    # Voeg percentages toe
    for i, (bar, pct) in enumerate(zip(bars1, df3_plot['percentage'])):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    ax1.set_xticks(range(len(df3_plot)))
    ax1.set_xticklabels(df3_plot['woonplaats'], rotation=45, ha='right')
    ax1.set_ylabel('Totale Omzet (€)', fontsize=12, fontweight='bold')
    ax1.set_title('Top 15 Woonplaatsen - Totale Omzet', fontsize=14, fontweight='bold')
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'€{x:,.0f}'))
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Aantal unieke klanten
    bars2 = ax2.bar(range(len(df3_plot)), df3_plot['unieke_klanten'], color=colors2)
    
    # Voeg gem. bestelwaarde toe
    for i, (bar, gem) in enumerate(zip(bars2, df3_plot['gem_bestelwaarde'])):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'€{gem:.0f}', ha='center', va='bottom', fontsize=8)
    
    ax2.set_xticks(range(len(df3_plot)))
    ax2.set_xticklabels(df3_plot['woonplaats'], rotation=45, ha='right')
    ax2.set_ylabel('Aantal Unieke Klanten', fontsize=12, fontweight='bold')
    ax2.set_title('Top 15 Woonplaatsen - Klantenaantal', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Geografische Analyse - Top 15 Woonplaatsen', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

# GF4: Klanten Segmentatie Matrix
def gf4_klanten_segmentatie_matrix():
    """GF4: Scatter plot van klanten segmentatie (RFM)"""
    print("\n🎨 GF4: Klanten Segmentatie Matrix genereren...")
    
    # Maak de figuur
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Maak scatter plot
    scatter = ax.scatter(df4_klanten['frequency'], df4_klanten['monetary'], 
                        c=df4_klanten['recency_dagen'], s=df4_klanten['monetary']/10,
                        cmap='RdYlGn_r', alpha=0.6, edgecolors='black', linewidth=1)
    
    # Voeg kleurenbalk toe
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Dagen sinds laatste bestelling', fontsize=12)
    
    # Bereken medianen voor kwadranten
    freq_mediaan = df4_klanten['frequency'].median()
    monetary_mediaan = df4_klanten['monetary'].median()
    
    ax.axvline(x=freq_mediaan, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=monetary_mediaan, color='gray', linestyle='--', alpha=0.5)
    
    # Label de kwadranten
    ax.text(freq_mediaan*1.5, monetary_mediaan*2, 'VIP\nKlanten', 
            fontsize=14, fontweight='bold', ha='center', alpha=0.7, 
            bbox=dict(boxstyle='round,pad=0.5', facecolor='gold', alpha=0.3))
    
    ax.text(freq_mediaan/2, monetary_mediaan*2, 'Nieuwe\nHoge Waarde', 
            fontsize=12, ha='center', alpha=0.7,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.3))
    
    ax.text(freq_mediaan*1.5, monetary_mediaan/2, 'Regelmatige\nKlanten', 
            fontsize=12, ha='center', alpha=0.7,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.3))
    
    ax.text(freq_mediaan/2, monetary_mediaan/2, 'Slapende\nKlanten', 
            fontsize=12, ha='center', alpha=0.7,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.3))
    
    # Markeer top 10 klanten
    top_10 = df4_klanten.nlargest(10, 'monetary')
    for idx, row in top_10.iterrows():
        ax.annotate('TOP', xy=(row['frequency'], row['monetary']), 
                   xytext=(5, 5), textcoords='offset points', fontsize=8, 
                   fontweight='bold', color='red')
    
    # Opmaak
    ax.set_xlabel('Frequency (Aantal Bestellingen)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Monetary (Totale Uitgaven €)', fontsize=12, fontweight='bold')
    ax.set_title('Klanten Segmentatie Matrix (RFM Analyse)', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    # Log schaal voor betere visualisatie
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    return fig

# GF5: Bestellingen Heatmap (Uur vs Dag)
def gf5_bestellingen_heatmap():
    """GF5: Heatmap van bestellingen per uur en dag"""
    print("\n🎨 GF5: Bestellingen Heatmap genereren...")
    
    # Maak pivot tabel voor heatmap
    df_filtered['weekdag'] = df_filtered['besteldatum'].dt.day_name()
    df_filtered['uur'] = pd.to_datetime(df_filtered['besteltijd'], format='%I:%M:%S %p').dt.hour
    
    # Dagen volgorde
    dagen_volgorde = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dagen_nl = ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo']
    
    # Maak pivot
    pivot = df_filtered.groupby(['uur', 'weekdag'])['bestelnummer'].nunique().reset_index()
    pivot = pivot.pivot(index='uur', columns='weekdag', values='bestelnummer').fillna(0)
    pivot = pivot.reindex(columns=dagen_volgorde)
    pivot.columns = dagen_nl
    
    # Maak de figuur
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Maak heatmap
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Aantal Bestellingen'}, ax=ax)
    
    # Opmaak
    ax.set_xlabel('Dag van de Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Uur van de Dag', fontsize=12, fontweight='bold')
    ax.set_title('Bestellingen Heatmap - Wanneer Bestellen Klanten?', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    return fig

# GF6: Product Categorie Donut Chart
def gf6_product_categorie_donut():
    """GF6: Donut diagram van product categorieën"""
    print("\n🎨 GF6: Product Categorie Donut genereren...")
    
    # Bereid data voor
    df6_plot = df6_categorie.sort_values('totaal_bedrag', ascending=False)
    
    # Kleuren
    kleuren = ['#FFD700', '#DC143C', '#8B4513', '#FF6347', '#6B8E23', '#4682B4']
    
    # Maak de figuur
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Maak donut
    wedges, texts, autotexts = ax.pie(df6_plot['totaal_bedrag'].values, 
                                      labels=df6_plot.index.tolist(), 
                                      colors=kleuren[:len(df6_plot)],
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      pctdistance=0.85)
    
    # Maak het een donut
    from matplotlib.patches import Circle
    centre_circle = Circle((0,0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Voeg totaal in het midden toe
    ax.text(0, 0, f'Totale Omzet\n€{df6_plot["totaal_bedrag"].sum():,.0f}', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Opmaak
    ax.set_title('Product Categorieën - Verdeling van Omzet', fontsize=16, fontweight='bold', pad=20)
    
    # Voeg legenda toe met details
    legend_labels = [f'{cat}: €{omzet:,.0f} ({pct:.1f}%)' 
                    for cat, omzet, pct in zip(df6_plot.index, df6_plot['totaal_bedrag'], df6_plot['percentage'])]
    ax.legend(wedges, legend_labels, loc="best", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    return fig

# GF7: Betaalmethode Analyse
def gf7_betaalmethode_analyse():
    """GF7: Analyse van betaalmethoden"""
    print("\n🎨 GF7: Betaalmethode Analyse genereren...")
    
    # Maak de figuur met twee subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Subplot 1: Staafdiagram aantal transacties
    df7_plot = df7_betaal.reset_index()
    bars1 = ax1.bar(range(len(df7_plot)), df7_plot['aantal_transacties'], 
                     color=plt.cm.Set3(np.linspace(0, 1, len(df7_plot))))
    
    # Labels
    for i, (bar, aantal) in enumerate(zip(bars1, df7_plot['aantal_transacties'])):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                str(aantal), ha='center', va='bottom', fontsize=10)
    
    ax1.set_xticks(range(len(df7_plot)))
    ax1.set_xticklabels(df7_plot['betaalmethode'], rotation=45, ha='right')
    ax1.set_ylabel('Aantal Transacties', fontsize=12, fontweight='bold')
    ax1.set_title('Aantal Transacties per Betaalmethode', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Box plot van bestelwaarden
    # Maak data voor boxplot
    betaal_data = []
    betaal_labels = []
    for methode in df7_plot['betaalmethode'][:3]:  # Top 3 voor duidelijkheid
        data = df_bestellingen[df_bestellingen['betaalmethode'] == methode]['totaal_bedrag']
        if len(data) > 0:
            betaal_data.append(data)
            betaal_labels.append(methode)
    
    bp = ax2.boxplot(betaal_data, labels=betaal_labels, patch_artist=True)
    
    # Kleuren voor boxplot
    for patch, color in zip(bp['boxes'], plt.cm.Set3(np.linspace(0, 1, len(betaal_labels)))):
        patch.set_facecolor(color)
    
    ax2.set_ylabel('Bestelwaarde (€)', fontsize=12, fontweight='bold')
    ax2.set_title('Verdeling Bestelwaarde per Betaalmethode (Top 3)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Betaalmethode Analyse', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

# GF8: Kaas + Brood Combinaties
def gf8_kaas_brood_combinaties():
    """GF8: Visualisatie van kaas+brood combinaties"""
    print("\n🎨 GF8: Kaas + Brood Combinaties genereren...")
    
    # Maak de figuur
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Subplot 1: Cirkeldiagram met/zonder brood
    sizes = [df8_brood_bij_kaas['met_brood'].iloc[0], df8_brood_bij_kaas['zonder_brood'].iloc[0]]
    labels = [f'Met Brood\n({sizes[0]})', f'Zonder Brood\n({sizes[1]})']
    colors = ['#FFD700', '#E0E0E0']
    explode = (0.1, 0)  # Highlight met brood
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.set_title('Kaasbestellingen: Met vs Zonder Brood', fontsize=14, fontweight='bold')
    
    # Subplot 2: Top broodsoorten bij kaas
    # Haal top broodsoorten uit data_analyse
    kaas_bestellingen = df_filtered[df_filtered['product_naam'].str.contains('aas', case=False, na=False)]['bestelnummer'].unique()
    brood_termen = ['brood', 'stok', 'baguette', 'ciabata', 'margot', 'spelt', 
                    'desem', 'walnoten vijgen', 'noten', 'krenten', 'foret', 
                    'houthakker', 'zwitsers', 'crackers']
    brood_mask = df_filtered['product_naam'].str.contains('|'.join(brood_termen), case=False, na=False)
    kaas_en_brood = set(kaas_bestellingen) & set(df_filtered[brood_mask]['bestelnummer'].unique())
    
    brood_bij_kaas = df_filtered[
        (df_filtered['bestelnummer'].isin(kaas_en_brood)) &
        (brood_mask)
    ]
    
    top_brood = brood_bij_kaas.groupby('product_naam')['aantal'].sum().nlargest(10)
    
    bars = ax2.barh(top_brood.index, top_brood.values, color='#8B4513')
    
    # Labels
    for bar, aantal in zip(bars, top_brood.values):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                str(aantal), va='center', fontsize=9)
    
    ax2.set_xlabel('Aantal Verkocht', fontsize=12, fontweight='bold')
    ax2.set_title('Top 10 Broodsoorten bij Kaasbestellingen', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.suptitle('Kaas + Brood Cross-Selling Analyse', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

# GF9: Verkooppatronen Analyse
def gf9_verkooppatronen():
    """GF9: Verkooppatronen Analyse - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('GF9: Verkooppatronen uit Echte Data', fontsize=16, fontweight='bold')
    
    # 1. Omzet per dag van de week - GEBRUIK GEÏMPORTEERDE DATA
    ax1 = axes[0, 0]
    dagen_nl = {
        'Monday': 'Ma', 'Tuesday': 'Di', 'Wednesday': 'Wo', 
        'Thursday': 'Do', 'Friday': 'Vr', 'Saturday': 'Za', 'Sunday': 'Zo'
    }
    dag_labels = [dagen_nl.get(dag, dag) for dag in df9_dag_omzet.index]
    bars = ax1.bar(range(len(df9_dag_omzet)), df9_dag_omzet.values, color='steelblue')
    ax1.set_xticks(range(len(df9_dag_omzet)))
    ax1.set_xticklabels(dag_labels)
    ax1.set_title('Omzet per Dag van de Week')
    ax1.set_ylabel('Omzet (€)')
    ax1.grid(axis='y', alpha=0.3)
    
    # Voeg waarden toe op de bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'€{height:.0f}', ha='center', va='bottom')
    
    # 2. Omzet per maand - GEBRUIK GEÏMPORTEERDE DATA
    ax2 = axes[0, 1]
    maand_namen = {
        1: 'Jan', 2: 'Feb', 3: 'Mrt', 4: 'Apr',
        5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Dec'
    }
    maand_labels = [maand_namen[m] for m in df9_maand_omzet.index]
    bars2 = ax2.bar(range(len(df9_maand_omzet)), df9_maand_omzet['totaal_bedrag'].values, 
                    color='darkgreen')
    ax2.set_xticks(range(len(df9_maand_omzet)))
    ax2.set_xticklabels(maand_labels, rotation=45)
    ax2.set_title('Seizoenspatroon: Omzet per Maand')
    ax2.set_ylabel('Omzet (€)')
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Uurpatroon - GEBRUIK BESTAANDE DATA
    ax3 = axes[1, 0]
    # Check of uur kolom al bestaat, anders toevoegen
    if 'uur' not in df_filtered.columns:
        df_filtered['uur'] = pd.to_datetime(df_filtered['besteltijd'], format='%I:%M:%S %p').dt.hour
    uur_omzet = df_filtered.groupby('uur')['totaal_bedrag'].sum()
    ax3.plot(uur_omzet.index, uur_omzet.values, marker='o', linewidth=2, 
             markersize=8, color='darkred')
    ax3.fill_between(uur_omzet.index, uur_omzet.values, alpha=0.3, color='darkred')
    ax3.set_title('Omzet per Uur van de Dag')
    ax3.set_xlabel('Uur')
    ax3.set_ylabel('Omzet (€)')
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(range(0, 24, 2))
    
    # Markeer het beste uur - GEBRUIK GEÏMPORTEERDE DATA
    ax3.axvline(x=df9_beste_uur, color='red', linestyle='--', alpha=0.5)
    ax3.text(df9_beste_uur, ax3.get_ylim()[1]*0.9, f'Piek: {df9_beste_uur}:00', 
             ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
    
    # 4. Conclusies - GEBRUIK GEÏMPORTEERDE DATA
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    conclusies_text = f"""
    BELANGRIJKSTE INZICHTEN:
    
    • Drukste dag: {dagen_nl.get(df9_beste_dag, df9_beste_dag)}
    • Beste uur: {df9_beste_uur}:00 - {df9_beste_uur+1}:00
    • Beste maand: {maand_namen[df9_beste_maand]}
    
    • Weekpatroon: Weekend is drukker
    • Dagpatroon: Piek rond lunch/namiddag
    • Seizoen: Zomer maanden zijn rustiger
    
    NOTE: Dit zijn bestelpatronen,
    niet wanneer klanten online zijn!
    """
    
    ax4.text(0.05, 0.95, conclusies_text, transform=ax4.transAxes,
             fontsize=12, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    return fig

# GF10: Prijsevolutie Analyse
def gf10_prijsevolutie():
    """GF10: Prijsevolutie Kaas- en Vleesschotels - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF10: Prijsevolutie per Persoon', fontsize=16, fontweight='bold')
    
    # 1. Kaasschotels evolutie
    ax1 = axes[0, 0]
    if len(df10_kaas_jaar_trend) > 0:
        jaren = df10_kaas_jaar_trend.index
        prijzen = df10_kaas_jaar_trend.values
        ax1.plot(jaren, prijzen, marker='o', linewidth=2, markersize=10, color='orange', label='Gemiddelde prijs')
        ax1.fill_between(jaren, prijzen, alpha=0.3, color='orange')
        ax1.set_title('Kaasschotels - Prijs per Persoon')
        ax1.set_xlabel('Jaar')
        ax1.set_ylabel('Prijs per persoon (€)')
        ax1.grid(True, alpha=0.3)
        
        # Voeg trendlijn toe
        if len(jaren) > 1:
            z = np.polyfit(jaren, prijzen, 1)
            p = np.poly1d(z)
            ax1.plot(jaren, p(jaren), "--", color='red', alpha=0.7, label='Trend')
        
        ax1.legend()
        
        # Voeg groeipercentage toe
        if df10_kaas_jaarlijkse_groei > 0:
            ax1.text(0.05, 0.95, f'Gem. groei: {df10_kaas_jaarlijkse_groei:.1f}%/jaar', 
                    transform=ax1.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 2. Vleesschotels evolutie
    ax2 = axes[0, 1]
    if len(df10_vlees_jaar_trend) > 0:
        jaren = df10_vlees_jaar_trend.index
        prijzen = df10_vlees_jaar_trend.values
        ax2.plot(jaren, prijzen, marker='s', linewidth=2, markersize=10, color='darkred', label='Gemiddelde prijs')
        ax2.fill_between(jaren, prijzen, alpha=0.3, color='darkred')
        ax2.set_title('Vleesschotels - Prijs per Persoon')
        ax2.set_xlabel('Jaar')
        ax2.set_ylabel('Prijs per persoon (€)')
        ax2.grid(True, alpha=0.3)
        
        # Voeg trendlijn toe
        if len(jaren) > 1:
            z = np.polyfit(jaren, prijzen, 1)
            p = np.poly1d(z)
            ax2.plot(jaren, p(jaren), "--", color='blue', alpha=0.7, label='Trend')
        
        ax2.legend()
        
        # Voeg groeipercentage toe
        if df10_vlees_jaarlijkse_groei > 0:
            ax2.text(0.05, 0.95, f'Gem. groei: {df10_vlees_jaarlijkse_groei:.1f}%/jaar', 
                    transform=ax2.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 3. Vergelijking kaas vs vlees
    ax3 = axes[1, 0]
    if len(df10_kaas_jaar_trend) > 0 and len(df10_vlees_jaar_trend) > 0:
        ax3.plot(df10_kaas_jaar_trend.index, df10_kaas_jaar_trend.values, 
                marker='o', linewidth=2, markersize=8, color='orange', label='Kaas')
        ax3.plot(df10_vlees_jaar_trend.index, df10_vlees_jaar_trend.values, 
                marker='s', linewidth=2, markersize=8, color='darkred', label='Vlees')
        ax3.set_title('Vergelijking Kaas vs Vlees')
        ax3.set_xlabel('Jaar')
        ax3.set_ylabel('Prijs per persoon (€)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    # 4. Samenvatting
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Bereken huidige prijzen
    huidige_kaas = df10_kaas_jaar_trend.iloc[-1] if len(df10_kaas_jaar_trend) > 0 else 0
    huidige_vlees = df10_vlees_jaar_trend.iloc[-1] if len(df10_vlees_jaar_trend) > 0 else 0
    
    info_text = f"""
    PRIJSEVOLUTIE ANALYSE:
    
    Kaasschotels:
    • Huidige prijs: €{huidige_kaas:.2f} per persoon
    • Jaarlijkse stijging: {df10_kaas_jaarlijkse_groei:.1f}%
    
    Vleesschotels:
    • Huidige prijs: €{huidige_vlees:.2f} per persoon
    • Jaarlijkse stijging: {df10_vlees_jaarlijkse_groei:.1f}%
    
    Algemeen:
    • Prijzen stijgen consistent
    • Inflatie + kwaliteitsverbetering
    • Marktpositie: Premium segment
    """
    
    ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    plt.tight_layout()
    return fig

# GF11: Toekomstvoorspelling
def gf11_toekomstvoorspelling():
    """GF11: Toekomstvoorspelling - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF11: Voorspelling Komende 5 Jaar', fontsize=16, fontweight='bold')
    
    # 1. Historische omzet + voorspelling
    ax1 = axes[0, 0]
    
    # Plot historische data
    jaren_hist = df11_omzet_per_jaar.index
    omzet_hist = df11_omzet_per_jaar.values
    ax1.plot(jaren_hist, omzet_hist, marker='o', linewidth=2, 
             markersize=10, color='blue', label='Historisch')
    
    # Voorspelling voor komende 5 jaar
    toekomst_jaren = range(df11_huidige_jaar + 1, df11_huidige_jaar + 6)
    huidige_omzet = omzet_hist[-1] if len(omzet_hist) > 0 else 50000
    
    # Constante groei scenario
    const_groei = []
    omzet = huidige_omzet
    for i in range(5):
        omzet *= 1.565  # 56.5% groei zoals berekend
        const_groei.append(omzet)
    
    ax1.plot(toekomst_jaren, const_groei, marker='o', linewidth=2,
             markersize=8, color='green', linestyle='--', label='Historisch model (56.5%/jr)')
    
    # Realistisch scenario met afvlakkende groei
    real_groei = []
    omzet = huidige_omzet
    for i, groei_pct in enumerate(df11_groei_percentages):
        omzet *= (1 + groei_pct / 100)
        real_groei.append(omzet)
    
    ax1.plot(toekomst_jaren, real_groei, marker='s', linewidth=2,
             markersize=8, color='orange', linestyle='--', label='Realistisch (afvlakkend)')
    
    ax1.set_title('Omzet Voorspelling')
    ax1.set_xlabel('Jaar')
    ax1.set_ylabel('Omzet (€)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000:.0f}K'))
    
    # 2. Groeipercentages over tijd
    ax2 = axes[0, 1]
    
    # Bereken historische groeipercentages
    hist_groei = []
    for i in range(1, len(omzet_hist)):
        groei = ((omzet_hist[i] - omzet_hist[i-1]) / omzet_hist[i-1] * 100)
        hist_groei.append(groei)
    
    if hist_groei:
        ax2.bar(range(len(hist_groei)), hist_groei, color='blue', alpha=0.7, label='Historisch')
    
    # Voorspelde groeipercentages
    x_offset = len(hist_groei)
    ax2.bar(range(x_offset, x_offset + 5), df11_groei_percentages, 
            color='orange', alpha=0.7, label='Voorspelling')
    
    ax2.set_title('Groeipercentages per Jaar')
    ax2.set_xlabel('Jaar (vanaf start)')
    ax2.set_ylabel('Groei (%)')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=0, color='black', linewidth=0.5)
    
    # 3. Aantal orders voorspelling
    ax3 = axes[1, 0]
    
    # Bereken orders voorspelling
    orders_nu = len(df_bestellingen[df_bestellingen['besteldatum'].dt.year == df11_huidige_jaar])
    orders_voorspelling = [orders_nu]
    
    for groei in df11_groei_percentages:
        orders_nu *= (1 + groei / 200)  # Orders groeien langzamer
        orders_voorspelling.append(orders_nu)
    
    jaren_orders = list(range(df11_huidige_jaar, df11_huidige_jaar + 6))
    ax3.plot(jaren_orders, orders_voorspelling, marker='o', linewidth=2,
             markersize=10, color='purple')
    ax3.fill_between(jaren_orders, orders_voorspelling, alpha=0.3, color='purple')
    ax3.set_title('Verwachte Aantal Orders')
    ax3.set_xlabel('Jaar')
    ax3.set_ylabel('Aantal Orders')
    ax3.grid(True, alpha=0.3)
    
    # 4. Samenvatting
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary_text = f"""
    VOORSPELLING SAMENVATTING:
    
    Huidige situatie ({df11_huidige_jaar}):
    • Omzet: €{omzet_hist[-1] if len(omzet_hist) > 0 else 0:,.0f}
    • Orders: {len(df_bestellingen[df_bestellingen['besteldatum'].dt.year == df11_huidige_jaar])}
    
    Verwachting {df11_huidige_jaar + 5}:
    • Omzet (realistisch): €{real_groei[-1]:,.0f}
    • Omzet (historisch): €{const_groei[-1]:,.0f}
    • Orders: {orders_voorspelling[-1]:.0f}
    
    Groeimodel:
    • Jaar 1: +{df11_groei_percentages[0]}%
    • Jaar 2: +{df11_groei_percentages[1]}%
    • Jaar 3: +{df11_groei_percentages[2]}%
    • Jaar 4: +{df11_groei_percentages[3]}%
    • Jaar 5: +{df11_groei_percentages[4]}%
    """
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout()
    return fig

# GF12: Prijsvoorspelling 2080
def gf12_lange_termijn():
    """GF12: 55-jaar voorspelling - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF12: Lange Termijn Voorspelling (55 jaar)', fontsize=16, fontweight='bold')
    
    # 1. Prijsevolutie gastronomische schotels
    ax1 = axes[0, 0]
    
    jaren = list(range(2025, 2081, 5))
    
    # Bereken prijzen voor elk scenario - GEBRUIK GEÏMPORTEERDE DATA
    for scenario_naam, params in df12_scenarios.items():
        kaas_prijzen = []
        vlees_prijzen = []
        
        kaas_prijs = df12_kaas_prijs_nu
        vlees_prijs = df12_vlees_prijs_nu
        
        for jaar in jaren:
            jaren_vooruit = jaar - 2025
            factor = (1 + (params['groei'] + params['inflatie']) / 100) ** jaren_vooruit
            kaas_prijzen.append(kaas_prijs * factor)
            vlees_prijzen.append(vlees_prijs * factor)
        
        if scenario_naam == 'Realistisch':
            ax1.plot(jaren, kaas_prijzen, marker='o', linewidth=2, 
                    label=f'Kaas - {scenario_naam}', color='orange')
            ax1.plot(jaren, vlees_prijzen, marker='s', linewidth=2,
                    label=f'Vlees - {scenario_naam}', color='darkred')
        else:
            ax1.plot(jaren, kaas_prijzen, linewidth=1, linestyle='--',
                    alpha=0.5, label=f'Kaas - {scenario_naam}')
            ax1.plot(jaren, vlees_prijzen, linewidth=1, linestyle='--',
                    alpha=0.5, label=f'Vlees - {scenario_naam}')
    
    ax1.set_title('Prijsevolutie Gastronomische Schotels')
    ax1.set_xlabel('Jaar')
    ax1.set_ylabel('Prijs per persoon (€)')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # 2. Inflatie-gecorrigeerde prijzen
    ax2 = axes[0, 1]
    
    # Realistisch scenario in constante euro's - GEBRUIK GEÏMPORTEERDE DATA
    params = df12_scenarios['Realistisch']
    jaren_kort = list(range(2025, 2081, 10))
    kaas_echt = []
    vlees_echt = []
    
    for jaar in jaren_kort:
        jaren_vooruit = jaar - 2025
        groei_factor = (1 + params['groei'] / 100) ** jaren_vooruit
        kaas_echt.append(df12_kaas_prijs_nu * groei_factor)
        vlees_echt.append(df12_vlees_prijs_nu * groei_factor)
    
    ax2.plot(jaren_kort, kaas_echt, marker='o', linewidth=2, 
            markersize=10, color='orange', label='Kaas (2025 euro\'s)')
    ax2.plot(jaren_kort, vlees_echt, marker='s', linewidth=2,
            markersize=10, color='darkred', label='Vlees (2025 euro\'s)')
    
    ax2.set_title('Reële Prijzen (inflatie-gecorrigeerd)')
    ax2.set_xlabel('Jaar')
    ax2.set_ylabel('Prijs in 2025 euro\'s')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Scenario vergelijking 2080
    ax3 = axes[1, 0]
    
    scenario_namen = list(df12_scenarios.keys())
    kaas_2080 = []
    vlees_2080 = []
    
    for scenario_naam, params in df12_scenarios.items():
        factor = (1 + (params['groei'] + params['inflatie']) / 100) ** 55
        kaas_2080.append(df12_kaas_prijs_nu * factor)
        vlees_2080.append(df12_vlees_prijs_nu * factor)
    
    x = np.arange(len(scenario_namen))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, kaas_2080, width, label='Kaas', color='orange')
    bars2 = ax3.bar(x + width/2, vlees_2080, width, label='Vlees', color='darkred')
    
    ax3.set_xlabel('Scenario')
    ax3.set_ylabel('Prijs in 2080 (€)')
    ax3.set_title('Prijzen per Scenario in 2080')
    ax3.set_xticks(x)
    ax3.set_xticklabels(scenario_namen)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Voeg waarden toe
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'€{height:.0f}', ha='center', va='bottom', fontsize=9)
    
    # 4. Conclusies
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Bereken realistische waarden - GEBRUIK GEÏMPORTEERDE DATA
    real_params = df12_scenarios['Realistisch']
    factor_55 = (1 + (real_params['groei'] + real_params['inflatie']) / 100) ** 55
    inflatie_factor = (1 + real_params['inflatie'] / 100) ** 55
    
    kaas_2080_nom = df12_kaas_prijs_nu * factor_55
    vlees_2080_nom = df12_vlees_prijs_nu * factor_55
    kaas_2080_real = kaas_2080_nom / inflatie_factor
    vlees_2080_real = vlees_2080_nom / inflatie_factor
    
    conclusie_text = f"""
    LANGE TERMIJN VOORSPELLING:
    
    Huidige prijzen (2025):
    • Kaas gastronomisch: €{df12_kaas_prijs_nu:.2f} pp
    • Vlees gastronomisch: €{df12_vlees_prijs_nu:.2f} pp
    
    Realistische voorspelling 2080:
    • Kaas: €{kaas_2080_nom:.0f} (nominaal)
            €{kaas_2080_real:.2f} (in 2025 euro's)
    
    • Vlees: €{vlees_2080_nom:.0f} (nominaal)
             €{vlees_2080_real:.2f} (in 2025 euro's)
    
    Belangrijke factoren:
    • Inflatie: {real_params['inflatie']}% per jaar
    • Reële groei: {real_params['groei']}% per jaar
    • Totale inflatie 55 jaar: {(inflatie_factor-1)*100:.0f}%
    """
    
    ax4.text(0.05, 0.95, conclusie_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))
    
    plt.tight_layout()
    return fig

# GF13: Seizoens & Feestdagen Analyse
def gf13_seizoens_feestdagen():
    """GF13: Seizoens & Feestdagen - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF13: Seizoens & Feestdagen Analyse', fontsize=16, fontweight='bold')
    
    # 1. Maandelijkse omzet patroon
    ax1 = axes[0, 0]
    
    maand_namen = {
        1: 'Jan', 2: 'Feb', 3: 'Mrt', 4: 'Apr',
        5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Dec'
    }
    
    maanden = list(range(1, 13))
    omzetten = []
    for maand in maanden:
        if maand in df13_maand_analyse.index:
            omzetten.append(df13_maand_analyse.loc[maand, 'totale_omzet'])
        else:
            omzetten.append(0)
    
    bars = ax1.bar(maanden, omzetten, color='skyblue', edgecolor='navy')
    ax1.set_xticks(maanden)
    ax1.set_xticklabels([maand_namen[m] for m in maanden])
    ax1.set_title('Omzet per Maand')
    ax1.set_ylabel('Totale Omzet (€)')
    ax1.grid(axis='y', alpha=0.3)
    
    # Markeer gemiddelde
    gem_omzet = np.mean(omzetten)
    ax1.axhline(y=gem_omzet, color='red', linestyle='--', label=f'Gemiddelde: €{gem_omzet:.0f}')
    ax1.legend()
    
    # 2. Kwartaal analyse
    ax2 = axes[0, 1]
    
    kwartaal_data = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.quarter)['totaal_bedrag'].sum()
    kwartaal_labels = ['Q1\n(Jan-Mrt)', 'Q2\n(Apr-Jun)', 'Q3\n(Jul-Sep)', 'Q4\n(Okt-Dec)']
    
    if len(kwartaal_data) > 0:
        bars2 = ax2.bar(range(len(kwartaal_data)), kwartaal_data.values, 
                        color=['lightblue', 'lightgreen', 'lightyellow', 'lightcoral'])
        ax2.set_xticks(range(len(kwartaal_data)))
        ax2.set_xticklabels(kwartaal_labels[:len(kwartaal_data)])
        ax2.set_title('Omzet per Kwartaal')
        ax2.set_ylabel('Omzet (€)')
        ax2.grid(axis='y', alpha=0.3)
        
        # Voeg percentages toe
        totaal = kwartaal_data.sum()
        for i, bar in enumerate(bars2):
            height = bar.get_height()
            pct = height / totaal * 100
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{pct:.1f}%', ha='center', va='bottom')
    
    # 3. Feestdagen impact (placeholder - echte data niet beschikbaar)
    ax3 = axes[1, 0]
    
    # Simuleer feestdagen data gebaseerd op maandpatronen
    feestdagen = ['Kerst/NY', 'Pasen', 'Communies', 'Moederdag', 'Halloween']
    impact = [15, 8, 12, 5, 3]  # Geschatte percentages
    colors = ['red', 'yellow', 'lightblue', 'pink', 'orange']
    
    bars3 = ax3.bar(feestdagen, impact, color=colors, alpha=0.7)
    ax3.set_title('Geschatte Feestdagen Impact')
    ax3.set_ylabel('% van Jaaromzet')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%', ha='center', va='bottom')
    
    # 4. Seizoensadvies
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Bepaal piek en dal maanden
    if len(df13_maand_analyse) > 0:
        piek_maand = df13_maand_analyse['totale_omzet'].idxmax()
        dal_maand = df13_maand_analyse['totale_omzet'].idxmin()
        
        advies_text = f"""
        SEIZOENSPATRONEN & ADVIES:
        
        Piekperiodes:
        • {maand_namen[piek_maand]}: Hoogste omzet
        • Q4: Feestdagen seizoen
        • Mei: Communies
        
        Rustige periodes:
        • {maand_namen[dal_maand]}: Laagste omzet
        • Zomermaanden: Vakantieperiode
        
        Aanbevelingen:
        • Plan extra capaciteit in Q4
        • Ontwikkel zomer promoties
        • Focus op feestdagen marketing
        • Bouw voorraad op voor piekperiodes
        
        Feestdagen strategie:
        • Kerst: Premium geschenkpakketten
        • Pasen: Familie brunch schotels
        • Communies: Kinderfeest opties
        """
    else:
        advies_text = "Geen seizoensdata beschikbaar"
    
    ax4.text(0.05, 0.95, advies_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout()
    return fig

# GF14: Bestel Leadtime Analyse
def gf14_leadtime_analyse():
    """GF14: Leadtime Analyse - alternatieve visualisatie bij lege data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF14: Bestelpatronen Analyse (Leadtime data niet beschikbaar)', fontsize=16, fontweight='bold')
    
    # Aangezien leadtime data leeg is, toon andere nuttige patronen
    
    # 1. Bestellingen per weekdag - GEBRUIK GEÏMPORTEERDE DATA
    ax1 = axes[0, 0]
    
    dagen_nl = {
        'Monday': 'Maandag', 'Tuesday': 'Dinsdag', 'Wednesday': 'Woensdag',
        'Thursday': 'Donderdag', 'Friday': 'Vrijdag', 'Saturday': 'Zaterdag', 'Sunday': 'Zondag'
    }
    dagen_volgorde = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    bars = ax1.bar(range(len(df14_weekdag_orders)), df14_weekdag_orders.values, 
                   color=['gray']*5 + ['lightcoral', 'lightcoral'])
    ax1.set_xticks(range(len(df14_weekdag_orders)))
    ax1.set_xticklabels([dagen_nl[d] for d in dagen_volgorde], rotation=45)
    ax1.set_title('Aantal Bestellingen per Weekdag')
    ax1.set_ylabel('Aantal Orders')
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Gemiddelde bestelwaarde per dag - GEBRUIK GEÏMPORTEERDE DATA
    ax2 = axes[0, 1]
    
    ax2.plot(range(len(df14_gem_waarde_weekdag)), df14_gem_waarde_weekdag.values, marker='o', 
             linewidth=2, markersize=10, color='darkgreen')
    ax2.set_xticks(range(len(df14_gem_waarde_weekdag)))
    ax2.set_xticklabels([dagen_nl[d] for d in dagen_volgorde], rotation=45)
    ax2.set_title('Gemiddelde Bestelwaarde per Weekdag')
    ax2.set_ylabel('Gemiddelde Waarde (€)')
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:.0f}'))
    
    # 3. Tijd tussen bestellingen per klant - GEBRUIK GEÏMPORTEERDE DATA
    ax3 = axes[1, 0]
    
    if df14_tijd_tussen:
        bins = [0, 7, 14, 30, 60, 90, 180, 365]
        labels = ['<1 week', '1-2 weken', '2-4 weken', '1-2 mnd', 
                 '2-3 mnd', '3-6 mnd', '>6 mnd']
        
        hist, edges = np.histogram(df14_tijd_tussen, bins=bins)
        ax3.bar(range(len(labels)), hist, color='skyblue', edgecolor='navy')
        ax3.set_xticks(range(len(labels)))
        ax3.set_xticklabels(labels, rotation=45)
        ax3.set_title('Tijd tussen Herhalingsaankopen')
        ax3.set_ylabel('Aantal')
        ax3.grid(axis='y', alpha=0.3)
    
    # 4. Advies zonder leadtime data
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    advies_text = """
    BESTELPATRONEN INZICHTEN:
    
    Weekpatronen:
    • Weekend heeft meer bestellingen
    • Vrijdag populairste besteldag
    • Maandag rustigste dag
    
    Herhalingsgedrag:
    • Meeste klanten bestellen om de 2-4 weken
    • Seizoensklanten komen terug na 3-6 maanden
    • Kernklanten bestellen wekelijks
    
    AANBEVELINGEN (zonder leadtime data):
    • Implementeer "Verwerken voor" veld in systeem
    • Track wanneer klanten product nodig hebben
    • Analyseer ideale voorbereidingstijd
    • Optimaliseer planning en capaciteit
    
    Met leadtime data kunnen we:
    • Last-minute vs geplande orders analyseren
    • Capaciteit beter plannen
    • Express service aanbieden
    """
    
    ax4.text(0.05, 0.95, advies_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    return fig

# GF15: Product Combinatie Matrix
def gf15_product_combinaties():
    """GF15: Product Combinaties - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF15: Cross-selling Analyse', fontsize=16, fontweight='bold')
    
    # 1. Top combinaties
    ax1 = axes[0, 0]
    
    if len(df15_combinaties) > 0:
        # Neem top 10 combinaties
        top10 = df15_combinaties.head(10)
        
        # Maak labels korter
        labels = []
        for _, row in top10.iterrows():
            combo = row['combinatie']
            label = f"{combo[0][:15]}... +\n{combo[1][:15]}..."
            labels.append(label)
        
        y_pos = np.arange(len(labels))
        ax1.barh(y_pos, top10['frequentie'], color='steelblue')
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(labels, fontsize=8)
        ax1.set_xlabel('Frequentie')
        ax1.set_title('Top 10 Product Combinaties')
        ax1.grid(axis='x', alpha=0.3)
        
        # Voeg waarden toe
        for i, v in enumerate(top10['frequentie']):
            ax1.text(v + 0.1, i, str(v), va='center')
    
    # 2. Categorie combinaties
    ax2 = axes[0, 1]
    
    if len(df15_categorie_combinaties) > 0:
        # Pie chart van categorie combinaties
        labels = []
        sizes = []
        for _, row in df15_categorie_combinaties.iterrows():
            combo = row['categorie_combo']
            labels.append(f"{combo[0]} + {combo[1]}")
            sizes.append(row['aantal'])
        
        # Neem alleen top 5 voor leesbaarheid
        if len(labels) > 5:
            andere = sum(sizes[5:])
            labels = labels[:5] + ['Andere']
            sizes = sizes[:5] + [andere]
        
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(sizes)))
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90)
        ax2.set_title('Categorie Combinaties')
        
        # Maak percentages kleiner
        for autotext in autotexts:
            autotext.set_fontsize(8)
    
    # 3. Attachment rate per categorie - GEBRUIK GEÏMPORTEERDE DATA
    ax3 = axes[1, 0]
    
    if df15_attachment_rate:
        categories = list(df15_attachment_rate.keys())
        rates = list(df15_attachment_rate.values())
        
        bars = ax3.bar(categories, rates, color='lightgreen', edgecolor='darkgreen')
        ax3.set_title('Cross-sell Rate per Hoofdcategorie')
        ax3.set_ylabel('% Orders met Multiple Producten')
        ax3.set_xlabel('Hoofdcategorie')
        ax3.grid(axis='y', alpha=0.3)
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        
        # Voeg percentages toe
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
    
    # 4. Cross-sell aanbevelingen
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # GEBRUIK GEÏMPORTEERDE STATISTIEKEN
    
    aanbevelingen_text = f"""
    CROSS-SELLING INZICHTEN:
    
    Statistieken:
    • {df15_multi_product_pct:.1f}% van orders heeft meerdere producten
    • Gemiddeld {df15_gem_producten_per_order:.1f} producten per order
    
    Beste Combinaties:
    • Kaas + Brood (natuurlijke match)
    • Kaas + Vlees (variatie)
    • Schotels + Delicatessen
    
    Opportuniteiten:
    • Kaas zonder brood: {100-21.9:.1f}% mist brood
    • Bundel aanbiedingen maken
    • "Vergeet niet" suggesties bij checkout
    
    Acties:
    • Creëer combideals
    • Train personeel op suggesties
    • Online: "vaak samen gekocht"
    • Seizoensgebonden bundels
    """
    
    ax4.text(0.05, 0.95, aanbevelingen_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    return fig

# GF16: Klant Lifetime Value
def gf16_klant_lifetime_value():
    """GF16: Customer Lifetime Value - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF16: Customer Lifetime Value Analyse', fontsize=16, fontweight='bold')
    
    # 1. LTV Segmenten verdeling
    ax1 = axes[0, 0]
    
    segment_sizes = {}
    segment_values = {}
    
    for segment_name, klanten_df in df16_ltv_segmenten.items():
        if len(klanten_df) > 0:
            segment_sizes[segment_name] = len(klanten_df)
            segment_values[segment_name] = klanten_df['voorspelde_ltv_3jaar'].sum()
    
    if segment_sizes:
        # Pie chart van aantal klanten per segment
        labels = list(segment_sizes.keys())
        sizes = list(segment_sizes.values())
        colors = ['gold', 'silver', '#CD7F32', 'lightgray'][:len(sizes)]
        
        wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
                                           colors=colors, startangle=90)
        ax1.set_title('Klanten per LTV Segment')
    
    # 2. LTV waarde per segment
    ax2 = axes[0, 1]
    
    if segment_values:
        segments = list(segment_values.keys())
        values = [segment_values[s]/1000 for s in segments]  # In duizenden
        
        bars = ax2.bar(segments, values, color=['gold', 'silver', '#CD7F32', 'lightgray'][:len(segments)])
        ax2.set_title('Totale LTV Waarde per Segment')
        ax2.set_ylabel('Voorspelde 3-jaar LTV (€1000)')
        ax2.grid(axis='y', alpha=0.3)
        
        # Voeg waarden toe
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'€{height:.0f}K', ha='center', va='bottom')
    
    # 3. Cohort retentie
    ax3 = axes[1, 0]
    
    if len(df16_cohort_analyse) > 0:
        jaren = df16_cohort_analyse.index
        retentie = df16_cohort_analyse['retentie_rate'].values
        
        ax3.plot(jaren, retentie, marker='o', linewidth=2, markersize=10, color='darkblue')
        ax3.fill_between(jaren, retentie, alpha=0.3, color='darkblue')
        ax3.set_title('Retentie Rate per Cohort Jaar')
        ax3.set_xlabel('Aanmeldjaar')
        ax3.set_ylabel('Retentie Rate (%)')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 100)
        
        # Voeg gemiddelde lijn toe
        gem_retentie = retentie.mean()
        ax3.axhline(y=gem_retentie, color='red', linestyle='--', 
                   label=f'Gemiddelde: {gem_retentie:.1f}%')
        ax3.legend()
    
    # 4. LTV insights
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Bereken totalen
    totaal_klanten = sum(segment_sizes.values()) if segment_sizes else 0
    totale_ltv = sum(segment_values.values()) if segment_values else 0
    gem_ltv = totale_ltv / totaal_klanten if totaal_klanten > 0 else 0
    
    insights_text = f"""
    LIFETIME VALUE INSIGHTS:
    
    Overzicht:
    • Totaal klanten: {totaal_klanten}
    • Totale voorspelde LTV: €{totale_ltv:,.0f}
    • Gemiddelde LTV: €{gem_ltv:,.0f}
    
    Segmentatie:
    • Focus op Diamond & Gold klanten
    • Bronze klanten kunnen groeien
    • Retentie cruciaal voor LTV
    
    Acties per segment:
    • Diamond: VIP behandeling, events
    • Gold: Loyaliteitsprogramma
    • Silver: Upsell campagnes
    • Bronze: Activatie programma's
    
    Retentie strategie:
    • Eerste 6 maanden cruciaal
    • Regelmatig contact onderhouden
    • Persoonlijke aanbiedingen
    """
    
    ax4.text(0.05, 0.95, insights_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='gold', alpha=0.2))
    
    plt.tight_layout()
    return fig

# GF17: Winstgevendheid Dashboard
def gf17_winstgevendheid():
    """GF17: Winstgevendheid Analyse - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF17: Winstgevendheid Analyse', fontsize=16, fontweight='bold')
    
    # 1. Winst per categorie
    ax1 = axes[0, 0]
    
    if len(df17_winst_per_categorie) > 0:
        categories = df17_winst_per_categorie.index
        winst = df17_winst_per_categorie['geschatte_winst'].values
        
        # Sorteer op winst
        sorted_idx = np.argsort(winst)[::-1]
        categories_sorted = [categories[i] for i in sorted_idx]
        winst_sorted = winst[sorted_idx]
        
        bars = ax1.bar(range(len(categories_sorted)), winst_sorted, 
                       color='darkgreen', alpha=0.7)
        ax1.set_xticks(range(len(categories_sorted)))
        ax1.set_xticklabels(categories_sorted, rotation=45)
        ax1.set_title('Geschatte Winst per Categorie')
        ax1.set_ylabel('Winst (€)')
        ax1.grid(axis='y', alpha=0.3)
        
        # Voeg margepercentages toe
        for i, (cat, bar) in enumerate(zip(categories_sorted, bars)):
            marge = df17_winst_per_categorie.loc[cat, 'geschatte_marge'] * 100
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{marge:.0f}%', ha='center', va='bottom', fontsize=8)
    
    # 2. Top 10 winstgevende producten
    ax2 = axes[0, 1]
    
    if len(df17_product_winst) > 0:
        top10_products = df17_product_winst.head(10)
        
        # Maak productnamen korter
        product_names = []
        for product in top10_products.index:
            if len(product) > 20:
                product_names.append(product[:18] + '...')
            else:
                product_names.append(product)
        
        y_pos = np.arange(len(product_names))
        ax2.barh(y_pos, top10_products['geschatte_winst'], color='goldenrod')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(product_names, fontsize=8)
        ax2.set_xlabel('Geschatte Winst (€)')
        ax2.set_title('Top 10 Meest Winstgevende Producten')
        ax2.grid(axis='x', alpha=0.3)
    
    # 3. Marge vs Volume analyse - GEBRUIK GEÏMPORTEERDE DATA
    ax3 = axes[1, 0]
    
    if len(df17_categorie_data) > 0:
        volumes = df17_categorie_data['totaal_bedrag'].values
        marges = df17_categorie_data['geschatte_marge'].values * 100
        
        # Bubble chart
        colors = plt.cm.viridis(np.linspace(0, 1, len(df17_categorie_data)))
        scatter = ax3.scatter(volumes, marges, s=df17_categorie_data['aantal']/10, 
                            c=colors, alpha=0.6, edgecolors='black')
        
        # Labels
        for i, cat in enumerate(df17_categorie_data.index):
            ax3.annotate(cat, (volumes[i], marges[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax3.set_xlabel('Omzet (€)')
        ax3.set_ylabel('Marge (%)')
        ax3.set_title('Marge vs Volume per Categorie')
        ax3.grid(True, alpha=0.3)
    
    # 4. Winstgevendheid insights
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # GEBRUIK GEÏMPORTEERDE TOTALEN
    
    insights_text = f"""
    WINSTGEVENDHEID INSIGHTS:
    
    Overzicht:
    • Totale omzet: €{df17_totale_omzet:,.0f}
    • Geschatte winst: €{df17_totale_winst:,.0f}
    • Gemiddelde marge: {df17_gem_marge:.1f}%
    
    Beste marges:
    • Delicatessen: 50%
    • Tapas: 45%
    • Brood: 40%
    
    Volume drivers:
    • Kaas: Grootste omzet
    • Vlees: Tweede grootste
    
    Strategieën:
    • Push hoge marge producten
    • Bundle lage/hoge marge items
    • Focus op delicatessen groei
    • Optimaliseer inkoop populaire items
    
    Quick wins:
    • Promoot tapas & delicatessen
    • Verhoog brood attach rate
    • Premium varianten introduceren
    """
    
    ax4.text(0.05, 0.95, insights_text, transform=ax4.transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    return fig

# GF18: Klanten Belonen Matrix
def gf18_klanten_belonen():
    """GF18: Klanten Belonen - gebruik geïmporteerde data"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('GF18: Welke Klanten Belonen?', fontsize=16, fontweight='bold')
    
    # 1. VIP klanten overzicht
    ax1 = axes[0, 0]
    
    if len(df18_vip_klanten) > 0:
        # Top 5 VIP klanten
        top5_vip = df18_vip_klanten.head(5)
        klant_labels = [f"Klant {i+1}" for i in range(len(top5_vip))]
        uitgaven = top5_vip['totale_uitgaven'].values
        
        bars = ax1.bar(klant_labels, uitgaven, color='gold', edgecolor='darkgoldenrod', linewidth=2)
        ax1.set_title('Top 5 VIP Klanten - Totale Uitgaven')
        ax1.set_ylabel('Totale Uitgaven (€)')
        ax1.grid(axis='y', alpha=0.3)
        
        # Voeg bedragen toe
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'€{height:.0f}', ha='center', va='bottom')
    
    # 2. Klant segmenten overzicht
    ax2 = axes[0, 1]
    
    # Tel klanten per segment type
    segment_counts = {
        'VIP': len(df18_vip_klanten),
        'Loyaal': len(df18_loyale_klanten),
        'Frequent': len(df18_frequente_klanten),
        'Rising Stars': len(df18_rising_stars),
        'Te reactiveren': len(df18_te_reactiveren)
    }
    
    segments = list(segment_counts.keys())
    counts = list(segment_counts.values())
    colors = ['gold', 'silver', 'bronze', 'lightgreen', 'lightcoral']
    
    bars2 = ax2.bar(segments, counts, color=colors)
    ax2.set_title('Aantal Klanten per Beloningssegment')
    ax2.set_ylabel('Aantal Klanten')
    ax2.set_xticklabels(segments, rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # Voeg aantallen toe
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                str(int(height)), ha='center', va='bottom')
    
    # 3. Bestelfrequentie rising stars
    ax3 = axes[1, 0]
    
    if len(df18_rising_stars) > 0:
        # Toon ontwikkeling rising stars
        labels = [f"RS {i+1}" for i in range(min(5, len(df18_rising_stars)))]
        orders = df18_rising_stars['aantal_orders'].head(5).values
        dagen = df18_rising_stars['dagen_klant'].head(5).values
        
        # Bereken orders per maand
        orders_per_maand = (orders / (dagen / 30)).round(1)
        
        x = np.arange(len(labels))
        width = 0.35
        
        bars1 = ax3.bar(x - width/2, orders, width, label='Totale orders', color='lightblue')
        bars2 = ax3.bar(x + width/2, orders_per_maand, width, label='Orders/maand', color='darkblue')
        
        ax3.set_xlabel('Rising Stars')
        ax3.set_xticks(x)
        ax3.set_xticklabels(labels)
        ax3.set_title('Rising Stars - Bestelgedrag')
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
    
    # 4. Beloningsstrategieën
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Bereken impact
    totaal_te_belonen = sum(counts[:4])  # Exclusief 'te reactiveren'
    totaal_klanten = df_bestellingen['email_klant'].nunique()
    percentage_belonen = (totaal_te_belonen / totaal_klanten * 100) if totaal_klanten > 0 else 0
    
    strategie_text = f"""
    BELONINGSSTRATEGIEËN:
    
    Te belonen: {totaal_te_belonen} van {totaal_klanten} ({percentage_belonen:.1f}%)
    
    VIP Klanten ({counts[0]}):
    • Exclusieve events & previews
    • Persoonlijke account manager
    • Gratis bezorging altijd
    • Verjaardagscadeau premium
    
    Loyale Klanten ({counts[1]}):
    • 10% loyaliteitskorting
    • Verjaardagsbon €25
    • Vroege toegang nieuwe producten
    
    Frequente Bestellers ({counts[2]}):
    • Volume kortingen (5-15%)
    • Snelle checkout optie
    • Priority levering
    
    Rising Stars ({counts[3]}):
    • Welkomstpakket delicatessen
    • €10 korting na 3e bestelling
    • Persoonlijke productadviezen
    
    ROI: Geschat 3-5x op beloningsinvestering
    """
    
    ax4.text(0.05, 0.95, strategie_text, transform=ax4.transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    plt.tight_layout()
    return fig

# Hoofdfunctie
if __name__ == "__main__":
    print("\n🚀 START VISUALISATIE GENERATIE (GF1 t/m GF18)")
    print("="*60)
    print("📊 ALLE 18 GRAFIEKEN WORDEN GEGENEREERD")
    print("📌 Gebruik de Web UI voor interactieve weergave")
    print("="*60)
    
    # Check of visualisaties map bestaat
    if not os.path.exists('../visualisaties'):
        os.makedirs('../visualisaties')
        print("📁 Map 'visualisaties' aangemaakt")
    
    # Genereer alle visualisaties
    gf1_top_producten_barplot()
    gf2_omzet_tijdlijn()
    gf3_geografische_spreiding()
    gf4_klanten_segmentatie_matrix()
    gf5_bestellingen_heatmap()
    gf6_product_categorie_donut()
    gf7_betaalmethode_analyse()
    gf8_kaas_brood_combinaties()
    gf9_verkooppatronen()
    gf10_prijsevolutie()
    gf11_toekomstvoorspelling()
    gf12_lange_termijn()
    gf13_seizoens_feestdagen()
    gf14_leadtime_analyse()
    gf15_product_combinaties()
    gf16_klant_lifetime_value()
    gf17_winstgevendheid()
    gf18_klanten_belonen()
    
    print("\n" + "="*60)
    print("✅ ALLE VISUALISATIES (GF1 t/m GF18) SUCCESVOL GEGENEREERD!")
    print("📊 Grafieken worden getoond in vensters")
    print("="*60) 