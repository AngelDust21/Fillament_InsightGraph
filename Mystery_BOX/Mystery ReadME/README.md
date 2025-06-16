# Mystery Box - Bestellingen Analyse Project 🧀📊

## Overzicht
Dit project analyseert verkoopdata van een delicatessenzaak gespecialiseerd in kaas- en vleesschotels. Het bevat volledige data cleaning, analyse en visualisatie van 521 bestellingen met een interactief web dashboard.

> "There are only two hard things in Computer Science: cache invalidation and naming things... and off-by-one errors." - En wij voegden toe: kaasschotels categoriseren!

## Project Structuur (ACTUEEL)
```
Mystery_BOX/
└── Mystery ReadME/
    ├── data/
    │   └── Bestellingen.csv                    # Originele dataset
    ├── scripts/
    │   ├── data_cleaning.py                    # Data opschoning (114 regels)
    │   ├── data_analyse.py                     # 18 dataframes analyses (1197 regels)
    │   ├── visualisaties.py                    # 18 grafieken generatie (1683 regels)
    │   ├── streamlit_app.py                    # Web dashboard (347 regels)
    │   ├── code_uitleg.py                      # Code documentatie (1183 regels)
    │   └── grafiek_uitleg.py                   # Grafiek documentatie (698 regels)
    ├── rapporten/
    │   ├── eindrapport_bestellingen_analyse.md
    │   └── social_media_strategie.md
    ├── README.md                               # Dit bestand (met easter eggs!)
    ├── bestellingen_analyse_uitgebreid.md      # Uitgebreide code documentatie
    ├── PROJECT_DOCUMENTATIE.md                 # Project overzicht
    └── start_web_ui.bat                        # Start script voor dashboard
```

## Installatie

### Vereisten
- Python 3.8+ (3.7 werkt ook maar ssst... 🤫)
- Alle dependencies: pandas, streamlit, matplotlib, seaborn, plotly
- Een gezonde liefde voor kaas (optioneel maar aanbevolen)
- Koffie ☕ (verplicht voor debugging)

### Installeer packages:
```bash
# Installeer de benodigde packages:
pip install pandas streamlit matplotlib seaborn plotly

# Of voor de avonturiers (zonder requirements.txt):
pip install pandas==2.* streamlit matplotlib seaborn plotly
# *Exacte versie maakt niet uit, net als de hoeveelheid kaas op je boterham

# Als het niet werkt, probeer:
# 1. Heb je het uit- en weer aangezet?
# 2. Is het een PEBKAC probleem?
# 3. Check for ID10T errors in je terminal
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
- Leest de originele CSV (zonder segfaults, beloofd!)
- Standaardiseert woonplaatsen (Tongeren/TONGEREN/tongeren → Tongeren)
- Standaardiseert productnamen (nee, "kaas" en "Kaas" zijn NIET hetzelfde)
- Creëert twee dataframes: df_filtered (item-niveau) en df_bestellingen (order-niveau)
- Werkt 60% van de tijd, elke keer! 😎

#### Data Analyse
```bash
python data_analyse.py
```
Dit genereert 18 dataframes (DF1-DF18):
- DF1: Top 20 producten (eigenlijk 19, maar wie telt er nou? 🤷)
- DF2: Maandelijkse omzet
- DF3: Geografische analyse
- DF4: Klant segmentatie (geen regex gebruikt, ik zweer het!)
- DF5: Uurpatronen
- DF6: Product categorieën
- DF7: Betaalmethoden (helaas geen "exposure" of "likes" geaccepteerd)
- DF8: Brood bij kaas analyse (spoiler: 404 - Brood Not Found)
- DF9: Verkooppatronen
- DF10: Prijsevolutie
- DF11: 5-jaar voorspelling (gemaakt met een kristallen bol... eh, machine learning)
- DF12: 2080 prijsvoorspelling (Y2K80 compatible!)
- DF13: Seizoensanalyse
- DF14: Leadtime analyse (gemeten in koffie-cups)
- DF15: Product combinaties
- DF16: Klant lifetime value
- DF17: Winstgevendheid ($$$ → €€€)
- DF18: Klanten belonen

> "99 bugs in the code, 99 bugs in the code. Take one down, patch it around, 117 bugs in the code..." 🐛

#### Visualisaties
```bash
python visualisaties.py
```
Dit genereert 18 grafieken (GF1-GF18) die getoond worden met plt.show().

## Belangrijkste Bevindingen

### Top Inzichten:
1. **Tongeren domineert:** 21.5% van alle omzet (the other 78.5% is just noise)
2. **Cross-sell kans:** Slechts 16.8% kaasbestellingen bevat brood (NullBreadException)
3. **Premium focus:** Gastronomische schotels hebben hoogste marges (correlation ≠ causation, maar €€€ = €€€)
4. **Groei potentieel:** Historisch 56.5% groei, realistisch 12-35% verwacht
5. **Hidden insight:** Als je alle productnamen achterstevoren leest om 3:14 AM, verschijnt er een geheime korting (disclaimer: werkt alleen op Pi-day)

### Aanbevelingen:
1. Implementeer VIP klantenprogramma voor 5 klantsegmenten (of 4.99 na floating point errors)
2. Versterk brood cross-selling (83.2% mist deze combo) - `if (kaas && !brood) { alert("U vergeet iets!"); }`
3. Focus marketing op Tongeren regio (ping: 2ms, perfecte latency voor kaaslevering)
4. Optimaliseer capaciteit voor piekuren (14:00-17:00) - aka "post-lunch cheese cravings"
5. Reactivatie campagne voor 299 slapende klanten (`SELECT * FROM customers WHERE last_order < NOW() - INTERVAL '1 YEAR' AND cheese_love = TRUE;`)
6. **BONUS:** Implementeer blockchain voor kaas-traceability (just kidding... of toch niet? 🤔)

## Data Kwaliteit

### Opgeloste Issues:
- Tongeren/TONGEREN/tongeren → Tongeren
- Kaasschotel varianten gestandaardiseerd
- Prijzen per persoon correct berekend

### Bekende Beperkingen:
- Geen sociale media data beschikbaar (LinkedIn kaasinfluencers tellen niet mee)
- Winstmarges zijn schattingen (30-50% ± een random.randint())
- Seizoensdata beperkt tot beschikbare jaren (time travel module nog in beta)
- Kan geen koffie zetten (grootste tekortkoming IMO)
- RTFM not included (Read The Fabulous Manual)
- Werkt niet op Internet Explorer (feature, niet een bug)

## Contact
Voor vragen over deze analyse, raadpleeg het eindrapport in de rapporten folder.

Voor technische problemen:
1. Check eerst of het een Layer 8 probleem is
2. Probeer `sudo make me a sandwich`
3. Als alles faalt: blame the intern

## Easter Egg Hunt 🥚
Er zijn precies 8 easter eggs verstopt in deze codebase:
- [ ] De 42 referentie
- [ ] Het ID10T probleem
- [ ] De NullBreadException
- [ ] Het PEBKAC mysterie
- [ ] De 404 grap
- [ ] De Pi-day korting
- [ ] De "off-by-one" error
- [ ] Deze lijst heeft er eigenlijk 9... of toch 7? 🤔

---
*Mystery Box Project - Data Analyse & Visualisatie*
*"It's not a bug, it's a cheese feature!"* 🧀

<!-- 
Gefeliciteerd! Je hebt de geheime developer notes gevonden!
Leuk weetje: Deze hele analyse is geschreven op een dieet van:
- 47 koppen koffie
- 12 kaasbroodjes (ironisch genoeg ZONDER kaasschotel)
- 1 rubber duck voor debugging
- ∞ Stack Overflow tabs

P.S. Als je dit in productie zet, verander dan alsjeblieft de wachtwoorden.
Ja, ook "admin123" en "kaas4life". Vooral die laatste.

"There is no cloud, it's just someone else's cheese server" 
--> 