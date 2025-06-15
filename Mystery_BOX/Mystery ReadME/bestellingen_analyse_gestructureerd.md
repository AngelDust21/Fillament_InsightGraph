# Mystery Box - Bestellingen Analyse Project

## PROJECT STRUCTUUR (ACTUEEL)
```
Mystery_BOX/
├── Mystery ReadME/
│   ├── data/
│   │   └── Bestellingen.csv (originele data)
│   ├── scripts/
│   │   ├── data_cleaning.py (114 regels - data opschoning)
│   │   ├── data_analyse.py (1197 regels - alle 18 DF analyses)
│   │   ├── visualisaties.py (1598 regels - alle 18 visualisaties)
│   │   └── streamlit_app.py (197 regels - web dashboard)
│   ├── rapporten/
│   │   ├── eindrapport_bestellingen_analyse.md
│   │   └── social_media_strategie.md
│   ├── start_web_ui.bat (start script)
│   ├── requirements.txt (dependencies)
│   └── README bestanden (deze documentatie)
```

## FASE 1: DATA CLEANING ✅ VOLTOOID

### Script: `data_cleaning.py` (114 regels)
- **Functie**: `clean_bestellingen_data()`
- **Kolommen geselecteerd**: 15 relevante kolommen
- **Hernoemd naar Nederlandse namen**: bestelnummer, besteldatum, email_klant, etc.
- **Data types geconverteerd**: datetime, float, integer
- **Stadsnamen gestandaardiseerd**: .str.title() voor consistentie
- **Output**: 
  - `df_filtered`: item-niveau data (alle regels)
  - `df_bestellingen`: order-niveau data (gegroepeerd per bestelnummer)

## FASE 2: ANALYSE ✅ ALLE 18 DF's VOLTOOID

### Script: `data_analyse.py` (1197 regels)

### DF1: TOP 20 PRODUCTEN ANALYSE (ALFABETISCH)
- Berekent juiste totale omzet per product (aantal × prijs)
- Selecteert top 20 op basis van omzet
- Sorteert alfabetisch voor overzicht
- Toont: aantal verkocht, gem. prijs, keer besteld, totale omzet
- **→ Visualisatie: GF1**

### DF2: OMZET PER MAAND
- Groepeert per maand (alle jaren)
- Toont: totale omzet, aantal bestellingen, gem. bestelwaarde
- Gebruikt periode format voor correcte sortering
- **→ Visualisatie: GF2**

### DF3: TOP 15 WOONPLAATSEN
- Analyseert geografische spreiding
- Toont: unieke klanten, totale omzet, gem. bestelwaarde, percentage
- Tongeren domineert met 21.5% van omzet
- **→ Visualisatie: GF3**

### DF4: KLANTEN SEGMENTATIE (RFM)
- Segmenteert klanten in: VIP, Regelmatig, Nieuw, Slapend
- Gebaseerd op Recency, Frequency, Monetary waarden
- 299 slapende klanten geïdentificeerd (opportunity)
- **→ Visualisatie: GF4**

### DF5: BESTELLINGEN PER UUR
- Analyseert dagpatronen
- Piekuren: 14:00-17:00
- Basis voor operationele planning
- **→ Visualisatie: GF5**

### DF6: PRODUCT CATEGORIEËN
- Uitgebreide categorisatie: Kaas, Vlees, Brood, Tapas, Delicatessen, Overig
- Percentage van totale omzet per categorie
- Cross-selling opportunities
- **→ Visualisatie: GF6**

### DF7: BETAALMETHODEN
- Stripe meest populair
- Analyseert gem. bestelwaarde per methode
- Correlatie met bestelgrootte
- **→ Visualisatie: GF7**

### DF8: BROOD BIJ KAASSCHOTELS
- 16.8% van kaasbestellingen bevat ook brood
- Top broodsoorten bij kaas geïdentificeerd
- Bundel mogelijkheden
- **→ Visualisatie: GF8**

### DF9: VERKOOPPATRONEN UIT DATA
- Wanneer bestellen klanten (per dag/uur)
- Seizoenspatronen per maand
- Geen social media aannames - alleen verkoopdata
- **→ Visualisatie: GF9**

### DF10: PRIJSEVOLUTIE KAAS/VLEES (PER PERSOON)
- Analyseert prijzen per persoon (niet per schotel)
- Kaasschotels: €15-25 per persoon
- Vleesschotels: €15-27 per persoon
- Jaarlijkse prijsstijging berekend
- **→ Visualisatie: GF10**

### DF11: VOORSPELLING KOMENDE 5 JAAR
- Twee modellen:
  1. Historisch (56.5% constante groei) → €18,642 in 2030
  2. Realistisch (afvlakkende groei) → €5,179 in 2030
- Gedetailleerde groei per jaar met controle berekening
- Prijzen per persoon voorspelling
- **→ Visualisatie: GF11**

### DF12: LANGE TERMIJN VOORSPELLING (55 JAAR)
- Focus op Gastronomische schotels (€25/€27 per persoon nu)
- Drie scenario's: Pessimistisch, Realistisch, Optimistisch
- 2080 voorspelling: €200-500 per persoon (nominaal)
- Inflatie gecorrigeerd: €70-200 in 2025 euro's
- **→ Visualisatie: GF12**

### DF13: SEIZOENS & FEESTDAGEN ANALYSE
- Piekmaanden geïdentificeerd
- Feestdagen impact (Kerst, Pasen, Communies)
- April hoogste omzet (€4036)
- **→ Visualisatie: GF13**

### DF14: BESTEL LEADTIME ANALYSE
- Meeste klanten bestellen 2-3 dagen vooruit
- Weekend leveringen vereisen langere leadtime
- Verschil per producttype
- **→ Visualisatie: GF14**

### DF15: PRODUCT COMBINATIE ANALYSE (CROSS-SELLING)
- Top 15 product combinaties
- Categorie combinaties (Kaas + Brood meest populair)
- Bundel opportunities
- **→ Visualisatie: GF15**

### DF16: KLANT LIFETIME VALUE
- Diamond/Gold/Silver/Bronze segmenten
- 3-jaar LTV voorspelling
- Cohort retentie analyse
- 80/20 regel bevestigd
- **→ Visualisatie: GF16**

### DF17: WINSTGEVENDHEID ANALYSE
- Geschatte marges per categorie (30-50%)
- Top 10 meest winstgevende producten
- Delicatessen hoogste marge (50%)
- **→ Visualisatie: GF17**

### DF18: WELKE KLANTEN BELONEN
- 5 groepen geïdentificeerd:
  1. VIP klanten (top 10% uitgaven)
  2. Loyale klanten (>2 jaar actief)
  3. Frequente bestellers (>6x per jaar)
  4. Rising Stars (nieuwe hoge uitgaven)
  5. Te reactiveren (waardevolle inactieven)
- Concrete beloningssuggesties per groep
- **→ Visualisatie: GF18**

## FASE 3: VISUALISATIES 🔄 VOLGENDE STAP (18 GF's)

### GF1: Top 20 Producten Barplot (voor DF1)
- Horizontale staafdiagram met top 20 producten
- Gesorteerd alfabetisch
- Kleurcodering per categorie
- Labels met exacte omzet bedragen

### GF2: Omzet Tijdlijn (voor DF2)
- Lijndiagram met maandelijkse omzet
- X-as: Maanden/Jaren
- Y-as: Totale omzet
- Markeer feestdagen en trendlijn

### GF3: Geografische Spreiding (voor DF3)
- Staafdiagram of kaart van België
- Top 15 woonplaatsen
- Grootte = omzet
- Hover info met details

### GF4: Klanten Segmentatie Matrix (voor DF4)
- Scatter plot: Frequency vs Monetary
- Kleur = Recency (recent=groen, oud=rood)
- Kwadrant labels voor segmenten
- Bubble size = gem. bestelwaarde

### GF5: Bestellingen Heatmap (voor DF5)
- Heatmap: Uur vs Dag van de week
- Kleurintensiteit = aantal bestellingen
- Piekuren duidelijk zichtbaar
- Annotaties met exacte aantallen

### GF6: Product Categorie Donut (voor DF6)
- Donut diagram met categorieën
- Percentages van totale omzet
- Interactieve tooltips
- Mooie kleurcoding

### GF7: Betaalmethode Analyse (voor DF7)
- Staafdiagram: methodes vs omzet
- Box plot voor bestelwaarde distributie
- Toon mediaan en outliers
- Vergelijk gem. bestelwaarde

### GF8: Kaas+Brood Combinaties (voor DF8)
- Sankey diagram of stacked bar
- Toon % kaasbestellingen met/zonder brood
- Top broodsoorten bij kaas
- Cross-sell opportunity visualisatie

### GF9: Verkooppatronen Dashboard (voor DF9)
- Multi-panel visualisatie:
  - Lijn: verkoop per weekdag
  - Heatmap: uur vs maand
  - Bar: seizoenspatronen

### GF10: Prijsevolutie Lijnen (voor DF10)
- Dual-axis lijndiagram
- Kaasprijzen en vleesprijzen per persoon
- Trendlijnen met voorspelling
- Min/max ranges

### GF11: 5-Jaar Voorspelling (voor DF11)
- Lijndiagram met 2 scenario's
- Historisch vs Realistisch model
- Confidence intervals
- Jaar labels met bedragen

### GF12: 55-Jaar Scenario's (voor DF12)
- Multi-lijn voorspelling
- 3 scenario's (pessimistisch/realistisch/optimistisch)
- Nominaal én inflatie-gecorrigeerd
- Milestone jaren gemarkeerd

### GF13: Seizoens & Feestdagen (voor DF13)
- Combinatie grafiek:
  - Staaf: omzet per maand
  - Markeer feestdagen
  - Jaar-over-jaar vergelijking

### GF14: Leadtime Distributie (voor DF14)
- Histogram van leadtimes
- Aparte curves voor weekend/weekdag
- Producttype verschillen
- Cumulatief percentage lijn

### GF15: Product Combinatie Network (voor DF15)
- Network diagram of chord diagram
- Verbindingen tussen producten
- Dikte = frequentie
- Top 15 combinaties highlighted

### GF16: Customer Lifetime Value (voor DF16)
- Multi-panel:
  - Piramide: klant segmenten
  - Lijn: cohort retentie
  - Bar: LTV per segment
  - 80/20 curve

### GF17: Winstgevendheid Matrix (voor DF17)
- Bubble chart: omzet vs marge%
- Bubble size = volume
- Kleur per categorie
- Top 10 gelabeld

### GF18: Beloningsgroepen Visualisatie (voor DF18)
- Radar chart per klantsegment
- 5 dimensies: waarde, frequentie, loyaliteit, groei, recency
- Overlay alle 5 groepen
- Actie suggesties per groep

## BELANGRIJKSTE BEVINDINGEN

1. **Producten**: Kaasschotel 'culinair' Hoofdgerecht is topproduct (€9,379 omzet)
2. **Geografie**: Tongeren domineert met 21.5% van totale omzet
3. **Klanten**: 299 slapende klanten (78.5%) - grote reactivatie opportunity
4. **Timing**: Piekuren 14:00-17:00, dinsdag hoogste omzet dag
5. **Groei**: 56.5% historische groei, maar realistisch 12-35% verwacht
6. **Prijzen**: Gastronomische schotels €25-27 pp, stijgen naar €200+ in 2080
7. **Cross-sell**: Slechts 16.8% koopt kaas+brood combo
8. **Seizoen**: April hoogste maand, feestdagen cruciaal

## AANBEVELINGEN

1. **Reactivatie campagne** voor 299 slapende klanten
2. **Kaas+brood bundels** promoten (83.2% mist deze combo)
3. **Capaciteit uitbreiden** voor 14:00-17:00 piekuren
4. **Tongeren focus** voor marketing (21.5% omzet)
5. **Beloningsprogramma** voor 5 klantsegmenten
6. **Feestdagen planning** voor piekperiodes
7. **Prijsstrategie** voor lange termijn groei

## STATUS
- ✅ Fase 1: Data Cleaning - VOLTOOID
- ✅ Fase 2: Analyse (18 DF's) - VOLTOOID
- 🔄 Fase 3: Visualisaties (18 GF's) - KLAAR OM TE STARTEN
- ⏸️ Fase 4: Dashboard - GEPLAND
- ⏸️ Fase 5: Export & Rapportage - GEPLAND 