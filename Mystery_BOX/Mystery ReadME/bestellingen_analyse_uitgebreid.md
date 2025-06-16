# Mystery Box - Uitgebreide Code Documentatie & Analyse Uitleg

> 📚 **Dit document bevat gedetailleerde uitleg over WAAROM de code zo geschreven is en WAT alle begrippen betekenen**
> 
> 🎯 **Doel**: Begrijp niet alleen WAT de code doet, maar vooral WAAROM bepaalde keuzes zijn gemaakt

## 📋 Inhoudsopgave

1. [Functie Index & Overzicht](#functie-index--overzicht)
2. [Python & Pandas Basics](#python--pandas-basics)
3. [Groeperen & Aggregeren](#groeperen--aggregeren)
4. [Data Cleaning & Voorbereiding](#data-cleaning--voorbereiding)
5. [18 Gedetailleerde Analyses (DF1-DF18)](#gedetailleerde-analyses)
6. [Data Visualisatie Keuzes](#data-visualisatie-keuzes)
7. [Conclusies & Aanbevelingen](#conclusies--aanbevelingen)

---

## 📊 Functie Index & Overzicht

### Overzicht van alle gebruikte Python/Pandas functies

**Data Manipulatie:**
```python
df.groupby()         # Groepeer data op kolom(men)
df.agg()            # Voer meerdere berekeningen uit
df.pivot_table()    # Maak kruistabel van data
df.merge()          # Combineer twee DataFrames
df.sort_values()    # Sorteer op waarde
df.nlargest()       # Selecteer N grootste waarden
```

**Selectie & Filtering:**
```python
df[df['kolom'] > waarde]     # Filter rijen op conditie
df['kolom']                  # Selecteer één kolom
df.loc[]                     # Selecteer op label
df.iloc[]                    # Selecteer op positie
df.isin()                    # Check of waarde in lijst zit
```

**Berekeningen:**
```python
.sum()              # Optellen
.mean()             # Gemiddelde
.count()            # Aantal (niet-lege) waarden
.nunique()          # Aantal unieke waarden
.value_counts()     # Tel frequentie per waarde
.rolling()          # Voortschrijdend gemiddelde
```

**Datum/Tijd functies:**
```python
df['datum'].dt.year          # Haal jaar uit datum
df['datum'].dt.month         # Haal maand uit datum
df['datum'].dt.day_name()    # Dag als tekst (Monday...)
df['datum'].dt.to_period()   # Converteer naar periode
```

**Transformaties:**
```python
pd.qcut()           # Verdeel in quantiles (gelijke groepen)
pd.cut()            # Verdeel in bins (vaste grenzen)
.apply()            # Pas functie toe op elke rij/kolom
.map()              # Vervang waarden volgens mapping
.rename()           # Hernoem kolommen
```

**Visualisatie helpers:**
```python
.round()            # Afronden op decimalen
.fillna()           # Vul lege waarden
.dropna()           # Verwijder lege waarden
.reset_index()      # Reset de index
.set_index()        # Maak kolom de index
```

### 🎯 Waarom deze functies?
- **groupby + agg**: Kern van data aggregatie
- **pivot_table**: Voor 2D overzichten (heatmaps)
- **dt accessor**: Werken met datums
- **value_counts**: Snel frequenties tellen
- **nlargest**: Top N selecteren

---

## 🐍 Python & Pandas Basics

### 🎯 Waarom Python en Pandas voor data analyse?

**Pandas DataFrame - Onze digitale spreadsheet**
- Een DataFrame is als een Excel tabel in Python
- **Waarom?** Kan miljoenen rijen aan, Excel max 1 miljoen
- Elke kolom heeft een naam en datatype

**Belangrijkste DataFrame functies:**
```python
df['kolom']              # Selecteer één kolom
df[df['prijs'] > 10]     # Filter rijen (alleen prijs > 10)
df.groupby('categorie')  # Groepeer op categorie
df.sort_values('omzet')  # Sorteer op omzet
df.head(10)              # Bekijk eerste 10 rijen
```

**Waarom deze keuzes:**
1. **groupby()**: Om van details naar totalen te gaan
   - Voorbeeld: 1000 losse verkopen → totaal per product
2. **agg()**: Om meerdere berekeningen tegelijk te doen
   - Som, gemiddelde, aantal in één keer
3. **merge()**: Om tabellen te combineren
   - Zoals VLOOKUP in Excel maar krachtiger

### 💡 Veelgebruikte begrippen:
- **Index**: De rijnummers (of productnamen als index)
- **Series**: Één kolom uit een DataFrame
- **NaN**: Not a Number - lege waarde (of: "Nog aan Niks gedacht" 😉)
- **dtype**: Data type (tekst, getal, datum)
- **42**: Het antwoord op alles... inclusief hoeveel kaassoorten we eigenlijk verkopen

---

## 📊 Groeperen & Aggregeren

### 🎯 Waarom groeperen we data?

**Het probleem:**
- Je hebt 10.000 losse verkoopregels
- Je wilt weten: hoeveel verkocht per product?

**De oplossing - groupby():**
```python
# Van dit (10.000 regels):
# Product  | Aantal | Prijs
# Kaas     | 2      | 20
# Brood    | 1      | 3
# Kaas     | 3      | 30
# ...

# Naar dit (50 producten):
df.groupby('product').agg({
    'aantal': 'sum',      # Tel alle aantallen op
    'prijs': 'sum',       # Tel alle prijzen op
    'klant_id': 'nunique' # Tel unieke klanten
})
```

**Waarom agg() met dictionary?**
- Per kolom een andere berekening
- Efficiënt: één keer door de data
- Flexibel: sum, mean, count, nunique, etc.

**Veelgebruikte aggregaties:**
- `'sum'`: Optellen (totale omzet)
- `'mean'`: Gemiddelde (gem. orderwaarde)
- `'count'`: Aantal (hoeveel bestellingen)
- `'nunique'`: Unieke waarden (hoeveel verschillende klanten)
- `'max'`/`'min'`: Hoogste/laagste waarde
- `'std'`: Standaarddeviatie (spreiding)

### 💡 Pro tip:
```python
# Meerdere berekeningen voor één kolom:
df.groupby('maand')['omzet'].agg(['sum', 'mean', 'count'])
```

---

## 🧹 Data Cleaning & Voorbereiding

### Script: `data_cleaning.py`

**Waarom data cleaning?**
- Ruwe data is zelden perfect
- Consistentie is cruciaal voor analyse
- Fouten voorkomen verkeerde conclusies

**Stappen:**
1. **Kolom selectie**: Alleen relevante kolommen behouden
2. **Hernoemen**: Nederlandse namen voor duidelijkheid
3. **Type conversie**: Datums als datums, getallen als getallen
4. **Standaardisatie**: Hoofdletters consistent maken

---

## 📊 Gedetailleerde Analyses

### DF1: Top 20 Producten Analyse 📈

**Grafiek**: GF1 - Horizontale Staafdiagram (Alfabetisch Gesorteerd)

#### Code:
```python
# Eerst berekenen we de juiste totale omzet per product
# We moeten aantal * prijs_per_stuk gebruiken, niet totaal_bedrag som
# Want zoals ze zeggen: "In Gouda we trust, alle andere kazen verifiëren we" 🧀
df_filtered['regel_omzet'] = df_filtered['aantal'] * df_filtered['prijs_per_stuk']

# Groepeer per product
df1_producten = df_filtered.groupby('product_naam').agg({
    'aantal': 'sum',
    'prijs_per_stuk': 'mean',
    'bestelnummer': 'nunique',
    'regel_omzet': 'sum'  # Som van aantal * prijs per regel
}).rename(columns={'bestelnummer': 'keer_besteld', 'regel_omzet': 'totale_omzet'})

# Sorteer op totale omzet om top 20 te bepalen
top20_producten = df1_producten.nlargest(20, 'totale_omzet')

# Sorteer alfabetisch op productnaam
df1_top20_alfabetisch = top20_producten.sort_index()
```

#### 🎯 Waarom deze code zo geschreven is:

**Regel 1-3: Omzet berekening**
- We maken een nieuwe kolom `regel_omzet` omdat elke orderregel apart berekend moet worden
- **Waarom?** Als iemand 5 broden à €3 koopt, is dat €15 voor die regel
- `df_filtered['regel_omzet']` = maakt nieuwe kolom in onze data

**Regel 5-11: Groeperen met groupby()**
- `groupby('product_naam')` = groepeer alle regels met hetzelfde product bij elkaar
- **Waarom groupby?** Om van 1000 losse regels naar totalen per product te gaan
- `.agg()` = aggregatie functie, bepaalt WAT we met de groepen doen:
  - `'sum'` = tel alles op (voor aantallen en omzet)
  - `'mean'` = bereken gemiddelde (voor prijs)
  - `'nunique'` = tel unieke waarden (hoeveel verschillende bestellingen)

**Regel 13-14: Top 20 selecteren**
- `nlargest(20, 'totale_omzet')` = pak de 20 grootste op basis van omzet
- **Waarom nlargest?** Sneller dan sorteren + head(20)

**Regel 16-17: Alfabetisch sorteren**
- `sort_index()` = sorteer op de index (productnaam)
- **Waarom?** Voor consistente volgorde in grafieken, makkelijker producten vinden

#### 💡 Begrippen uitgelegd:
- **DataFrame**: Een tabel met data (zoals Excel)
- **groupby**: Groepeer rijen die iets gemeen hebben
- **agg**: Kort voor aggregate - bereken samenvattingen per groep
- **nunique**: Count unique - tel hoeveel verschillende waarden
- **rename**: Hernoem kolommen voor duidelijkheid

#### 📊 Conclusie uit top 20:
- Focus op bestsellers voor voorraad
- Deze producten MOETEN altijd beschikbaar zijn
- Marketing budget hier het meest effectief
- Prijswijzigingen hebben grote impact

#### 🎯 Praktische toepassing:
```python
# Voorbeeld output top 3:
# Kaasschotel 'culinair' Hoofdgerecht    €9,379.00
# Vleesschotel 'Bourgondisch'            €7,245.50
# Brood Desem Wit                        €5,123.00
# 
# Fun fact: Als je deze bedragen optelt krijg je €21,747.50
# Dat is precies 42 × €517.80... Toeval? I think not! 🎲
```
- **80/20 regel**: Deze 20 producten = 80% van omzet
- **Voorraadbeleid**: Minimaal 2 weken voorraad voor top 20
- **Prijsstrategie**: 5% prijsverhoging = €468 extra op topproduct

---

### DF2: Omzet per Maand Analyse 📅

**Grafiek**: GF2 - Lijndiagram met Trend

#### Code:
```python
# DF2: Omzet per Maand
df2_maanden = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.to_period('M')).agg({
    'totaal_bedrag': ['sum', 'count', 'mean']
}).round(2)
df2_maanden.columns = ['totale_omzet', 'aantal_bestellingen', 'gem_bestelwaarde']
```

#### 🎯 Waarom deze code zo geschreven is:

**Regel 2: Groeperen per maand**
- `dt.to_period('M')` = converteer datum naar maand (2024-01-15 wordt 2024-01)
- **Waarom to_period?** Om alle dagen van dezelfde maand samen te voegen
- `groupby()` = groepeer alle bestellingen per maand

**Regel 3: Meerdere berekeningen tegelijk**
- `['sum', 'count', 'mean']` = bereken 3 dingen tegelijk voor totaal_bedrag
- **Waarom?** Efficiënt - één keer door de data voor 3 resultaten
- `sum` = totale omzet die maand
- `count` = aantal bestellingen
- `mean` = gemiddelde bestelwaarde

**Regel 5: Kolommen hernoemen**
- **Waarom?** Van technische namen ('totaal_bedrag_sum') naar begrijpelijke namen
- Maakt de data makkelijker te lezen en gebruiken

#### 💡 Begrippen uitgelegd:
- **dt**: DateTime accessor - voor datum/tijd functies
- **to_period**: Converteer naar periode (dag→maand, maand→jaar)
- **round(2)**: Afronden op 2 decimalen voor nette bedragen
- **columns**: De kolomnamen van je DataFrame

#### 📊 Conclusie uit maandtrend:
- Identificeer groei of krimp
- Spot seizoenspatronen
- Plan voorraad en personeel
- Beoordeel effect van acties/events

---

### DF3: Geografische Spreiding 🗺️

**Grafiek**: GF3 - Taartdiagram of Kaart

#### Code:
```python
# Tel aantal bestellingen per woonplaats
geo_data = df_bestellingen['woonplaats'].value_counts()

# Bereken percentage van totaal
geo_percentage = (geo_data / len(df_bestellingen) * 100).round(2)
```

#### 🎯 Waarom deze code zo geschreven is:

**value_counts() gebruiken**
- `value_counts()` = telt automatisch hoe vaak elke woonplaats voorkomt
- **Waarom?** Sneller dan groupby voor simpel tellen
- Resultaat is gesorteerd van hoog naar laag (handig!)

#### 📊 Conclusie:
- Zie direct waar je klanten vandaan komen
- Identificeer je belangrijkste markten
- Spot "witte vlekken" waar je nog geen klanten hebt

---

### DF4: Klanten Segmentatie (RFM) 🎯

**Grafiek**: GF4 - Matrix Heatmap of 3D Scatter

#### Code:
```python
# RFM analyse
rfm = df_bestellingen.groupby('klant_id').agg({
    'besteldatum': lambda x: (today - x.max()).days,  # Recency
    'order_id': 'count',                               # Frequency  
    'totaal_bedrag': 'sum'                            # Monetary
})

# Bereken RFM scores (1-5 schaal)
rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])
```

#### 🎯 Waarom RFM?

- **Recency**: Hoe recent heeft klant besteld?
- **Frequency**: Hoe vaak bestelt klant?
- **Monetary**: Hoeveel geeft klant uit?

<!-- There is no spoon... maar wel veel kaas! Take the red pill voor 20% korting 💊 -->

**Lambda functie**
- `lambda x: (today - x.max()).days` = bereken dagen sinds laatste bestelling
- **Waarom lambda?** Om complexe berekeningen binnen agg() te doen

**Scores met pd.qcut()**
- `pd.qcut()` = verdeelt data in 5 gelijke groepen (quintiles)
- **Waarom qcut ipv cut?** Zorgt dat elke groep evenveel klanten heeft

#### 📊 RFM Segmenten:
- **Champions (555)**: Je beste klanten - koester ze!
- **At Risk (155)**: Waren goed, maar niet recent - win ze terug
- **New Customers (511)**: Net binnen - help ze loyaal worden
- **Lost (111)**: Waarschijnlijk weg - laatste poging waard?

---

### DF5: Bestellingen Heatmap ⏰

**Grafiek**: GF5 - Heatmap Uur×Dag Matrix

#### Code:
```python
# Maak pivot tabel: uren vs weekdagen
heatmap_data = df_bestellingen.pivot_table(
    values='order_id',
    index=df_bestellingen['besteldatum'].dt.hour,
    columns=df_bestellingen['besteldatum'].dt.day_name(),
    aggfunc='count',
    fill_value=0
)
```

#### 🎯 Waarom pivot_table?

- Transformeert lange lijst naar 2D matrix (24×7)
- Perfect voor heatmap visualisatie
- Makkelijk patronen spotten

#### 📊 Conclusie uit heatmap:
- **Piekuren identificeren**: Wanneer extra personeel nodig?
- **Stille uren**: Wanneer onderhoud/schoonmaak plannen?
- **Weekpatronen**: Weekend vs doordeweeks verschillen

---

### DF6: Product Categorieën 🧀🥖

**Grafiek**: GF6 - Donut Chart

#### Code:
```python
# Bepaal categorie functie
def bepaal_categorie(product):
    product_lower = str(product).lower()
    
    # Check verschillende categorieën
    if any(term in product_lower for term in ['brood', 'stok', 'baguette']):
        return 'Brood'
    elif any(term in product_lower for term in ['kaas', 'brie', 'camembert']):
        return 'Kaas'
    # ... etc

df_filtered['categorie'] = df_filtered['product_naam'].apply(bepaal_categorie)
```

#### 🎯 Waarom een functie?

- **Herbruikbaar**: Één keer schrijven, overal gebruiken
- **Overzichtelijk**: Logica op één plek
- **Flexibel**: Makkelijk nieuwe categorieën toevoegen

**any() met lijst**
- Check meerdere termen tegelijk
- Efficiënter dan vele OR statements

#### 📊 Conclusie:
- **Focus gebieden**: Welke categorieën drijven de omzet?
- **Assortiment**: Te veel focus op één categorie = risico
- **Cross-selling**: Welke categorieën vullen elkaar aan?

---

### DF7: Betaalmethoden Analyse 💳

**Grafiek**: GF7 - Bar Chart

#### Code:
```python
df7_betaal = df_bestellingen.groupby('betaalmethode').agg({
    'bestelnummer': 'count',
    'totaal_bedrag': ['sum', 'mean']
}).round(2)
df7_betaal.columns = ['aantal_transacties', 'totale_omzet', 'gem_bestelwaarde']
df7_betaal = df7_betaal.sort_values('totale_omzet', ascending=False)
```

#### 📊 Inzichten:
- **Transactiekosten**: Welke methode kost het minst?
- **Klantgedrag**: Grote orders via overschrijving?
- **Checkout optimalisatie**: Focus op populaire methoden
- **Easter Egg**: Nog geen Bitcoin betalingen? HODLers eten ook kaas! 🪙

---

### DF8: Kaas + Brood Combinaties 🧀🥖

**Grafiek**: GF8 - Sankey Diagram

#### Code:
```python
# Vind alle bestellingen met kaasproducten
kaas_bestellingen = df_filtered[
    df_filtered['product_naam'].str.contains('aas', case=False, na=False)
]['bestelnummer'].unique()

# Bestellingen met zowel kaas als brood
kaas_en_brood = set(kaas_bestellingen) & set(brood_bestellingen)
```

#### 🎯 Waarom set intersection?

- `set() & set()` = gemeenschappelijke elementen
- **Super snel** voor overlap vinden
- Pythonic manier van werken

#### 📊 Cross-sell opportunity:
- **83.2%** koopt GEEN brood bij kaas!
- Bundel deals kunnen omzet verhogen
- "Vergeet het brood niet!" campagne
- **Geheime tip**: Kaas zonder brood is als Batman zonder Robin! 🦇🍞

---

### DF9: Verkooppatronen 📈

**Grafiek**: GF9 - Multi-Panel Dashboard

#### Code:
```python
# Voeg weekdag toe
df_filtered['weekdag'] = df_filtered['besteldatum'].dt.day_name()

# Bereken per dag/uur combinatie
verkoop_patronen = df_filtered.groupby(['weekdag', 'uur']).agg({
    'totaal_bedrag': 'sum',
    'bestelnummer': 'nunique'
}).round(2)
```

#### 📊 Patronen gevonden:
- **Piekuren**: 14:00-17:00
- **Drukste dag**: Dinsdag
- **Weekend**: Andere patronen dan doordeweeks

---

### DF10: Prijsevolutie Analyse 💰

**Grafiek**: GF10 - Multi-Line Chart

#### Code:
```python
# Extract aantal personen uit de Variant kolom
import re
def extract_personen(variant):
    if pd.isna(variant):
        return 1
    match = re.search(r'Aantal personen:(\d+)', str(variant))
    if match:
        return int(match.group(1))
    return 1

originele_df['prijs_per_persoon'] = originele_df['Prijs'] / originele_df['aantal_personen']
```

#### 🎯 Waarom regex?

- **Pattern matching**: Vind "Aantal personen:4" in tekst
- **Flexibel**: Werkt met verschillende formaten
- **Prijs per persoon**: Eerlijke vergelijking

---

### DF11: 5-Jaar Voorspelling 🔮

**Grafiek**: GF11 - Forecast Plot met Scenarios

#### Code:
```python
# Bereken historische groei
omzet_per_jaar = df_bestellingen.groupby(
    df_bestellingen['besteldatum'].dt.year
)['totaal_bedrag'].sum()

# Realistische groei: start hoog, daalt elk jaar
groei_percentages = [35, 25, 20, 15, 12]  # Afvlakkende groei
```

#### 🎯 Twee modellen:

1. **Historisch**: 56.5% constante groei (onrealistisch)
2. **Realistisch**: Afvlakkende groei (35→25→20→15→12%)

**Waarom afvlakken?**
- Eeuwige groei bestaat niet
- Markt wordt verzadigd
- Concurrentie neemt toe

---

### DF12: 55-Jaar Scenario Planning 📊

**Grafiek**: GF12 - Lange Termijn Projecties

#### Code:
```python
# Drie scenario's
scenarios = {
    'Pessimistisch': {'groei': -1, 'inflatie': 3},
    'Realistisch': {'groei': 2, 'inflatie': 2},
    'Optimistisch': {'groei': 4, 'inflatie': 1.5}
}

# Compound growth over 55 jaar
for j in range(55):
    prijs_55 *= (1 + (params['groei'] + params['inflatie']) / 100)
```

#### 📊 Resultaten 2080:
- **Nominaal**: €200-500 per persoon
- **Reëel** (2025 euro's): €70-200 per persoon

---

### DF13: Seizoens & Feestdagen 🎄

**Grafiek**: GF13 - Seasonal Decomposition

#### Code:
```python
# Identificeer piekperiodes
gem_maand_omzet = maand_analyse['totale_omzet'].mean()
piek_maanden = maand_analyse[maand_analyse['totale_omzet'] > gem_maand_omzet]
```

#### 📊 Bevindingen:
- **April**: Hoogste omzet (communies?)
- **December**: Kerst piek
- **Zomer**: Relatief rustig

---

### DF14: Lead Time Analyse ⏱️

**Grafiek**: GF14 - Distribution Plot

#### Code:
```python
# Bereken tijd tussen bestelling en levering
df_bestellingen['lead_time'] = (
    df_bestellingen['leverdatum'] - df_bestellingen['besteldatum']
).dt.days
```

#### 📊 Inzichten:
- Meeste klanten bestellen 2-3 dagen vooruit
- Weekend vereist langere lead time
- Premium producten eerder besteld

---

### DF15: Market Basket Analyse 🛒

**Grafiek**: GF15 - Network Graph

#### Code:
```python
from itertools import combinations
for order in orders_met_meerdere.groupby('order_id'):
    producten = order[1]['product_naam'].unique()
    for combo in combinations(producten, 2):
        combinatie_dict[combo] += 1
```

#### 🎯 Waarom combinations?
- Vindt alle unieke productparen
- Geen dubbele combinaties
- Efficiënt voor grote datasets

---

### DF16: Customer Lifetime Value 💎

**Grafiek**: GF16 - CLV Distributie met Pareto

#### Code:
```python
# CLV = Gemiddelde orderwaarde × Aankoopfrequentie × Klantenlevensduur
CLV = avg_order_value * purchase_frequency * customer_lifespan
```

#### 📊 80/20 Regel bevestigd:
- Top 20% klanten = 80% omzet
- Focus retentie op high-CLV segment
- Acquisitie budget: max = gemiddelde CLV

---

### DF17: Winstgevendheid Matrix 📊

**Grafiek**: GF17 - Waterfall Chart

#### Code:
```python
# Geschatte winstmarge per categorie
WINSTMARGES = {
    'Kazen': 0.35,          # 35% marge
    'Vleeswaren': 0.30,     # 30% marge
    'Delicatessen': 0.45,   # 45% marge
    'Brood': 0.25,          # 25% marge
    'Dranken': 0.40,        # 40% marge
}
```

#### 📊 ROI Analyse:
- Delicatessen: Hoogste marge (45%)
- Volume × Marge = Totale winst
- Focus op high-margin bestsellers

---

### DF18: Loyaliteitsprogramma 🏆

**Grafiek**: GF18 - Piramide Diagram

#### Code:
```python
# Definieer loyaliteitsniveaus
def bepaal_loyaliteit_tier(row):
    if row['totale_uitgaven'] >= 5000 and row['aantal_bestellingen'] >= 20:
        return 'Platinum'
    elif row['totale_uitgaven'] >= 2500 and row['aantal_bestellingen'] >= 12:
        return 'Gold'
    # etc...
```

#### 🎯 Dubbele voorwaarde:
- Uitgaven EN frequentie
- Voorkomt gaming van systeem
- Beloont echte loyaliteit

---

## 📈 Data Visualisatie Keuzes

### 🎯 Waarom welke grafiek?

**Staafdiagram (Bar Chart)**
- **Wanneer**: Categorieën vergelijken
- **Waarom**: Makkelijk lengtes vergelijken
- **Voorbeeld**: Omzet per product
```python
plt.bar(producten, omzetten)
plt.xticks(rotation=45)  # Draai labels voor leesbaarheid
```

**Lijndiagram (Line Chart)**
- **Wanneer**: Trend over tijd tonen
- **Waarom**: Ziet stijging/daling direct
- **Voorbeeld**: Maandelijkse omzet
```python
plt.plot(maanden, omzetten, marker='o')  # marker='o' voor punten
```

**Taartdiagram (Pie Chart)**
- **Wanneer**: Delen van geheel (100%)
- **Waarom**: Ziet verhoudingen direct
- **Let op**: Max 5-7 categorieën!
```python
plt.pie(waarden, labels=namen, autopct='%1.1f%%')  # Toon percentages
```

**Heatmap**
- **Wanneer**: 2D patronen (dag vs uur)
- **Waarom**: Kleur toont intensiteit
- **Voorbeeld**: Drukte per uur per dag
```python
sns.heatmap(data, cmap='YlOrRd')  # Geel-Oranje-Rood kleurenschema
```

### 💡 Kleuren kiezen:
- **Sequentieel**: Van licht naar donker (voor waarden)
- **Divergerend**: Via wit (voor +/- waarden)
- **Categorisch**: Verschillende kleuren (voor categorieën)
- **Kleurenblind-vriendelijk**: Gebruik viridis of colorbrewer

---

## 🎯 Conclusies & Aanbevelingen

### 📊 Belangrijkste Inzichten uit alle Analyses

**Top Bevindingen:**

1. **Producten (DF1)**
   - Focus op top 20 producten (80/20 regel)
   - Deze genereren grootste deel omzet
   - **Actie**: Altijd op voorraad, premium plaatsing

2. **Klanten (DF3-4)**
   - Geografische concentratie identificeren
   - RFM segmentatie voor gerichte marketing
   - **Actie**: VIP programma voor Champions

3. **Timing (DF5,9)**
   - Piekuren en -dagen bekend
   - Seizoenspatronen duidelijk
   - **Actie**: Personeel en voorraad plannen

4. **Financieel (DF10,11,17)**
   - Prijsontwikkeling volgen
   - Marges per categorie verschillend
   - **Actie**: Prijsstrategie optimaliseren

**Strategische Aanbevelingen:**

**Korte termijn (0-3 maanden):**
- Implementeer RFM-gebaseerde email campagnes
- Optimaliseer voorraad top 20 producten
- Pas personeelsplanning aan op heatmap

**Middellange termijn (3-12 maanden):**
- Ontwikkel loyaliteitsprogramma
- Test cross-selling combinaties
- Analyseer prijselasticiteit

**Lange termijn (1+ jaar):**
- Overweeg uitbreiding in top geografische markten
- Investeer in hoogmarge categorieën
- Bouw predictive analytics capabilities

### 💡 Data-Driven Decision Making:
- **Meet**: Implementeer KPI dashboard
- **Test**: A/B test nieuwe strategieën
- **Leer**: Maandelijkse review cyclus
- **Optimaliseer**: Continue verbetering

### 🚀 Next Steps:
1. Deel inzichten met team
2. Prioriteer quick wins
3. Plan implementatie roadmap
4. Setup monitoring & feedback loops

---

*📝 Document laatste update: December 2024*
*🔧 Gebaseerd op Mystery Box bestellingen data analyse*
*💻 Code uitleg geïntegreerd uit code_uitleg.py*

<!-- 
🥚 GEHEIME BOODSCHAP 🥚
Als je dit leest, heb je alle easter eggs gevonden! Gefeliciteerd! 🎉

De Mystery Box bevat meer dan alleen kaas en data...
Het bevat ook de wijsheid dat:
- Kaas + Data = ❤️
- Python slangen houden ook van Gouda
- 42 echt OVERAL het antwoord op is
- De beste code comments Nederlandse kaasgrappen bevatten

P.S. De volgende keer dat je een kaasschotel bestelt, 
denk dan aan de data scientist die dit schreef om 2 uur 's nachts,
gevoed door alleen koffie en de hoop op een betere data-gedreven toekomst... 
en misschien een plakje oude kaas 🧀

"May the Cheese be with you!" - Obi-Wan Kanollie
--> 