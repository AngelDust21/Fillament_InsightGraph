# Mystery Box - Bestellingen Analyse Project

## Overzicht
Dit project analyseert verkoopdata van een delicatessenzaak gespecialiseerd in kaas- en vleesschotels. Het bevat volledige data cleaning, analyse en visualisatie van 521 bestellingen met een interactief web dashboard.

## Project Structuur (ACTUEEL)
```
Mystery_BOX/
└── Mystery ReadME/
    ├── data/
    │   └── Bestellingen.csv          # Originele dataset
    ├── scripts/
    │   ├── data_cleaning.py          # Data opschoning (114 regels)
    │   ├── data_analyse.py           # 18 dataframes analyses (1197 regels)
    │   ├── visualisaties.py          # 18 grafieken generatie (1598 regels)
    │   └── streamlit_app.py          # Web dashboard (197 regels)
    ├── rapporten/
    │   ├── eindrapport_bestellingen_analyse.md
    │   └── social_media_strategie.md
    ├── start_web_ui.bat              # Start script voor dashboard
    ├── requirements.txt              # Python dependencies
    └── README bestanden              # Documentatie
```

## Installatie

### Vereisten
- Python 3.8+
- Alle dependencies in requirements.txt

### Installeer packages:
```bash
cd "Mystery_BOX/Mystery ReadME"
pip install -r requirements.txt
```

## Gebruik

### 1. Web Dashboard (AANBEVOLEN)
```bash
# Vanuit Mystery ReadME map:
start_web_ui.bat

# Of handmatig:
cd scripts
streamlit run streamlit_app.py
```

### 2. Losse Scripts Draaien

#### Data Cleaning
```bash
cd scripts
python data_cleaning.py
```
Dit script:
- Leest de originele CSV
- Standaardiseert woonplaatsen (Tongeren varianten)
- Standaardiseert productnamen
- Creëert twee dataframes: df_filtered (item-niveau) en df_bestellingen (order-niveau)

#### Data Analyse
```bash
python data_analyse.py
```
Dit genereert 18 dataframes (DF1-DF18):
- DF1: Top 20 producten
- DF2: Maandelijkse omzet
- DF3: Geografische analyse
- DF4: Klant segmentatie
- DF5: Uurpatronen
- DF6: Product categorieën
- DF7: Betaalmethoden
- DF8: Brood bij kaas analyse
- DF9: Verkooppatronen
- DF10: Prijsevolutie
- DF11: 5-jaar voorspelling
- DF12: 2080 prijsvoorspelling
- DF13: Seizoensanalyse
- DF14: Leadtime analyse
- DF15: Product combinaties
- DF16: Klant lifetime value
- DF17: Winstgevendheid
- DF18: Klanten belonen

#### Visualisaties
```bash
python visualisaties.py
```
Dit genereert 18 grafieken (GF1-GF18) die getoond worden met plt.show().

## Belangrijkste Bevindingen

### Top Inzichten:
1. **Tongeren domineert:** 21.5% van alle omzet
2. **Cross-sell kans:** Slechts 16.8% kaasbestellingen bevat brood
3. **Premium focus:** Gastronomische schotels hebben hoogste marges
4. **Groei potentieel:** Historisch 56.5% groei, realistisch 12-35% verwacht

### Aanbevelingen:
1. Implementeer VIP klantenprogramma voor 5 klantsegmenten
2. Versterk brood cross-selling (83.2% mist deze combo)
3. Focus marketing op Tongeren regio
4. Optimaliseer capaciteit voor piekuren (14:00-17:00)
5. Reactivatie campagne voor 299 slapende klanten

## Data Kwaliteit

### Opgeloste Issues:
- Tongeren/TONGEREN/tongeren → Tongeren
- Kaasschotel varianten gestandaardiseerd
- Prijzen per persoon correct berekend

### Bekende Beperkingen:
- Geen sociale media data beschikbaar
- Winstmarges zijn schattingen (30-50%)
- Seizoensdata beperkt tot beschikbare jaren

## Contact
Voor vragen over deze analyse, raadpleeg het eindrapport in de rapporten folder.

---
*Mystery Box Project - Data Analyse & Visualisatie* 