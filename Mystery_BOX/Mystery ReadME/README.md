# Bestellingen Analyse Project

## Overzicht
Dit project analyseert verkoopdata van een delicatessenzaak gespecialiseerd in kaas- en vleesschotels. Het bevat volledige data cleaning, analyse en visualisatie van 521 bestellingen.

## Project Structuur
```
bestellingen_analyse/
├── data/
│   └── Bestellingen.csv          # Originele dataset
├── scripts/
│   ├── data_cleaning.py          # Data opschoning en voorbereiding
│   ├── data_analyse.py           # 18 dataframes (DF1-DF18) met analyses
│   └── visualisaties.py          # 18 grafieken (GF1-GF18) generatie
├── visualisaties/
│   └── [18 PNG bestanden]        # Gegenereerde grafieken
├── rapporten/
│   └── eindrapport_bestellingen_analyse.md  # Volledig rapport
└── README.md                     # Dit bestand
```

## Installatie

### Vereisten
- Python 3.8+
- Pandas
- Matplotlib
- Seaborn
- NumPy

### Installeer packages:
```bash
pip install pandas matplotlib seaborn numpy
```

## Gebruik

### 1. Data Cleaning
```bash
cd scripts
python data_cleaning.py
```
Dit script:
- Leest de originele CSV
- Standaardiseert woonplaatsen (Tongeren varianten)
- Standaardiseert productnamen
- Creëert twee dataframes: df_filtered (item-niveau) en df_bestellingen (order-niveau)

### 2. Data Analyse
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

### 3. Visualisaties
```bash
python visualisaties.py
```
Dit genereert 18 grafieken (GF1-GF18) in de visualisaties folder.

## Belangrijkste Bevindingen

### Top Inzichten:
1. **Tongeren domineert:** 29.4% van alle omzet
2. **Cross-sell kans:** Slechts 21.9% kaasbestellingen bevat brood
3. **Premium focus:** Gastronomische schotels hebben hoogste marges
4. **Groei potentieel:** Realistische 20% jaarlijkse groei mogelijk

### Aanbevelingen:
1. Implementeer VIP klantenprogramma
2. Versterk brood cross-selling
3. Focus marketing op Tongeren regio
4. Optimaliseer capaciteit voor piekuren (14:00-17:00)

## Data Kwaliteit

### Opgeloste Issues:
- Tongeren/TONGEREN/tongeren → Tongeren
- Kaasschotel varianten gestandaardiseerd
- Prijzen per persoon correct berekend

### Bekende Beperkingen:
- Geen sociale media data beschikbaar
- Winstmarges zijn schattingen
- Seizoensdata beperkt tot beschikbare jaren

## Contact
Voor vragen over deze analyse, raadpleeg het eindrapport in de rapporten folder.

---
*Project gemaakt voor proefexamen data analyse* 