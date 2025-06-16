"""
Code Uitleg Module - Documentatie van code keuzes en begrippen
Dit bestand legt uit WAAROM de code zo geschreven is en WAT alle begrippen betekenen
"""

# Dictionary met alle code fragmenten en hun uitleg (alfabetisch gesorteerd DF1-DF18)
CODE_UITLEG = {
    "DF1: Top 20 Producten": {
        "grafiek": "GF1: Horizontale Staafdiagram - Top 20 Producten op Omzet",
        "code": """
# Eerst berekenen we de juiste totale omzet per product
# We moeten aantal * prijs_per_stuk gebruiken, niet totaal_bedrag som
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
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

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

### 💡 Begrippen uitgelegd:
- **DataFrame**: Een tabel met data (zoals Excel)
- **groupby**: Groepeer rijen die iets gemeen hebben
- **agg**: Kort voor aggregate - bereken samenvattingen per groep
- **nunique**: Count unique - tel hoeveel verschillende waarden
- **rename**: Hernoem kolommen voor duidelijkheid

### 📊 Conclusie uit top 20:
- Focus op bestsellers voor voorraad
- Deze producten MOETEN altijd beschikbaar zijn
- Marketing budget hier het meest effectief
- Prijswijzigingen hebben grote impact
"""
    },
    
    "DF2: Omzet per Maand": {
        "grafiek": "GF2: Lijndiagram - Omzettrend per Maand",
        "code": """
# DF2: Omzet per Maand
df2_maanden = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.to_period('M')).agg({
    'totaal_bedrag': ['sum', 'count', 'mean']
}).round(2)
df2_maanden.columns = ['totale_omzet', 'aantal_bestellingen', 'gem_bestelwaarde']
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

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

### 💡 Begrippen uitgelegd:
- **dt**: DateTime accessor - voor datum/tijd functies
- **to_period**: Converteer naar periode (dag→maand, maand→jaar)
- **round(2)**: Afronden op 2 decimalen voor nette bedragen
- **columns**: De kolomnamen van je DataFrame

### 📊 Conclusie uit maandtrend:
- Identificeer groei of krimp
- Spot seizoenspatronen
- Plan voorraad en personeel
- Beoordeel effect van acties/events
"""
    },
    
    "DF3: Geografische Spreiding": {
        "grafiek": "GF3: Taartdiagram of Kaart - Klanten per Locatie",
        "code": """
# Tel aantal bestellingen per woonplaats
geo_data = df_bestellingen['woonplaats'].value_counts()

# Bereken percentage van totaal
geo_percentage = (geo_data / len(df_bestellingen) * 100).round(2)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2: value_counts() gebruiken**
- `value_counts()` = telt automatisch hoe vaak elke woonplaats voorkomt
- **Waarom?** Sneller dan groupby voor simpel tellen
- Resultaat is gesorteerd van hoog naar laag (handig!)

**Regel 5: Percentage berekening**
- Delen door totaal aantal bestellingen × 100
- **Waarom percentages?** Makkelijker te interpreteren dan absolute getallen
- `round(2)` = afronden op 2 decimalen voor nette weergave

### 💡 Begrippen uitgelegd:
- **value_counts()**: Telt unieke waarden en sorteert meteen
- **len(df)**: Geeft aantal rijen in DataFrame
- **Series**: Het resultaat van value_counts (zoals een kolom)

### 📊 Conclusie uit deze analyse:
- Zie direct waar je klanten vandaan komen
- Identificeer je belangrijkste markten
- Spot "witte vlekken" waar je nog geen klanten hebt
- Basis voor bezorgkosten en marketingbudget per regio
"""
    },
    
    "DF4: Klanten Segmentatie (RFM)": {
        "grafiek": "GF4: Matrix Heatmap of 3D Scatter - RFM Segmentatie",
        "code": """
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
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-6: RFM berekeningen in één groupby**
- `lambda x: (today - x.max()).days` = bereken dagen sinds laatste bestelling
- **Waarom lambda?** Om complexe berekeningen binnen agg() te doen
- **Waarom .max()?** We willen de LAATSTE (meest recente) besteldatum

**Regel 9-11: Scores met pd.qcut()**
- `pd.qcut()` = verdeelt data in 5 gelijke groepen (quintiles)
- **Waarom qcut ipv cut?** Zorgt dat elke groep evenveel klanten heeft
- **Labels [5,4,3,2,1] voor Recency**: Recent = hoge score (omgekeerd!)
- **rank(method='first')**: Voorkomt problemen bij gelijke waarden

### 💡 Begrippen uitgelegd:
- **lambda**: Mini-functie die je inline kunt schrijven
- **pd.qcut()**: Quantile cut - verdeelt in gelijke groepen
- **rank()**: Geeft rangnummers aan waarden
- **agg()**: Voer verschillende berekeningen tegelijk uit

### 📊 Conclusie uit RFM:
- **Champions (555)**: Je beste klanten - koester ze!
- **At Risk (155)**: Waren goed, maar niet recent - win ze terug
- **New Customers (511)**: Net binnen - help ze loyaal worden
- **Lost (111)**: Waarschijnlijk weg - laatste poging waard?

Met RFM kun je gerichte acties per groep ondernemen!
"""
    },
    
    "DF5: Bestellingen Heatmap": {
        "grafiek": "GF5: Heatmap - Bestellingen per Dag×Uur Matrix",
        "code": """
# Maak pivot tabel: uren vs weekdagen
heatmap_data = df_bestellingen.pivot_table(
    values='order_id',
    index=df_bestellingen['besteldatum'].dt.hour,
    columns=df_bestellingen['besteldatum'].dt.day_name(),
    aggfunc='count',
    fill_value=0
)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-8: pivot_table() voor 2D matrix**
- **values='order_id'**: Wat we tellen (kan elke kolom zijn)
- **index=dt.hour**: Uren komen op de Y-as (rijen)
- **columns=dt.day_name()**: Dagen komen op X-as (kolommen)
- **aggfunc='count'**: Tel het aantal orders
- **fill_value=0**: Vul lege cellen met 0 (geen orders)

**Waarom pivot_table?**
- Transformeert lange lijst naar 2D matrix (24×7)
- Perfect voor heatmap visualisatie
- Makkelijk patronen spotten

### 💡 Begrippen uitgelegd:
- **pivot_table()**: Draait data van lang naar breed formaat
- **dt.hour**: Haalt uur (0-23) uit datetime
- **dt.day_name()**: Geeft dag als tekst (Monday, Tuesday...)
- **fill_value**: Wat te doen met ontbrekende combinaties

### 📊 Conclusie uit heatmap:
- **Piekuren identificeren**: Wanneer extra personeel nodig?
- **Stille uren**: Wanneer onderhoud/schoonmaak plannen?
- **Weekpatronen**: Weekend vs doordeweeks verschillen
- **Optimalisatie**: Openingstijden aanpassen aan drukte

De donkerste vlekken = meeste actie = focus voor operations!
"""
    },
    
    "DF6: Product Categorieën": {
        "grafiek": "GF6: Donut Chart - Omzet per Categorie",
        "code": """
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
df6_categorie = df_filtered.groupby('categorie').agg({
    'totaal_bedrag': 'sum',
    'aantal': 'sum',
    'prijs_per_stuk': 'mean'
}).round(2)
df6_categorie['percentage'] = (df6_categorie['totaal_bedrag'] / df_filtered['totaal_bedrag'].sum() * 100).round(1)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-11: Categorie functie**
- `str(product).lower()` = maak alles kleine letters voor vergelijking
- **Waarom functie?** Herbruikbaar en overzichtelijk
- **any() met lijst**: Check meerdere termen tegelijk

**Regel 13: Apply functie op hele kolom**
- `.apply(bepaal_categorie)` = pas functie toe op elke rij
- **Waarom?** Efficiënt categoriseren van duizenden producten

**Regel 14-18: Groepeer en bereken metrics**
- Som van omzet en aantal per categorie
- Gemiddelde prijs om prijsniveau te zien
- **Waarom deze 3?** Geeft compleet beeld per categorie

**Regel 19: Percentage berekening**
- Deel door totale omzet voor relatief belang
- **Waarom?** "Kaas is 35% van omzet" zegt meer dan "€17.500"

### 💡 Begrippen uitgelegd:
- **apply()**: Pas functie toe op elke waarde in kolom
- **any()**: True als minstens één conditie waar is
- **Categorie logic**: Van specifiek naar algemeen

### 📊 Conclusie uit categorieën:
- **Focus gebieden**: Welke categorieën drijven de omzet?
- **Marge analyse**: Verschillende marges per categorie
- **Assortiment**: Te veel focus op één categorie = risico
- **Cross-selling**: Welke categorieën vullen elkaar aan?
"""
    },
    
    "DF7: Betaalmethoden": {
        "grafiek": "GF7: Bar Chart - Omzet per Betaalmethode",
        "code": """
df7_betaal = df_bestellingen.groupby('betaalmethode').agg({
    'bestelnummer': 'count',
    'totaal_bedrag': ['sum', 'mean']
}).round(2)
df7_betaal.columns = ['aantal_transacties', 'totale_omzet', 'gem_bestelwaarde']
df7_betaal = df7_betaal.sort_values('totale_omzet', ascending=False)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 1-4: Multi-level aggregatie**
- `['sum', 'mean']` voor totaal_bedrag = 2 berekeningen tegelijk
- **Waarom?** Één keer door data voor meerdere inzichten
- Count voor volume, sum voor waarde, mean voor gedrag

**Regel 5: Kolommen hernoemen**
- Van technische namen naar begrijpelijke labels
- **Waarom?** 'totaal_bedrag_sum' wordt 'totale_omzet'

**Regel 6: Sorteren op omzet**
- `ascending=False` = hoogste eerst
- **Waarom op omzet?** Financieel belangrijkste eerst

### 💡 Begrippen uitgelegd:
- **Multi-level agg**: Meerdere functies per kolom
- **Flatten columns**: Na multi-agg moet je kolommen hernoemen
- **ascending**: False = van hoog naar laag

### 📊 Conclusie uit betaalmethoden:
- **Transactiekosten**: Welke methode kost het minst?
- **Klantgedrag**: Grote orders via overschrijving?
- **Fraud risico**: Contant vs digitaal
- **Checkout optimalisatie**: Focus op populaire methoden
"""
    },
    
    "DF8: Kaas + Brood Combinaties": {
        "grafiek": "GF8: Sankey Diagram of Stacked Bar - Kaas-Brood Relaties",
        "code": """
# Vind alle bestellingen met kaasproducten
kaas_bestellingen = df_filtered[df_filtered['product_naam'].str.contains('aas', case=False, na=False)]['bestelnummer'].unique()

# Broodproducten identificeren
brood_termen = ['brood', 'stok', 'baguette', 'ciabata', 'margot', 'spelt', 'desem']
brood_mask = df_filtered['product_naam'].str.contains('|'.join(brood_termen), case=False, na=False)
brood_bestellingen = df_filtered[brood_mask]['bestelnummer'].unique()

# Bestellingen met zowel kaas als brood
kaas_en_brood = set(kaas_bestellingen) & set(brood_bestellingen)

# Bereken percentages
df8_brood_bij_kaas = pd.DataFrame({
    'totaal_kaas_bestellingen': [len(kaas_bestellingen)],
    'met_brood': [len(kaas_en_brood)],
    'zonder_brood': [len(kaas_bestellingen) - len(kaas_en_brood)],
    'percentage_met_brood': [round(len(kaas_en_brood) / len(kaas_bestellingen) * 100, 1)]
})
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2: Contains met 'aas'**
- Matcht 'kaas', 'Kaasschotel', etc.
- **Waarom 'aas'?** Vangt alle kaasvarianten
- Case=False voor hoofdletter ongevoelig

**Regel 5-7: Brood identificatie**
- Lijst met broodtermen om niets te missen
- `'|'.join()` maakt regex: 'brood|stok|baguette...'
- **Waarom lijst?** Flexibel uitbreidbaar

**Regel 10: Set intersection**
- `set() & set()` = gemeenschappelijke elementen
- **Waarom sets?** Super snel voor overlap vinden

**Regel 13-18: Resultaat DataFrame**
- Overzichtelijke presentatie van resultaten
- Absolute getallen EN percentage
- **Waarom beide?** Context én vergelijkbaarheid

### 💡 Begrippen uitgelegd:
- **str.contains()**: Zoek substring in tekst
- **unique()**: Haal duplicaten eruit
- **set()**: Verzameling unieke waarden
- **&**: Intersection (doorsnede) operator

### 📊 Conclusie uit kaas-brood analyse:
- **Upsell kans**: % klanten koopt geen brood bij kaas
- **Bundel deals**: Populaire kaas-brood combinaties
- **Assortiment**: Juiste broodsoorten voor kaasklanten?
- **Marketing**: "Vergeet het brood niet!" campagne
"""
    },
    
    "DF9: Verkooppatronen": {
        "grafiek": "GF9: Combined Chart - Dag/Uur/Seizoen Patronen",
        "code": """
# Voeg weekdag toe
df_filtered['weekdag'] = df_filtered['besteldatum'].dt.day_name()

# Bereken per dag/uur combinatie
verkoop_patronen = df_filtered.groupby(['weekdag', 'uur']).agg({
    'totaal_bedrag': 'sum',
    'bestelnummer': 'nunique'
}).round(2)

# Groepeer per maand voor seizoenspatronen
maand_omzet = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.month).agg({
    'totaal_bedrag': 'sum',
    'bestelnummer': 'count'
}).round(2)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2: Weekdag toevoegen**
- `dt.day_name()` = geeft dag als tekst (Monday, Tuesday...)
- **Waarom?** Mensen gedragen zich anders per weekdag
- Tekst is leesbaarder dan cijfers (0-6)

**Regel 5-9: Multi-level groupby**
- Groepeer op weekdag EN uur tegelijk
- **Waarom 2 levels?** Om patronen te vinden (zaterdag 10u vs maandag 10u)
- Som omzet + tel unieke orders

**Regel 12-15: Maand aggregatie**
- `dt.month` = haalt maandnummer uit datum
- **Waarom per maand?** Seizoenspatronen identificeren
- Count vs nunique: alle orders vs unieke orders

### 💡 Begrippen uitgelegd:
- **Multi-index**: Groeperen op meerdere kolommen
- **dt accessor**: Speciale functies voor datum/tijd kolommen
- **.loc[]**: Selecteer data uit multi-index

### 📊 Conclusie uit verkooppatronen:
- **Piekuren**: Wanneer extra personeel inzetten?
- **Weekend vs weekdagen**: Verschillende strategieën
- **Seizoenen**: Voorraad en marketing planning
- **Capaciteit**: Kan de keuken piekuren aan?

Deze patronen zijn de basis voor operationele beslissingen!
"""
    },
    
    "DF10: Prijsevolutie": {
        "grafiek": "GF10: Multi-Line Chart - Prijsontwikkeling per Categorie",
        "code": """
# Extract aantal personen uit de Variant kolom
import re
def extract_personen(variant):
    if pd.isna(variant):
        return 1
    match = re.search(r'Aantal personen:(\d+)', str(variant))
    if match:
        return int(match.group(1))
    return 1

originele_df['aantal_personen'] = originele_df['Variant'].apply(extract_personen)
originele_df['prijs_per_persoon'] = originele_df['Prijs'] / originele_df['aantal_personen']

# Filter kaas- en vleesschotels
kaas_df = originele_df[originele_df['Item'].str.contains('aasschotel', case=False, na=False)]
kaas_per_jaar = kaas_df.groupby(['jaar', 'Item'])['prijs_per_persoon'].agg(['mean', 'count']).round(2)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 3-9: Extract personen functie**
- `re.search()` = zoek patroon in tekst met regex
- **Waarom regex?** Om getal uit "Aantal personen:4" te halen
- `match.group(1)` = pak het eerste gevonden getal

**Regel 11-12: Prijs per persoon**
- Deel totaalprijs door aantal personen
- **Waarom?** Eerlijke vergelijking tussen verschillende schotels

**Regel 15-16: Filter en groepeer**
- Filter alleen relevante producten
- Groepeer per jaar EN product voor detail
- **Waarom mean + count?** Gemiddelde prijs + betrouwbaarheid

### 💡 Begrippen uitgelegd:
- **regex (re)**: Regular expressions voor patroon matching
- **pd.isna()**: Check of waarde leeg is
- **apply()**: Pas functie toe op elke rij
- **Multi-level groupby**: Groepeer op meerdere kolommen

### 📊 Conclusie uit prijsevolutie:
- **Inflatie tracking**: Volg je de markt of loop je achter?
- **Per persoon prijzen**: Eerlijke vergelijking
- **Jaarlijkse groei**: Basis voor toekomstvoorspellingen
- **Actie**: Geleidelijke prijsaanpassingen om klanten te behouden
"""
    },
    
    "DF11: Voorspellingen": {
        "grafiek": "GF11: Forecast Plot - 5 Jaar Voorspelling met Scenarios",
        "code": """
# Bereken groeipercentages uit historische data
omzet_per_jaar = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.year)['totaal_bedrag'].sum()
groei_percentages = []
jaren = sorted(omzet_per_jaar.index)
for i in range(1, len(jaren)):
    groei = ((omzet_per_jaar[jaren[i]] - omzet_per_jaar[jaren[i-1]]) / omzet_per_jaar[jaren[i-1]] * 100)
    groei_percentages.append(groei)

gem_omzet_groei = sum(groei_percentages) / len(groei_percentages) if groei_percentages else 5

# Realistische groei: start hoog, daalt elk jaar
groei_percentages = [35, 25, 20, 15, 12]  # Afvlakkende groei
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2: Jaarlijkse omzet**
- Groepeer per jaar voor historische trend
- **Waarom per jaar?** Stabielere basis dan maanden

**Regel 3-7: Groei berekening**
- Loop door jaren om jaar-op-jaar groei te berekenen
- **Waarom?** Historische groei als basis voor voorspelling
- Formule: (nieuw - oud) / oud × 100

**Regel 9: Gemiddelde groei**
- Gemiddelde van alle groeipercentages
- **Waarom gemiddelde?** Smootht uitschieters

**Regel 12: Realistische aanpassing**
- Afvlakkende groei (35→25→20→15→12%)
- **Waarom afvlakken?** Eeuwige groei bestaat niet
- Houdt rekening met marktmaturiteit

### 💡 Begrippen uitgelegd:
- **Year-over-year**: Vergelijk met zelfde periode vorig jaar
- **Compound growth**: Groei op groei effect
- **Scenario planning**: Meerdere mogelijke toekomsten

### 📊 Conclusie uit voorspellingen:
- **Historisch vs realistisch**: Twee modellen voor balans
- **Planning**: Budget en capaciteit voor komende jaren
- **Investeringen**: Wanneer uitbreiden?
- **Waarschuwing**: Verder = onzekerder

Gebruik als richtlijn, niet als garantie!
"""
    },
    
    "DF12: 55-jaar Voorspelling": {
        "grafiek": "GF12: Scenario Chart - Lange Termijn Projecties",
        "code": """
# Filter gastronomische schotels
kaas_gastr_df = kaas_df[kaas_df['Item'].str.contains('astronomisch', case=False, na=False)]
vlees_gastr_df = vlees_df[vlees_df['Item'].str.contains('astronomisch', case=False, na=False)]

# Bereken verschillende scenario's voor 55 jaar
scenarios = {
    'Pessimistisch': {'groei': -1, 'inflatie': 3},
    'Realistisch': {'groei': 2, 'inflatie': 2},
    'Optimistisch': {'groei': 4, 'inflatie': 1.5}
}

# Projecteer prijzen 55 jaar vooruit
for scenario_naam, params in scenarios.items():
    prijs_55 = start_prijs
    for j in range(55):
        prijs_55 *= (1 + (params['groei'] + params['inflatie']) / 100)
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-3: Filter op 'astronomisch'**
- Specifiek de premium/gastronomische versies
- **Waarom?** Deze hebben andere prijsdynamiek
- Focus op high-end segment voor lange termijn

**Regel 6-11: Scenario dictionary**
- 3 scenarios met groei + inflatie parameters
- **Waarom dictionary?** Overzichtelijk en uitbreidbaar
- Pessimistisch = negatieve reële groei

**Regel 14-17: Compound growth loop**
- 55 iteraties voor 55 jaar
- **Waarom loop?** Compound effect jaar-op-jaar
- Groei + inflatie = nominale stijging

### 💡 Begrippen uitgelegd:
- **Compound growth**: Rente-op-rente effect
- **Nominaal vs reëel**: Met/zonder inflatie correctie
- **Scenario planning**: Meerdere toekomsten modelleren

### 📊 Conclusie uit 55-jaar model:
- **Inflatie impact**: Grootste driver op lange termijn
- **Compound effect**: Kleine verschillen → grote impact
- **Onzekerheid**: Hoe verder, hoe onzekerder
- **Gebruik**: Strategische visie, niet exacte voorspelling

Let op: 55 jaar is extreem lang - gebruik voor discussie, niet planning!
"""
    },
    
    "DF13: Seizoens & Feestdagen": {
        "grafiek": "GF13: Seasonal Decomposition - Maandelijkse Patronen",
        "code": """
# Voeg maand en kwartaal info toe
df_bestellingen['maand'] = df_bestellingen['besteldatum'].dt.month
df_bestellingen['kwartaal'] = df_bestellingen['besteldatum'].dt.quarter

# Analyse per maand
maand_analyse = df_bestellingen.groupby('maand').agg({
    'totaal_bedrag': ['sum', 'mean', 'count']
}).round(2)
maand_analyse.columns = ['totale_omzet', 'gem_bestelling', 'aantal_orders']

# Identificeer piekperiodes
gem_maand_omzet = maand_analyse['totale_omzet'].mean()
piek_maanden = maand_analyse[maand_analyse['totale_omzet'] > gem_maand_omzet]
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-3: Datum features toevoegen**
- `dt.month` = maandnummer (1-12)
- `dt.quarter` = kwartaal (1-4)
- **Waarom beide?** Verschillende aggregatieniveaus

**Regel 6-10: Multi-metric aggregatie**
- 3 metrics in één keer: sum, mean, count
- **Waarom?** Volledig beeld per maand
- Flatten columns voor leesbaarheid

**Regel 12-14: Piekperiode detectie**
- Vergelijk met gemiddelde
- **Waarom mean?** Robuuster dan mediaan hier
- Boolean indexing voor filtering

### 💡 Begrippen uitgelegd:
- **dt.quarter**: Q1=Jan-Mar, Q2=Apr-Jun, etc.
- **Multi-column agg**: ['sum', 'mean', 'count']
- **Boolean mask**: df[conditie] voor filtering

### 📊 Conclusie uit seizoensanalyse:
- **Piekmaanden**: Extra personeel en voorraad
- **Dalperiodes**: Onderhoud en vakantie plannen
- **Marketing timing**: Campagnes voor rustige periodes
- **Cashflow**: Anticipeer op seizoensschommelingen

December vaak piek door feestdagen!
"""
    },
    
    "DF14: Bestelpatronen": {
        "grafiek": "GF14: Distribution Plot - Lead Time Analyse",
        "code": """
# Bereken tijd tussen bestelling en levering
df_bestellingen['lead_time'] = (df_bestellingen['leverdatum'] - df_bestellingen['besteldatum']).dt.days

# Analyseer lead times
lead_time_stats = df_bestellingen['lead_time'].describe()

# Groepeer per lead time
lead_time_dist = df_bestellingen['lead_time'].value_counts().sort_index()
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2: Lead time berekening**
- Datum verschil met `.dt.days`
- **Waarom dagen?** Standaard business metric
- Timedelta naar integer conversie

**Regel 5: Describe() voor statistieken**
- Geeft mean, std, min, max, quartiles
- **Waarom describe?** Complete distributie overzicht
- Één regel voor 8 statistieken

**Regel 8: Value counts met sort**
- Tel frequentie per lead time
- **Waarom sort_index?** Chronologische volgorde
- Zie meest voorkomende lead times

### 💡 Begrippen uitgelegd:
- **Timedelta**: Verschil tussen twee datums
- **.dt.days**: Converteer naar aantal dagen
- **describe()**: Samenvattende statistieken
- **value_counts()**: Frequentietabel

### 📊 Conclusie uit lead time analyse:
- **Service level**: Hoeveel % binnen X dagen?
- **Bottlenecks**: Waar zitten vertragingen?
- **Klantervaring**: Realistische verwachtingen stellen
- **Procesverbetering**: Focus op outliers

Snelle levering = competitief voordeel!
"""
    },
    
    "DF15: Product Combinaties (Market Basket)": {
        "grafiek": "GF15: Network Graph of Heatmap - Product Associaties",
        "code": """
# Vind producten die vaak samen gekocht worden
orders_met_meerdere = df_filtered[
    df_filtered['order_id'].isin(
        df_filtered['order_id'].value_counts()[
            df_filtered['order_id'].value_counts() > 1
        ].index
    )
]

# Maak combinatie matrix
from itertools import combinations
for order in orders_met_meerdere.groupby('order_id'):
    producten = order[1]['product_naam'].unique()
    for combo in combinations(producten, 2):
        combinatie_dict[combo] += 1
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-7: Filter orders met meerdere producten**
- `value_counts() > 1` = tel orders, behoud alleen die met 2+ producten
- `.isin()` = check of order_id in onze gefilterde lijst zit
- **Waarom?** Combinaties bestaan alleen bij 2+ producten per order

**Regel 11: Import combinations**
- `combinations(lijst, 2)` = alle unieke paren uit lijst
- **Waarom itertools?** Efficiënt en voorkomt dubbele paren

**Regel 12-15: Tel combinaties**
- Loop door elke order
- Vind alle productparen
- Tel hoe vaak elk paar voorkomt
- **Waarom dict?** Snel optellen per combinatie

### 💡 Begrippen uitgelegd:
- **isin()**: Check lidmaatschap (zit waarde in lijst?)
- **combinations**: Alle mogelijke paren zonder herhaling
- **unique()**: Haal dubbele producten uit order
- **groupby loop**: order[0] = key, order[1] = data

### 📊 Conclusie uit market basket:
- **Cross-selling kansen**: "Klanten die X kopen, kopen ook Y"
- **Bundel aanbiedingen**: Populaire combinaties samen aanbieden
- **Winkel layout**: Gerelateerde producten bij elkaar plaatsen
- **Voorraad planning**: Zorg dat combinaties beide op voorraad zijn

Top combinaties = direct toepasbare marketing insights!
"""
    },
    
    "DF16: Customer Lifetime Value": {
        "grafiek": "GF16: Histogram met Pareto Curve - CLV Distributie",
        "code": """
# CLV = Gemiddelde orderwaarde × Aankoopfrequentie × Klantenlevensduur
clv_data = df_bestellingen.groupby('klant_id').agg({
    'totaal_bedrag': ['sum', 'mean', 'count'],
    'besteldatum': ['min', 'max']
})

# Bereken metrieken
avg_order_value = clv_data[('totaal_bedrag', 'mean')]
purchase_frequency = clv_data[('totaal_bedrag', 'count')] / jaren_actief
customer_lifespan = 3  # Aanname: gemiddeld 3 jaar klant

CLV = avg_order_value * purchase_frequency * customer_lifespan
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-5: Multi-metric aggregatie**
- Bereken 5 metrics per klant in één keer
- **Waarom?** Alle CLV componenten in één query
- Min/max datum voor actieve periode

**Regel 8-9: CLV componenten**
- Gemiddelde orderwaarde uit mean
- Frequentie = orders / actieve jaren
- **Waarom delen door jaren?** Normaliseer voor vergelijking

**Regel 10: Levensduur aanname**
- 3 jaar als standaard
- **Waarom aanname?** Toekomst onbekend
- Kan verfijnd met survival analyse

**Regel 12: CLV formule**
- Simpele multiplicatie van 3 factoren
- **Waarom simpel?** Begrijpelijk en toepasbaar
- Complexere modellen mogelijk maar minder transparant

### 💡 Begrippen uitgelegd:
- **Multi-level columns**: Na agg met meerdere functies
- **CLV**: Customer Lifetime Value - totale waarde klant
- **Frequency**: Hoe vaak koopt klant per periode

### 📊 Conclusie uit CLV:
- **80/20 regel**: Focus op top 20% klanten
- **Acquisitie budget**: Max uitgave = CLV
- **Retentie prioriteit**: Hoge CLV klanten behouden
- **Segmentatie**: Verschillende strategieën per CLV groep
"""
    },
    
    "DF17: Winstgevendheid": {
        "grafiek": "GF17: Waterfall Chart - Winstmarges per Categorie",
        "code": """
# Geschatte winstmarge per categorie
WINSTMARGES = {
    'Kazen': 0.35,          # 35% marge
    'Vleeswaren': 0.30,     # 30% marge
    'Delicatessen': 0.45,   # 45% marge
    'Brood': 0.25,          # 25% marge
    'Dranken': 0.40,        # 40% marge
}

# Bereken winst
df_filtered['geschatte_winst'] = df_filtered.apply(
    lambda row: row['totaal_regel'] * WINSTMARGES.get(row['categorie'], 0.30),
    axis=1
)

# ROI = (Winst / Kosten) × 100
roi_per_categorie = (winst / kosten) * 100
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-8: Marge dictionary**
- Hardcoded marges per categorie
- **Waarom dictionary?** Makkelijk aan te passen
- **Waarom geschat?** Exacte marges vaak vertrouwelijk

**Regel 11-14: Apply met lambda**
- Bereken winst per regel individueel
- `.get(categorie, 0.30)` = default 30% als onbekend
- **Waarom apply?** Flexibel per rij berekenen

**Regel 17: ROI berekening**
- Return on Investment formule
- **Waarom ROI?** Vergelijk categorieën onderling
- Hogere ROI = efficiënter gebruik kapitaal

### 💡 Begrippen uitgelegd:
- **lambda row**: Functie die per rij werkt
- **.get()**: Dictionary lookup met default waarde
- **axis=1**: Apply functie per rij (niet kolom)
- **ROI**: Return on Investment - rendement

### 📊 Conclusie uit winstgevendheid:
- **Focus categorieën**: Hoogste marge ≠ meeste winst
- **Volume vs marge**: Balans vinden
- **Pricing strategy**: Ruimte voor prijsverhoging?
- **Assortiment**: Lage marge producten heroverwegen

Winstgevendheid stuurt strategische keuzes!
"""
    },
    
    "DF18: Loyaliteitsprogramma": {
        "grafiek": "GF18: Piramide Diagram - Loyaliteitstiers",
        "code": """
# Definieer loyaliteitsniveaus
def bepaal_loyaliteit_tier(row):
    if row['totale_uitgaven'] >= 5000 and row['aantal_bestellingen'] >= 20:
        return 'Platinum'
    elif row['totale_uitgaven'] >= 2500 and row['aantal_bestellingen'] >= 12:
        return 'Gold'
    elif row['totale_uitgaven'] >= 1000 and row['aantal_bestellingen'] >= 6:
        return 'Silver'
    else:
        return 'Bronze'

# Bereken kortingspercentages
KORTINGEN = {
    'Platinum': 0.15,  # 15% korting
    'Gold': 0.10,      # 10% korting
    'Silver': 0.05,    # 5% korting
    'Bronze': 0.00     # 0% korting
}
""",
        "uitleg": """
### 🎯 Waarom deze code zo geschreven is:

**Regel 2-10: Tier functie**
- Dubbele voorwaarde: uitgaven EN frequentie
- **Waarom beide?** Voorkomt gaming (1x groot bedrag)
- If-elif structuur voor duidelijke hiërarchie

**Regel 13-18: Korting dictionary**
- Percentage per tier niveau
- **Waarom oplopend?** Beloon beste klanten meer
- 0% voor Bronze houdt ze betrokken

### 💡 Begrippen uitgelegd:
- **Tier systeem**: Niveaus van loyaliteit
- **AND voorwaarde**: Beide moeten waar zijn
- **Gaming**: Systeem misbruiken voor voordeel

### 📊 Conclusie uit loyaliteitsprogramma:
- **Retentie**: Klanten blijven voor volgende tier
- **Upsell**: Motivatie om meer uit te geven
- **Segmentatie**: Verschillende communicatie per tier
- **ROI**: Korting < extra omzet door loyaliteit

Goed programma betaalt zichzelf terug!
"""
    }
}

def get_code_uitleg(analyse_naam):
    """
    Haal code en wetenschappelijke uitleg op voor een specifieke analyse
    
    Parameters:
    analyse_naam (str): Naam van de analyse (bijv. "DF1: Top 20 Producten")
    
    Returns:
    dict: Dictionary met 'code', 'uitleg' en 'grafiek' keys
    """
    return CODE_UITLEG.get(analyse_naam, {
        "grafiek": "Grafiek informatie niet beschikbaar",
        "code": "# Code niet gevonden",
        "uitleg": "Uitleg niet beschikbaar voor deze analyse"
    })

def get_alle_analyses():
    """
    Geef lijst van alle beschikbare analyses
    
    Returns:
    list: Lijst met namen van alle analyses
    """
    return list(CODE_UITLEG.keys())

# Extra uitleg over code concepten en keuzes
ALGEMENE_CONCEPTEN = {
    "📋 Functie Index & Overzicht": {
        "uitleg": """
### 📊 Overzicht van alle gebruikte Python/Pandas functies

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
"""
    },
    
    "🐍 Python & Pandas Basics": {
        "uitleg": """
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
- **NaN**: Not a Number - lege waarde
- **dtype**: Data type (tekst, getal, datum)
"""
    },
    
    "📊 Groeperen & Aggregeren": {
        "uitleg": """
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
"""
    },
    
    "📈 Data Visualisatie Keuzes": {
        "uitleg": """
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
"""
    },
    
    "🎯 Conclusies & Aanbevelingen": {
        "uitleg": """
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
"""
    }
}

def get_algemeen_concept(concept_naam):
    """
    Haal uitleg op over code concepten en waarom bepaalde keuzes zijn gemaakt
    """
    concept = ALGEMENE_CONCEPTEN.get(concept_naam, {})
    return concept.get('uitleg', 'Concept niet gevonden') 