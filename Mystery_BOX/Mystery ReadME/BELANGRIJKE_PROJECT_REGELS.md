# 🚨 BELANGRIJKE PROJECT REGELS - NOOIT MEER VERGISSEN! 🚨

## 📁 PROJECT STRUCTUUR

```
bestellingen_analyse/
├── data/
│   └── Bestellingen.csv (ORIGINELE DATA - NIET AANRAKEN!)
├── scripts/
│   ├── data_cleaning.py (31 regels - haalt data op, maakt df_filtered en df_bestellingen)
│   ├── data_analyse.py (1066 regels - ALLE 18 DF analyses)
│   └── visualisaties.py (visualisaties - IMPORTEERT uit data_analyse!)
├── visualisaties/ (voor eventuele export)
└── rapporten/ (voor rapporten)
```

## ⚠️ FUNDAMENTELE REGELS - ONTHOUD DIT!

### 1. DATA FLOW
```
Bestellingen.csv → data_cleaning.py → data_analyse.py → visualisaties.py
                         ↓                    ↓                ↓
                   (maakt 2 dfs)      (gebruikt dfs,      (importeert 
                                       maakt DF1-18)       DF resultaten)
```

### 2. GEEN DUBBELE CODE!
- ❌ FOUT: Data opnieuw inlezen in visualisaties.py
- ❌ FOUT: DFs opnieuw berekenen in visualisaties.py
- ✅ GOED: Importeer DFs uit data_analyse.py!

### 3. HOE HET WERKT:

#### data_cleaning.py:
```python
def clean_bestellingen_data():
    # Leest Bestellingen.csv
    # Maakt schoon
    return df_filtered, df_bestellingen
```

#### data_analyse.py:
```python
# Gebruikt data_cleaning
df_filtered, df_bestellingen = clean_bestellingen_data()

# Berekent ALLE analyses
df1_top20_alfabetisch = ...
df2_maanden = ...
df3_geo = ...
df4_klanten = ...
# ... tot DF18
```

#### visualisaties.py:
```python
# IMPORTEERT uit data_analyse!
from data_analyse import (
    df1_top20_alfabetisch,
    df2_maanden,
    df3_geo,
    df4_klanten,
    bepaal_categorie
)

# Maakt ALLEEN visualisaties
plt.show()  # GEEN savefig!
```

## 🎯 WAT WE WILLEN:

1. **Data cleaning**: Gebeurt in `data_cleaning.py`
2. **Analyses (DF1-18)**: Gebeuren in `data_analyse.py` 
3. **Visualisaties (GF1-18)**: Gebeuren in `visualisaties.py`
   - GF1 gebruikt DF1
   - GF2 gebruikt DF2
   - etc...

## 🚫 NOOIT MEER DOEN:

1. **Data opnieuw inlezen** in visualisaties.py
2. **DFs opnieuw berekenen** in visualisaties.py
3. **Functies definiëren** voor DFs (ze zijn gewoon variabelen!)
4. **PNG/bestanden opslaan** - gebruik plt.show()
5. **Dubbele imports** of dubbele berekeningen

## ✅ ALTIJD DOEN:

1. **Importeer uit data_analyse.py** wat je nodig hebt
2. **Gebruik plt.show()** voor visualisaties
3. **Keep it simple** - geen overbodige code
4. **Volg de data flow** - cleaning → analyse → visualisatie

## 📊 DF OVERZICHT:

- **DF1**: Top 20 producten (alfabetisch) → `df1_top20_alfabetisch`
- **DF2**: Omzet per maand → `df2_maanden`
- **DF3**: Top 15 woonplaatsen → `df3_geo`
- **DF4**: Klanten segmentatie (RFM) → `df4_klanten`
- **DF5**: Bestellingen per uur → `df5_uren`
- **DF6**: Product categorieën → `df6_categorie`
- **DF7**: Betaalmethoden → `df7_betaal`
- **DF8**: Brood bij kaasschotels → `df8_brood_bij_kaas`
- **DF9**: Verkooppatronen (geen aparte df, print statements)
- **DF10**: Prijsevolutie (gebruikt originele_df)
- **DF11**: Voorspelling 5 jaar (berekeningen)
- **DF12**: Voorspelling 55 jaar (berekeningen)
- **DF13**: Seizoens analyse (maand_omzet)
- **DF14**: Leadtime analyse (berekeningen)
- **DF15**: Product combinaties (berekeningen)
- **DF16**: Customer Lifetime Value (berekeningen)
- **DF17**: Winstgevendheid (berekeningen)
- **DF18**: Klanten belonen (berekeningen)

## 🎨 VISUALISATIES STATUS:

- ✅ GF1: Top 20 producten barplot (horizontaal)
- ✅ GF2: Omzet tijdlijn (lijndiagram)
- ✅ GF3: Geografische spreiding (2 staafdiagrammen)
- ✅ GF4: Klanten segmentatie matrix (scatter plot)
- ⏳ GF5-18: Nog te maken...

## 📝 ONTHOUD:

**"Data cleaning doet het zware werk, data analyse berekent alles, visualisaties toont het mooi!"**

---

*Dit bestand is gemaakt omdat ik steeds dezelfde fouten maakte. Nu kan ik altijd hier kijken hoe het project echt werkt!* 