# 📊 Delicatessenzaak Data Analyse Project

## 🎯 Project Overzicht

Dit project bevat een uitgebreide data-analyse suite voor een delicatessenzaak, met 18 verschillende analyses (DF1-DF18) die inzicht geven in verkoop, klantgedrag, en bedrijfsprestaties.

## 📁 Project Structuur

```
Mystery_BOX/
│
├── Mystery ReadME/
│   ├── scripts/
│   │   ├── data_cleaning.py      # Data voorbereiding en opschoning
│   │   ├── data_analyse.py       # Alle 18 analyses (DF1-DF18)
│   │   ├── visualisaties.py      # Grafische weergave (GF1-GF18)
│   │   ├── streamlit_app.py      # Web UI applicatie
│   │   ├── code_uitleg.py        # Code documentatie en uitleg
│   │   └── grafiek_uitleg.py     # Grafiek interpretatie gids
│   │
│   ├── data/
│   │   └── Bestellingen.csv      # Bron data
│   │
│   ├── rapporten/
│   │   └── [gegenereerde rapporten]
│   │
│   └── requirements.txt          # Python dependencies
```

## 🔧 Installatie & Setup

1. **Vereisten:**
   - Python 3.8 of hoger
   - pip package manager

2. **Installatie:**
   ```bash
   cd "Mystery_BOX/Mystery ReadME"
   pip install -r requirements.txt
   ```

3. **Starten:**
   ```bash
   # Windows:
   start_web_ui.bat
   
   # Of direct:
   streamlit run scripts/streamlit_app.py
   ```

## 📊 Overzicht Analyses

### Basis Analyses (DF1-DF4)
- **DF1: Top 20 Producten** - Identificeert bestsellers op basis van omzet
- **DF2: Omzet Tijdlijn** - Toont maandelijkse omzettrends met voortschrijdend gemiddelde
- **DF3: Geografische Spreiding** - Analyseert klantenverdeling per locatie
- **DF4: Klanten Segmentatie** - RFM analyse voor klantwaarde bepaling

### Operationele Inzichten (DF5-DF8)
- **DF5: Bestellingen Heatmap** - Visualiseert drukte per dag en uur
- **DF6: Product Categorieën** - Categoriseert en analyseert productgroepen
- **DF7: Betaalmethoden** - Vergelijkt verschillende betaalmethoden
- **DF8: Kaas + Brood Combinaties** - Specifieke combi-analyse

### Geavanceerde Analyses (DF9-DF12)
- **DF9: Verkooppatronen** - Identificeert terugkerende patronen
- **DF10: Prijsevolutie** - Analyseert prijsontwikkeling en inflatie
- **DF11: Toekomstvoorspelling** - 12-maanden omzetvoorspelling
- **DF12: Lange Termijn** - 55-jaar voorspelling met scenario's

### Marketing & Strategie (DF13-DF15)
- **DF13: Seizoens & Feestdagen** - Impact van seizoenen en feestdagen
- **DF14: Bestelpatronen** - Lead time en bestelfrequentie analyse
- **DF15: Cross-selling** - Market basket analyse voor productcombinaties

### Klant & Winst Analyses (DF16-DF18)
- **DF16: Customer Lifetime Value** - Berekent klantwaarde over tijd
- **DF17: Winstgevendheid** - Analyseert winstmarges per categorie
- **DF18: Loyaliteitsprogramma** - Segmenteert klanten voor beloningen

## 💻 Web UI Features

### Hoofdfuncties:
- **Interactieve Dashboard** - Navigeer door alle 18 analyses
- **Visualisaties** - Professionele grafieken voor elke analyse
- **Download Functie** - Export grafieken als PNG (300 DPI)
- **Code Uitleg** - Bekijk de onderliggende code en formules
- **Real-time Stats** - KPI's in de sidebar

### Nieuwe Uitleg Features:

#### 🎓 Grafiek Uitleg Knop:
Bij elke visualisatie een speciale knop die toont:
- **Wat zie je?** - Beschrijving van grafiek elementen
- **Hoe lees je dit?** - Stap-voor-stap leeswijzer
- **Wat betekent dit?** - Business interpretatie
- **Conclusies & Acties** - Concrete vervolgstappen

#### 💻 Code Uitleg Sectie:
- Gedetailleerde uitleg van gebruikte formules
- Zakelijke rechtvaardiging voor elke analyse
- Algemene concepten uitleg (Pandas, Visualisaties, BI)
- Side-by-side code en uitleg weergave

## 📈 Belangrijkste Formules

### RFM Score (DF4):
```python
Recency = (today - laatste_besteldatum).days
Frequency = aantal_bestellingen
Monetary = totale_uitgaven
```

### Customer Lifetime Value (DF16):
```python
CLV = Gem_Orderwaarde × Aankoopfrequentie × Klantenlevensduur
```

### ROI Berekening (DF17):
```python
ROI = (Winst / Kosten) × 100
```

## 🎯 Business Intelligence Inzichten

### Top KPI's:
1. **Totale Omzet**: Som van alle bestellingen
2. **Gemiddelde Orderwaarde**: Omzet / Aantal orders
3. **Klantretentie**: % klanten die terugkomen
4. **Product Mix**: Verdeling over categorieën
5. **Geografische Dekking**: Spreiding van klanten

### Strategische Aanbevelingen:
- Focus op top 20% producten (80/20 regel)
- Optimaliseer voorraad op basis van seizoenspatronen
- Implementeer dynamische pricing voor maximale winstgevendheid
- Gebruik cross-selling inzichten voor productplaatsing
- Beloon loyale klanten op basis van CLV

## 🛠️ Technische Details

### Gebruikte Technologieën:
- **Python 3.8+**: Hoofdprogrammeertaal
- **Pandas**: Data manipulatie en analyse
- **NumPy**: Numerieke berekeningen
- **Matplotlib/Seaborn**: Visualisaties
- **Streamlit**: Web UI framework
- **Scikit-learn**: Machine learning voor voorspellingen

### Data Pipeline:
1. **Cleaning** (`data_cleaning.py`):
   - Datum parsing
   - Missing values handling
   - Data type conversies
   - Outlier detectie

2. **Analyse** (`data_analyse.py`):
   - 18 gestructureerde analyses
   - Herbruikbare functies
   - Geoptimaliseerde berekeningen

3. **Visualisatie** (`visualisaties.py`):
   - Consistente styling
   - Interactieve elementen
   - Export-ready kwaliteit

4. **Presentatie** (`streamlit_app.py`):
   - Gebruiksvriendelijke interface
   - Real-time updates
   - Responsive design

## 📝 Onderhoud & Updates

### Dagelijks:
- Check data kwaliteit
- Monitor performance metrics

### Wekelijks:
- Update voorspellingen
- Analyseer nieuwe trends

### Maandelijks:
- Evalueer KPI targets
- Pas segmentaties aan
- Update documentatie

### Jaarlijks:
- Herzie winstmarges
- Update inflatie parameters
- Evalueer loyaliteitsprogramma

## 🚀 Toekomstige Uitbreidingen

1. **Real-time Integratie**
   - Koppeling met kassasysteem
   - Live dashboard updates

2. **Geavanceerde Analytics**
   - A/B testing framework
   - Sentiment analyse reviews
   - Voorspellende voorraad optimalisatie

3. **Automatisering**
   - Geautomatiseerde rapporten
   - Alert systeem voor anomalieën
   - Automatische prijsoptimalisatie

4. **Machine Learning**
   - Churn predictie
   - Recommendation engine
   - Demand forecasting

## 📞 Contact & Support

Voor vragen of ondersteuning:
- Bekijk de inline documentatie in de code
- Gebruik de Code Uitleg sectie in de Web UI
- Raadpleeg de README bestanden

---

**Laatste Update**: December 2024
**Versie**: 1.0
**Status**: Production Ready 