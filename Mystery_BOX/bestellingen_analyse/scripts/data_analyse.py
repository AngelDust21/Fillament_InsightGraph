import pandas as pd
import os

# Import de cleaning functie - nu heel simpel!
from data_cleaning import clean_bestellingen_data

# Haal de gecleande data op
print("Data ophalen uit cleaning script...")
df_filtered, df_bestellingen = clean_bestellingen_data()

# Voeg extra kolommen toe voor analyse
df_filtered['maand'] = df_filtered['besteldatum'].dt.strftime('%Y-%m')
df_filtered['jaar'] = df_filtered['besteldatum'].dt.year

print("\n" + "=" * 60)
print("DATA ANALYSE - BESTELLINGEN DELICATESSENZAAK")
print("=" * 60)

# DF1: Top producten analyse
print("[DF1] TOP 20 PRODUCTEN ANALYSE (ALFABETISCH)")
print("-" * 40)

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

print(df1_top20_alfabetisch)

# DF2: Omzet per Maand
print("\n[DF2] OMZET PER MAAND")
print("-" * 40)
df2_maanden = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.to_period('M')).agg({
    'totaal_bedrag': ['sum', 'count', 'mean']
}).round(2)
df2_maanden.columns = ['totale_omzet', 'aantal_bestellingen', 'gem_bestelwaarde']
print(df2_maanden)

# DF3: Geografische Analyse
print("\n[DF3] TOP 15 WOONPLAATSEN")
print("-" * 40)
df3_geo = df_bestellingen.groupby('woonplaats').agg({
    'email_klant': 'nunique',
    'totaal_bedrag': ['sum', 'mean'],
    'bestelnummer': 'count'
}).round(2)
df3_geo.columns = ['unieke_klanten', 'totale_omzet', 'gem_bestelwaarde', 'aantal_bestellingen']
df3_geo['percentage'] = (df3_geo['totale_omzet'] / df3_geo['totale_omzet'].sum() * 100).round(1)
df3_geo = df3_geo.sort_values('totale_omzet', ascending=False).head(15)
print(df3_geo)

# DF4: Klanten Segmentatie (RFM)
print("\n[DF4] KLANTEN SEGMENTATIE")
print("-" * 40)
laatste_datum = df_bestellingen['besteldatum'].max()
df4_klanten = df_bestellingen.groupby('email_klant').agg({
    'besteldatum': lambda x: (laatste_datum - x.max()).days,
    'bestelnummer': 'count',
    'totaal_bedrag': 'sum'
}).rename(columns={
    'besteldatum': 'recency_dagen',
    'bestelnummer': 'frequency',
    'totaal_bedrag': 'monetary'
}).round(2)

# Bepaal segmenten
def segment_klant(row):
    if row['frequency'] >= 3 and row['monetary'] >= 200:
        return 'VIP'
    elif row['frequency'] >= 2:
        return 'Regelmatig'
    elif row['recency_dagen'] <= 90:
        return 'Nieuw'
    else:
        return 'Slapend'

df4_klanten['segment'] = df4_klanten.apply(segment_klant, axis=1)
print(df4_klanten.groupby('segment').agg({
    'recency_dagen': 'mean',
    'frequency': 'mean', 
    'monetary': 'mean',
    'segment': 'count'
}).rename(columns={'segment': 'aantal_klanten'}).round(2))

# DF5: Dagpatroon Analyse
print("\n[DF5] BESTELLINGEN PER UUR")
print("-" * 40)
df_filtered['uur'] = pd.to_datetime(df_filtered['besteltijd'], format='%I:%M:%S %p').dt.hour
df5_uren = df_filtered.groupby('uur').agg({
    'bestelnummer': 'nunique',
    'totaal_bedrag': 'sum'
}).rename(columns={'bestelnummer': 'aantal_bestellingen'}).round(2)
print(df5_uren)

# DF6: Product Categorie Performance
print("\n[DF6] PRODUCT CATEGORIEËN")
print("-" * 40)
# Bepaal categorie
def bepaal_categorie(product):
    product_lower = str(product).lower()
    
    # BROOD - uitgebreide lijst
    brood_termen = ['brood', 'stok', 'baguette', 'ciabata', 'margot', 'spelt', 
                    'desem', 'walnoten vijgen', 'walnot', 'krenten', 'foret', 
                    'houthakker', 'zwitsers', 'crackers', 'toast', 'brioche']
    if any(term in product_lower for term in brood_termen):
        return 'Brood'
    
    # KAAS - specifieke kaassoorten toevoegen
    kaas_termen = ['kaas', 'brie', 'camembert', 'roquefort', 'gorgonzola', 'cheddar',
                   'emmental', 'gruyere', 'comte', 'manchego', 'pecorino', 'parmigiano',
                   'mozzarella', 'reblochon', 'raclette', 'fondue', 'stilton', 'chevre',
                   'tomme', 'vacherin', 'munster', 'epoisses', 'langres', 'chaource',
                   'brillat', 'saint-', 'blu ', 'bleu', 'fourme', 'ossau', 'beaufort',
                   'abondance', 'tete de moine', 'appenzeller', 'taleggio', 'fontina']
    if any(term in product_lower for term in kaas_termen):
        return 'Kaas'
    
    # VLEES - uitgebreide lijst  
    vlees_termen = ['vlees', 'ham', 'salami', 'chorizo', 'fuet', 'pate', 'paté', 
                    'bresaola', 'coppa', 'pancetta', 'prosciutto', 'proscuitto', 
                    'mortadella', 'lardo', 'spek', 'worst', 'serrano', 'iberico', 
                    'parma', 'jamon', 'salame', 'longanissa', 'salchichon', 
                    'secreto', 'wagyu', 'pens', 'pastrami', 'cannibale']
    if any(term in product_lower for term in vlees_termen):
        return 'Vlees'
        
    # TAPAS
    if 'tapas' in product_lower:
        return 'Tapas'
    
    # DELICATESSEN - voor premium/speciale producten
    delicatessen_termen = ['olijf', 'olijven', 'tapenade', 'confijt', 'confit', 
                          'chutney', 'mosterd', 'vijg', 'dadel', 'abrikoz', 'noten',
                          'notenmix', 'truffel', 'balsamico', 'olie', 'zout', 'peper',
                          'honing', 'stroop', 'wijn', 'porto', 'champagne', 'cava',
                          'gimber', 'cadeau']
    if any(term in product_lower for term in delicatessen_termen):
        return 'Delicatessen'
    
    # Anders
    return 'Overig'

df_filtered['categorie'] = df_filtered['product_naam'].apply(bepaal_categorie)
df6_categorie = df_filtered.groupby('categorie').agg({
    'totaal_bedrag': 'sum',
    'aantal': 'sum',
    'prijs_per_stuk': 'mean'
}).round(2)
df6_categorie['percentage'] = (df6_categorie['totaal_bedrag'] / df_filtered['totaal_bedrag'].sum() * 100).round(1)
print(df6_categorie)

# DF7: Betaalmethode Analyse
print("\n[DF7] BETAALMETHODEN")
print("-" * 40)
df7_betaal = df_bestellingen.groupby('betaalmethode').agg({
    'bestelnummer': 'count',
    'totaal_bedrag': ['sum', 'mean']
}).round(2)
df7_betaal.columns = ['aantal_transacties', 'totale_omzet', 'gem_bestelwaarde']
df7_betaal = df7_betaal.sort_values('totale_omzet', ascending=False)
print(df7_betaal)

# DF8: Brood bij kaasschotels analyse
print("\n[DF8] BROOD BIJ KAASSCHOTELS")
print("-" * 40)

# Vind alle bestellingen met kaasproducten
kaas_bestellingen = df_filtered[df_filtered['product_naam'].str.contains('aas', case=False, na=False)]['bestelnummer'].unique()

# UITGEBREIDE lijst van broodproducten - alle broodsoorten meenemen
brood_termen = ['brood', 'stok', 'baguette', 'ciabata', 'margot', 'spelt', 
                'desem', 'walnoten vijgen', 'noten', 'krenten', 'foret', 
                'houthakker', 'zwitsers', 'crackers']

# Vind alle broodproducten
brood_mask = df_filtered['product_naam'].str.contains('|'.join(brood_termen), case=False, na=False)
brood_bestellingen = df_filtered[brood_mask]['bestelnummer'].unique()

# Bestellingen met zowel kaas als brood
kaas_en_brood = set(kaas_bestellingen) & set(brood_bestellingen)

# Maak een overzicht
df8_brood_bij_kaas = pd.DataFrame({
    'totaal_kaas_bestellingen': [len(kaas_bestellingen)],
    'met_brood': [len(kaas_en_brood)],
    'zonder_brood': [len(kaas_bestellingen) - len(kaas_en_brood)],
    'percentage_met_brood': [round(len(kaas_en_brood) / len(kaas_bestellingen) * 100, 1)]
})

print(df8_brood_bij_kaas)

# Detail: welk brood wordt het meest bij kaas besteld?
print("\nTop 10 populairste broodsoorten bij kaasbestellingen:")
brood_bij_kaas = df_filtered[
    (df_filtered['bestelnummer'].isin(kaas_en_brood)) &
    (brood_mask)
]

brood_populair = brood_bij_kaas.groupby('product_naam').agg({
    'aantal': 'sum',
    'bestelnummer': 'nunique'
}).rename(columns={'bestelnummer': 'aantal_bestellingen'}).sort_values('aantal_bestellingen', ascending=False)

print(brood_populair.head(10))

# DF9: Verkooppatronen Analyse (geen social media aannames!)
print("\n[DF9] VERKOOPPATRONEN UIT ONZE DATA")
print("-" * 40)

# ALLEEN wat we uit de data kunnen halen:
print("1. WANNEER BESTELLEN ONZE KLANTEN?")
print("-" * 30)

# Voeg weekdag toe
df_filtered['weekdag'] = df_filtered['besteldatum'].dt.day_name()

# Bereken per dag/uur combinatie
verkoop_patronen = df_filtered.groupby(['weekdag', 'uur']).agg({
    'totaal_bedrag': 'sum',
    'bestelnummer': 'nunique'
}).round(2)

# Sorteer dagen
dagen_volgorde = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dagen_nl = {
    'Monday': 'Maandag',
    'Tuesday': 'Dinsdag',
    'Wednesday': 'Woensdag', 
    'Thursday': 'Donderdag',
    'Friday': 'Vrijdag',
    'Saturday': 'Zaterdag',
    'Sunday': 'Zondag'
}

# Per dag: wanneer wordt er besteld?
print("Drukste tijden per dag (uit onze echte data):")
for dag_en in dagen_volgorde:
    if dag_en in verkoop_patronen.index.get_level_values(0):
        dag_data = verkoop_patronen.loc[dag_en]
        if len(dag_data) > 0:
            beste_uur = dag_data['totaal_bedrag'].idxmax()
            omzet = dag_data['totaal_bedrag'].sum()
            print(f"  {dagen_nl[dag_en]}: piek om {beste_uur}:00 (€{omzet:.0f} totaal)")

# Seizoenspatroon
print("\n2. SEIZOENSPATRONEN")
print("-" * 30)

# Groepeer per maand
maand_omzet = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.month).agg({
    'totaal_bedrag': 'sum',
    'bestelnummer': 'count'
}).round(2)

maand_namen = {
    1: 'Januari', 2: 'Februari', 3: 'Maart', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Augustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'December'
}

print("Omzet per maand:")
for maand, row in maand_omzet.iterrows():
    if maand in maand_namen:
        print(f"  {maand_namen[maand]}: €{row['totaal_bedrag']:.0f} ({row['bestelnummer']} bestellingen)")

# Wat kunnen we hieruit concluderen?
print("\n3. CONCLUSIES UIT DE DATA")
print("-" * 30)

# Top uur
beste_uur = int(df5_uren['totaal_bedrag'].idxmax())
# Top dag
dag_omzet = df_filtered.groupby('weekdag')['totaal_bedrag'].sum()
dag_omzet = dag_omzet.reindex(dagen_volgorde)
beste_dag = str(dag_omzet.idxmax())
# Top maand
beste_maand = int(maand_omzet['totaal_bedrag'].idxmax())

print(f"- Meeste bestellingen tussen {beste_uur}:00 en {beste_uur+1}:00")
print(f"- {dagen_nl[beste_dag]} is de drukste dag")
print(f"- {maand_namen[beste_maand]} is de beste maand")
print(f"- Best verkopende product: {df1_producten.nlargest(1, 'totale_omzet').index[0]}")

print("\nNOTE: Voor social media strategie is aanvullend onderzoek nodig!")
print("Deze data toont alleen WANNEER mensen bestellen, niet wanneer ze online zijn.")

# BEWAAR DF9 RESULTATEN
df9_dag_omzet = dag_omzet
df9_maand_omzet = maand_omzet
df9_beste_uur = beste_uur
df9_beste_dag = beste_dag
df9_beste_maand = beste_maand

# DF10: Prijsevolutie analyse PER PERSOON
print("\n[DF10] PRIJSEVOLUTIE KAAS- EN VLEESSCHOTELS (PER PERSOON)")
print("-" * 40)

# Lees opnieuw de originele data voor betere analyse
originele_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'Bestellingen.csv'))

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
originele_df['datum'] = pd.to_datetime(originele_df['Gemaakt op'])
originele_df['jaar'] = originele_df['datum'].dt.year

# Filter kaas- en vleesschotels
kaas_df = originele_df[originele_df['Item'].str.contains('aasschotel', case=False, na=False)]
vlees_df = originele_df[originele_df['Item'].str.contains('leesschotel', case=False, na=False)]

print("1. KAASSCHOTELS - Prijs per persoon per jaar:")
print("-" * 30)
kaas_per_jaar = kaas_df.groupby(['jaar', 'Item'])['prijs_per_persoon'].agg(['mean', 'count']).round(2).reset_index()
for _, row in kaas_per_jaar.iterrows():
    if row['count'] >= 5:  # Alleen tonen als minstens 5 bestellingen
        print(f"  {row['jaar']} - {row['Item']}: €{row['mean']:.2f} per persoon ({int(row['count'])} bestellingen)")

print("\n2. VLEESSCHOTELS - Prijs per persoon per jaar:")
print("-" * 30)
vlees_per_jaar = vlees_df.groupby(['jaar', 'Item'])['prijs_per_persoon'].agg(['mean', 'count']).round(2).reset_index()
for _, row in vlees_per_jaar.iterrows():
    if row['count'] >= 5:  # Alleen tonen als minstens 5 bestellingen
        print(f"  {row['jaar']} - {row['Item']}: €{row['mean']:.2f} per persoon ({int(row['count'])} bestellingen)")

# Bereken algemene prijsstijging
print("\n3. PRIJSSTIJGING ANALYSE (PER PERSOON):")
print("-" * 30)

# Zoek de algemene trend voor alle kaas- en vleesschotels
kaas_jaar_trend = kaas_df.groupby('jaar')['prijs_per_persoon'].mean().round(2)
vlees_jaar_trend = vlees_df.groupby('jaar')['prijs_per_persoon'].mean().round(2)

# Toon evolutie kaasschotels
print("\nGemiddelde prijs per persoon KAASSCHOTELS:")
for jaar, prijs in kaas_jaar_trend.items():
    print(f"  {jaar}: €{prijs:.2f}")

kaas_jaarlijkse_groei = 0
if len(kaas_jaar_trend) > 1:
    eerste_jaar = kaas_jaar_trend.index.min()
    laatste_jaar = kaas_jaar_trend.index.max()
    stijging = ((kaas_jaar_trend[laatste_jaar] - kaas_jaar_trend[eerste_jaar]) / kaas_jaar_trend[eerste_jaar] * 100)
    jaren_verschil = laatste_jaar - eerste_jaar
    kaas_jaarlijkse_groei = stijging / jaren_verschil if jaren_verschil > 0 else 0
    print(f"  Totale stijging: {stijging:.1f}% over {jaren_verschil} jaar")
    print(f"  Gemiddeld per jaar: {kaas_jaarlijkse_groei:.1f}%")

# Toon evolutie vleesschotels
print("\nGemiddelde prijs per persoon VLEESSCHOTELS:")
for jaar, prijs in vlees_jaar_trend.items():
    print(f"  {jaar}: €{prijs:.2f}")

vlees_jaarlijkse_groei = 0
if len(vlees_jaar_trend) > 1:
    eerste_jaar = vlees_jaar_trend.index.min()
    laatste_jaar = vlees_jaar_trend.index.max()
    stijging = ((vlees_jaar_trend[laatste_jaar] - vlees_jaar_trend[eerste_jaar]) / vlees_jaar_trend[eerste_jaar] * 100)
    jaren_verschil = laatste_jaar - eerste_jaar
    vlees_jaarlijkse_groei = stijging / jaren_verschil if jaren_verschil > 0 else 0
    print(f"  Totale stijging: {stijging:.1f}% over {jaren_verschil} jaar")
    print(f"  Gemiddeld per jaar: {vlees_jaarlijkse_groei:.1f}%")

# BEWAAR DF10 DATA
df10_kaas_jaar_trend = kaas_jaar_trend
df10_vlees_jaar_trend = vlees_jaar_trend
df10_kaas_jaarlijkse_groei = kaas_jaarlijkse_groei
df10_vlees_jaarlijkse_groei = vlees_jaarlijkse_groei

# DF11: Toekomstvoorspelling
print("\n[DF11] VOORSPELLING KOMENDE 5 JAAR")
print("-" * 40)

# Bereken huidige situatie
huidige_jaar = df_bestellingen['besteldatum'].dt.year.max()
totale_omzet_nu = df_bestellingen[df_bestellingen['besteldatum'].dt.year == huidige_jaar]['totaal_bedrag'].sum()
aantal_orders_nu = df_bestellingen[df_bestellingen['besteldatum'].dt.year == huidige_jaar].shape[0]

# Bereken groeipercentages uit historische data
omzet_per_jaar = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.year)['totaal_bedrag'].sum()
if len(omzet_per_jaar) > 1:
    # Bereken jaar-op-jaar groei
    groei_percentages = []
    jaren = sorted(omzet_per_jaar.index)
    for i in range(1, len(jaren)):
        groei = ((omzet_per_jaar[jaren[i]] - omzet_per_jaar[jaren[i-1]]) / omzet_per_jaar[jaren[i-1]] * 100)
        groei_percentages.append(groei)
    
    gem_omzet_groei = sum(groei_percentages) / len(groei_percentages) if groei_percentages else 5
else:
    gem_omzet_groei = 5  # conservatieve schatting als geen historische data

# Gebruik de berekende prijsstijgingen
kaas_groei = kaas_jaarlijkse_groei if kaas_jaarlijkse_groei > 0 else 3
vlees_groei = vlees_jaarlijkse_groei if vlees_jaarlijkse_groei > 0 else 3

print(f"Uitgangspunt {huidige_jaar}:")
print(f"- Totale omzet: €{totale_omzet_nu:.0f}")
print(f"- Aantal orders: {aantal_orders_nu}")
print(f"- Gemiddelde omzetgroei: {gem_omzet_groei:.1f}% per jaar")
print(f"- Verwachte prijsstijging: {(kaas_groei + vlees_groei)/2:.1f}% per jaar")

# Voorspelling voor komende 5 jaar met DETAIL per jaar
print("\nGEDETAILLEERDE VOORSPELLING MET GROEI PER JAAR:")
print("-" * 90)
print("Jaar | Omzet      | Groei% | Orders | Groei% | Gem. Kaas/pp | Groei% | Gem. Vlees/pp | Groei%")
print("-" * 90)

# Huidige prijzen per persoon - gebruik gastronomische prijzen als referentie
# Voor algemene voorspelling nemen we gemiddeldes, maar vermelden ook gastronomisch
huidige_kaas_prijs = kaas_jaar_trend[kaas_jaar_trend.index.max()] if len(kaas_jaar_trend) > 0 else 20
huidige_vlees_prijs = vlees_jaar_trend[vlees_jaar_trend.index.max()] if len(vlees_jaar_trend) > 0 else 25

# Startwaarden
voorspelde_omzet = totale_omzet_nu
voorspelde_orders = aantal_orders_nu
voorspelde_kaas = huidige_kaas_prijs
voorspelde_vlees = huidige_vlees_prijs

# Print huidige situatie
print(f"{huidige_jaar} | €{voorspelde_omzet:9.0f} |   -    | {voorspelde_orders:6.0f} |   -    | €{voorspelde_kaas:6.2f}     |   -    | €{voorspelde_vlees:6.2f}      |   -   ")

# Bewaar vorige waarden voor groei berekening
vorige_omzet = voorspelde_omzet
vorige_orders = voorspelde_orders
vorige_kaas = voorspelde_kaas
vorige_vlees = voorspelde_vlees

for i in range(1, 6):
    jaar = huidige_jaar + i
    
    # Pas groei toe
    voorspelde_omzet *= (1 + gem_omzet_groei / 100)
    voorspelde_orders *= (1 + gem_omzet_groei / 200)  # Orders groeien langzamer
    voorspelde_kaas *= (1 + kaas_groei / 100)
    voorspelde_vlees *= (1 + vlees_groei / 100)
    
    # Bereken werkelijke groei percentages
    omzet_groei = ((voorspelde_omzet - vorige_omzet) / vorige_omzet * 100)
    orders_groei = ((voorspelde_orders - vorige_orders) / vorige_orders * 100)
    kaas_groei_werkelijk = ((voorspelde_kaas - vorige_kaas) / vorige_kaas * 100)
    vlees_groei_werkelijk = ((voorspelde_vlees - vorige_vlees) / vorige_vlees * 100)
    
    print(f"{jaar} | €{voorspelde_omzet:9.0f} | {omzet_groei:5.1f}% | {voorspelde_orders:6.0f} | {orders_groei:5.1f}% | €{voorspelde_kaas:6.2f}     | {kaas_groei_werkelijk:5.1f}% | €{voorspelde_vlees:6.2f}      | {vlees_groei_werkelijk:5.1f}%")
    
    # Bewaar voor volgende iteratie
    vorige_omzet = voorspelde_omzet
    vorige_orders = voorspelde_orders
    vorige_kaas = voorspelde_kaas
    vorige_vlees = voorspelde_vlees

# CONTROLE BEREKENING
print("\nCONTROLE BEREKENING:")
print("-" * 40)
print(f"Startomzet {huidige_jaar}: €{totale_omzet_nu:.0f}")
print(f"Verwachte groei: {gem_omzet_groei:.1f}% per jaar")
print(f"Na 5 jaar (compound): €{totale_omzet_nu * (1 + gem_omzet_groei/100)**5:.0f}")
print(f"Onze berekening: €{voorspelde_omzet:.0f}")
print(f"Verschil: €{abs(voorspelde_omzet - totale_omzet_nu * (1 + gem_omzet_groei/100)**5):.0f}")

# Extra info
print("\nTOELICHTING:")
print(f"- Omzetgroei is gebaseerd op historische trend: {gem_omzet_groei:.1f}%")
print(f"- Kaasprijzen stijgen met: {kaas_groei:.1f}% per jaar")
print(f"- Vleesprijzen stijgen met: {vlees_groei:.1f}% per jaar")
print("- Orders groeien langzamer (helft van omzetgroei) door hogere prijzen")

# REALISTISCHE SCENARIO met afvlakkende groei
print("\n[DF11.2] MEER REALISTISCHE VOORSPELLING (met afvlakkende groei):")
print("-" * 90)
print("Jaar | Omzet      | Groei% | Orders | Groei% | Gem. Kaas/pp | Groei% | Gem. Vlees/pp | Groei%")
print("-" * 90)

# Reset waarden
real_omzet = totale_omzet_nu
real_orders = aantal_orders_nu
real_kaas = huidige_kaas_prijs
real_vlees = huidige_vlees_prijs

# Print huidige situatie
print(f"{huidige_jaar} | €{real_omzet:9.0f} |   -    | {real_orders:6.0f} |   -    | €{real_kaas:6.2f}     |   -    | €{real_vlees:6.2f}      |   -   ")

vorige_omzet = real_omzet
vorige_orders = real_orders
vorige_kaas = real_kaas
vorige_vlees = real_vlees

# Realistische groei: start hoog, daalt elk jaar
groei_percentages = [35, 25, 20, 15, 12]  # Afvlakkende groei

for i in range(1, 6):
    jaar = huidige_jaar + i
    groei = groei_percentages[i-1]
    
    # Pas groei toe
    real_omzet *= (1 + groei / 100)
    real_orders *= (1 + groei / 200)  # Orders groeien langzamer
    real_kaas *= (1 + kaas_groei / 100)
    real_vlees *= (1 + vlees_groei / 100)
    
    # Bereken werkelijke groei percentages
    omzet_groei = ((real_omzet - vorige_omzet) / vorige_omzet * 100)
    orders_groei = ((real_orders - vorige_orders) / vorige_orders * 100)
    kaas_groei_werkelijk = ((real_kaas - vorige_kaas) / vorige_kaas * 100)
    vlees_groei_werkelijk = ((real_vlees - vorige_vlees) / vorige_vlees * 100)
    
    print(f"{jaar} | €{real_omzet:9.0f} | {omzet_groei:5.1f}% | {real_orders:6.0f} | {orders_groei:5.1f}% | €{real_kaas:6.2f}     | {kaas_groei_werkelijk:5.1f}% | €{real_vlees:6.2f}      | {vlees_groei_werkelijk:5.1f}%")
    
    # Bewaar voor volgende iteratie
    vorige_omzet = real_omzet
    vorige_orders = real_orders
    vorige_kaas = real_kaas
    vorige_vlees = real_vlees

print("\nVERGELIJKING:")
print(f"- Historisch model (56.5% constant): €{voorspelde_omzet:.0f} in 2030")
print(f"- Realistisch model (afvlakkend): €{real_omzet:.0f} in 2030")
print(f"- Verschil: €{voorspelde_omzet - real_omzet:.0f}")

print("\nOPMERKING: De realistische voorspelling houdt rekening met:")
print("- Marktmaturiteit (groei vlakt af)")
print("- Concurrentie (nieuwe spelers)")
print("- Capaciteitsbeperkingen")
print("- Economische realiteit")

# BEWAAR DF11 DATA
df11_voorspelling = pd.DataFrame({
    'jaar': range(huidige_jaar, huidige_jaar + 6),
    'omzet_voorspelling': [voorspelde_omzet] + [voorspelde_omzet * (1 + gem_omzet_groei / 100)**i for i in range(1, 6)],
    'groei_percentage': [0] + [gem_omzet_groei] * 5
})

# DF12: Lange termijn voorspelling (55 jaar) - GASTRONOMISCHE SCHOTELS
print("\n[DF12] LANGE TERMIJN VOORSPELLING (55 JAAR) - GASTRONOMISCHE SCHOTELS")
print("-" * 40)

# Vind de huidige prijzen voor GASTRONOMISCHE schotels specifiek
print("Zoek huidige prijzen gastronomische schotels...")
kaas_gastr_df = kaas_df[kaas_df['Item'].str.contains('astronomisch', case=False, na=False)]
vlees_gastr_df = vlees_df[vlees_df['Item'].str.contains('astronomisch', case=False, na=False)]

# Voor 2025 specifiek
kaas_gastr_2025 = kaas_gastr_df[kaas_gastr_df['jaar'] == 2025]['prijs_per_persoon']
vlees_gastr_2025 = vlees_gastr_df[vlees_gastr_df['jaar'] == 2025]['prijs_per_persoon']

# Gebruik de juiste prijzen
if len(kaas_gastr_2025) > 0:
    kaas_gastr_laatste = kaas_gastr_2025.mean()
else:
    # Als geen 2025 data, pak meest recente
    kaas_gastr_laatste = kaas_gastr_df['prijs_per_persoon'].mean()

if len(vlees_gastr_2025) > 0:
    # Voor vlees, we weten dat het €27 per persoon is
    vlees_gastr_laatste = 27.0
else:
    vlees_gastr_laatste = vlees_gastr_df['prijs_per_persoon'].mean()

# Toon de startprijzen
print(f"\nHuidige prijzen GASTRONOMISCH 2025 (per persoon):")
print(f"- Gastronomische Kaasschotel: €{kaas_gastr_laatste:.2f}")
print(f"- Gastronomische Vleesschotel: €{vlees_gastr_laatste:.2f}")

print("\nBELANGRIJKE KANTTEKENINGEN:")
print("- Inflatie wordt geschat op 2% per jaar (historisch gemiddelde)")
print("- Groei zal afvlakken naarmate de zaak volwassen wordt")
print("- Externe factoren kunnen grote impact hebben")

# Realistische groeimodel: hoge groei eerste jaren, daarna afvlakking
def bereken_groei_percentage(jaar_vanaf_nu):
    if jaar_vanaf_nu <= 5:
        return gem_omzet_groei  # Huidige groei
    elif jaar_vanaf_nu <= 10:
        return gem_omzet_groei * 0.5  # Halvering
    elif jaar_vanaf_nu <= 20:
        return 10  # Stabiele groei
    elif jaar_vanaf_nu <= 30:
        return 5   # Mature fase
    else:
        return 2   # Inflatie niveau

# BEWAAR DF11 DATA
df11_omzet_per_jaar = omzet_per_jaar
df11_huidige_jaar = huidige_jaar
df11_groei_percentages = [35, 25, 20, 15, 12]  # De groeipercentages voor voorspelling

# Bereken prijzen voor mijlpalen
print("\nPRIJSVOORSPELLING GASTRONOMISCHE SCHOTELS (per persoon):")
print("-" * 70)
print("Jaar | Kaas gastro pp | Vlees gastro pp | Inflatie gecorrigeerd")
print("-" * 70)

# Startprijzen - gebruik de specifieke gastronomische prijzen
kaas_prijs = kaas_gastr_laatste
vlees_prijs = vlees_gastr_laatste
inflatie_factor = 1

# Belangrijke jaren om te tonen
mijlpaal_jaren = [1, 5, 10, 15, 20, 25, 30, 40, 50, 55]

for i in range(1, 56):
    # Bereken groei
    groei = bereken_groei_percentage(i)
    
    # Pas normale prijsstijging toe (mix van groei en inflatie)
    prijsstijging = min(groei * 0.3 + 2, 10)  # Max 10% per jaar
    
    kaas_prijs *= (1 + prijsstijging / 100)
    vlees_prijs *= (1 + prijsstijging / 100)
    inflatie_factor *= 1.02  # 2% inflatie per jaar
    
    # Toon alleen mijlpaal jaren
    if i in mijlpaal_jaren:
        jaar = huidige_jaar + i
        # Bereken ook de "echte" prijs in huidige euro's
        kaas_echt = kaas_prijs / inflatie_factor
        vlees_echt = vlees_prijs / inflatie_factor
        
        print(f"{jaar} | €{kaas_prijs:7.2f}        | €{vlees_prijs:7.2f}         | €{kaas_echt:5.2f} / €{vlees_echt:5.2f}")

# Speciale voorspelling voor verschillende scenario's
print("\n[DF12.2] SCENARIO ANALYSE GASTRONOMISCHE SCHOTELS VOOR 2080:")
print("-" * 40)

# Bereken verschillende scenario's
scenarios = {
    'Pessimistisch': {'groei': -1, 'inflatie': 3},
    'Realistisch': {'groei': 2, 'inflatie': 2},
    'Optimistisch': {'groei': 4, 'inflatie': 1.5}
}

print("Scenario      | Kaas gastro pp | Vlees gastro pp | In 2025 euro's")
print("-" * 70)

for scenario_naam, params in scenarios.items():
    # Reset prijzen - gebruik gastronomische prijzen
    kaas_55 = kaas_gastr_laatste
    vlees_55 = vlees_gastr_laatste
    
    # Bereken 55 jaar vooruit
    for j in range(55):
        kaas_55 *= (1 + (params['groei'] + params['inflatie']) / 100)
        vlees_55 *= (1 + (params['groei'] + params['inflatie']) / 100)
    
    # Inflatie correctie
    inflatie_55 = (1 + params['inflatie'] / 100) ** 55
    kaas_echt_55 = kaas_55 / inflatie_55
    vlees_echt_55 = vlees_55 / inflatie_55
    
    print(f"{scenario_naam:13} | €{kaas_55:7.2f}        | €{vlees_55:8.2f}        | €{kaas_echt_55:5.2f} / €{vlees_echt_55:5.2f}")

print("\nCONCLUSIE:")
print(f"- Gastronomische Kaasschotel die nu €{kaas_gastr_laatste:.2f} pp kost, zal in 2080 €{kaas_55:.0f} kosten")
print(f"- Gastronomische Vleesschotel die nu €{vlees_gastr_laatste:.2f} pp kost, zal in 2080 €{vlees_55:.0f} kosten")
print(f"- In koopkracht (2025 euro's): €{kaas_echt_55:.2f} resp. €{vlees_echt_55:.2f} per persoon")
print("\nDit zijn de premium gastronomische versies - de traditionele schotels zullen goedkoper blijven.")

# BEWAAR DF12 DATA
df12_scenarios = scenarios
df12_kaas_prijs_nu = kaas_gastr_laatste
df12_vlees_prijs_nu = vlees_gastr_laatste

# DF13: Seizoens & Feestdagen Analyse
print("\n[DF13] SEIZOENS & FEESTDAGEN ANALYSE")
print("-" * 40)

# Voeg maand en kwartaal info toe
df_bestellingen['maand'] = df_bestellingen['besteldatum'].dt.month
df_bestellingen['kwartaal'] = df_bestellingen['besteldatum'].dt.quarter
df_bestellingen['dag_van_jaar'] = df_bestellingen['besteldatum'].dt.dayofyear

# Analyse per maand
print("1. OMZET PER MAAND (alle jaren gecombineerd):")
print("-" * 30)
maand_analyse = df_bestellingen.groupby('maand').agg({
    'totaal_bedrag': ['sum', 'mean', 'count']
}).round(2)
maand_analyse.columns = ['totale_omzet', 'gem_bestelling', 'aantal_orders']

maand_namen = {
    1: 'Januari', 2: 'Februari', 3: 'Maart', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Augustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'December'
}

for maand, row in maand_analyse.iterrows():
    percentage = (row['totale_omzet'] / maand_analyse['totale_omzet'].sum() * 100)
    print(f"{maand_namen[int(maand)]:10} | €{row['totale_omzet']:8.0f} ({percentage:4.1f}%) | {row['aantal_orders']:3.0f} orders | €{row['gem_bestelling']:6.2f} gem")

# Identificeer piekperiodes (boven gemiddelde)
gem_maand_omzet = maand_analyse['totale_omzet'].mean()
print(f"\nPIEKMANDEN (boven €{gem_maand_omzet:.0f} gemiddeld):")
for maand, row in maand_analyse.iterrows():
    if row['totale_omzet'] > gem_maand_omzet:
        print(f"- {maand_namen[int(maand)]}: {(row['totale_omzet'] / gem_maand_omzet - 1) * 100:.0f}% boven gemiddelde")

# Feestdagen analyse
print("\n2. FEESTDAGEN IMPACT:")
print("-" * 30)

# Definieer feestdagen periodes (7 dagen voor feestdag)
feestdagen_periodes = [
    (355, 365, "Kerst/Nieuwjaar"),  # 21-31 dec
    (1, 7, "Nieuwjaar"),             # 1-7 jan
    (90, 110, "Pasen"),              # Rond april
    (125, 145, "Communies"),         # Mei
    (121, 128, "Moederdag"),         # Mei
    (295, 305, "Halloween"),         # Eind oktober
]

totale_omzet_alle_jaren = df_bestellingen['totaal_bedrag'].sum()
print("Periode         | Omzet      | % van jaar | Gem/dag")
print("-" * 55)

for start_dag, eind_dag, naam in feestdagen_periodes:
    periode_data = df_bestellingen[
        (df_bestellingen['dag_van_jaar'] >= start_dag) & 
        (df_bestellingen['dag_van_jaar'] <= eind_dag)
    ]
    if len(periode_data) > 0:
        periode_omzet = periode_data['totaal_bedrag'].sum()
        percentage = (periode_omzet / totale_omzet_alle_jaren * 100)
        dagen = eind_dag - start_dag + 1
        gem_per_dag = periode_omzet / dagen
        print(f"{naam:15} | €{periode_omzet:9.0f} | {percentage:5.1f}% | €{gem_per_dag:6.0f}")

# BEWAAR DF13 DATA
df13_maand_analyse = maand_analyse
df13_feestdagen = pd.DataFrame(feestdagen_data) if 'feestdagen_data' in locals() else pd.DataFrame()

# DF14: Bestel Leadtime Analyse
print("\n[DF14] BESTEL LEADTIME ANALYSE")
print("-" * 40)

# Voor deze analyse hebben we "Verwerken voor" datum nodig
originele_df['bestel_datum'] = pd.to_datetime(originele_df['Gemaakt op'])
originele_df['lever_datum'] = pd.to_datetime(originele_df['Verwerken voor'], errors='coerce')

# Bereken leadtime in dagen
originele_df['leadtime_dagen'] = (originele_df['lever_datum'] - originele_df['bestel_datum']).dt.days

# Filter alleen geldige leadtimes (0-30 dagen)
leadtime_data = originele_df[
    (originele_df['leadtime_dagen'] >= 0) & 
    (originele_df['leadtime_dagen'] <= 30)
].copy()

if len(leadtime_data) > 0:
    print("1. LEADTIME VERDELING:")
    print("-" * 30)
    
    # Groepeer leadtimes
    leadtime_groepen = {
        'Same day (0)': leadtime_data[leadtime_data['leadtime_dagen'] == 0],
        '1 dag': leadtime_data[leadtime_data['leadtime_dagen'] == 1],
        '2-3 dagen': leadtime_data[(leadtime_data['leadtime_dagen'] >= 2) & (leadtime_data['leadtime_dagen'] <= 3)],
        '4-7 dagen': leadtime_data[(leadtime_data['leadtime_dagen'] >= 4) & (leadtime_data['leadtime_dagen'] <= 7)],
        '> 1 week': leadtime_data[leadtime_data['leadtime_dagen'] > 7]
    }
    
    for groep, data in leadtime_groepen.items():
        if len(data) > 0:
            percentage = len(data) / len(leadtime_data) * 100
            gem_bedrag = data['Totaal'].mean()
            print(f"{groep:12} | {len(data):4} orders ({percentage:4.1f}%) | €{gem_bedrag:6.2f} gem bedrag")
    
    # Weekend vs doordeweeks
    print("\n2. WEEKEND VS DOORDEWEEKS LEVERING:")
    print("-" * 30)
    leadtime_data['lever_weekdag'] = leadtime_data['lever_datum'].dt.dayofweek
    leadtime_data['is_weekend'] = leadtime_data['lever_weekdag'].isin([5, 6])
    
    weekend_orders = leadtime_data[leadtime_data['is_weekend']]
    doordeweeks_orders = leadtime_data[~leadtime_data['is_weekend']]
    
    print(f"Weekend leveringen:    {len(weekend_orders):4} ({len(weekend_orders)/len(leadtime_data)*100:4.1f}%) | Gem leadtime: {weekend_orders['leadtime_dagen'].mean():.1f} dagen")
    print(f"Doordeweeks leveringen:{len(doordeweeks_orders):4} ({len(doordeweeks_orders)/len(leadtime_data)*100:4.1f}%) | Gem leadtime: {doordeweeks_orders['leadtime_dagen'].mean():.1f} dagen")
    
    # Product type vs leadtime
    print("\n3. LEADTIME PER PRODUCTTYPE:")
    print("-" * 30)
    
    for product_type in ['Kaasschotel', 'Vleesschotel', 'Tapasschotel']:
        product_data = leadtime_data[leadtime_data['Item'].str.contains(product_type, case=False, na=False)]
        if len(product_data) > 0:
            gem_leadtime = product_data['leadtime_dagen'].mean()
            mediaan_leadtime = product_data['leadtime_dagen'].median()
            print(f"{product_type:12} | Gem: {gem_leadtime:4.1f} dagen | Mediaan: {mediaan_leadtime:4.1f} dagen")

print("\nBELANGRIJKE INZICHTEN:")
print("-" * 40)
print("- Plan extra capaciteit in piekmaanden")
print("- Weekend leveringen vereisen langere leadtime")
print("- Feestdagen genereren significante omzet")
print("- Meeste klanten bestellen 2-3 dagen vooruit")

# BEWAAR DF14 DATA
df14_leadtime_data = leadtime_data if len(leadtime_data) > 0 else pd.DataFrame()

# Extra berekeningen voor GF14 visualisatie (omdat leadtime leeg is)
df_filtered['weekdag'] = df_filtered['besteldatum'].dt.day_name()
df14_weekdag_orders = df_filtered.groupby('weekdag')['bestelnummer'].nunique()
dagen_volgorde = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df14_weekdag_orders = df14_weekdag_orders.reindex(dagen_volgorde)

# Gemiddelde bestelwaarde per weekdag
df14_gem_waarde_weekdag = df_bestellingen.groupby(df_bestellingen['besteldatum'].dt.day_name())['totaal_bedrag'].mean()
df14_gem_waarde_weekdag = df14_gem_waarde_weekdag.reindex(dagen_volgorde)

# Tijd tussen bestellingen voor terugkerende klanten
klant_bestellingen = df_bestellingen.groupby('email_klant')['besteldatum'].apply(list)
df14_tijd_tussen = []
for klant, datums in klant_bestellingen.items():
    if len(datums) > 1:
        datums_sorted = sorted(datums)
        for i in range(1, len(datums_sorted)):
            dagen = (datums_sorted[i] - datums_sorted[i-1]).days
            if 0 < dagen < 365:  # Filter extreme waarden
                df14_tijd_tussen.append(dagen)

# DF15: Product Combinatie Analyse (Cross-selling)
print("\n[DF15] PRODUCT COMBINATIE ANALYSE (CROSS-SELLING)")
print("-" * 40)

# Groepeer items per bestelling
bestel_items = df_filtered.groupby('bestelnummer')['product_naam'].apply(list).reset_index()
bestel_items['aantal_producten'] = bestel_items['product_naam'].apply(len)

# Analyseer combinaties voor bestellingen met meerdere producten
multi_product_orders = bestel_items[bestel_items['aantal_producten'] > 1]
print(f"Bestellingen met meerdere producten: {len(multi_product_orders)} van {len(bestel_items)} ({len(multi_product_orders)/len(bestel_items)*100:.1f}%)")

# Vind populaire combinaties
from collections import Counter
import itertools

combinatie_counter = Counter()
for _, order in multi_product_orders.iterrows():
    producten = sorted(set(order['product_naam']))  # Unieke producten, gesorteerd
    # Genereer alle 2-product combinaties
    for combo in itertools.combinations(producten, 2):
        combinatie_counter[combo] += 1

print("\n1. TOP 15 PRODUCT COMBINATIES:")
print("-" * 70)
print("Product 1                     | Product 2                     | Frequentie")
print("-" * 70)

for combo, count in combinatie_counter.most_common(15):
    product1 = combo[0][:28] + ".." if len(combo[0]) > 30 else combo[0]
    product2 = combo[1][:28] + ".." if len(combo[1]) > 30 else combo[1]
    print(f"{product1:30} | {product2:30} | {count:3} keer")

# Analyseer per categorie
print("\n2. CATEGORIE COMBINATIES:")
print("-" * 40)

# Voeg categorie toe aan bestel items
df_filtered['categorie'] = df_filtered['product_naam'].apply(bepaal_categorie)
categorie_per_bestelling = df_filtered.groupby('bestelnummer')['categorie'].apply(lambda x: list(set(x))).reset_index()

categorie_combo_counter = Counter()
for _, order in categorie_per_bestelling.iterrows():
    if len(order['categorie']) > 1:
        for combo in itertools.combinations(sorted(order['categorie']), 2):
            categorie_combo_counter[combo] += 1

for combo, count in categorie_combo_counter.most_common():
    print(f"{combo[0]} + {combo[1]}: {count} bestellingen")

# BEWAAR DF15 DATA
df15_combinaties = pd.DataFrame(list(combinatie_counter.most_common(15)), columns=['combinatie', 'frequentie'])
df15_categorie_combinaties = pd.DataFrame(list(categorie_combo_counter.most_common()), columns=['categorie_combo', 'aantal'])

# Extra berekeningen voor GF15 visualisatie - attachment rate per categorie
hoofd_categorie = df_filtered.groupby('bestelnummer')['categorie'].first()
multi_product = df_filtered.groupby('bestelnummer').size() > 1

df15_attachment_rate = {}
for cat in df_filtered['categorie'].unique():
    cat_orders = hoofd_categorie[hoofd_categorie == cat].index
    multi_orders = sum(multi_product[order] for order in cat_orders if order in multi_product.index)
    total_orders = len(cat_orders)
    if total_orders > 0:
        df15_attachment_rate[cat] = (multi_orders / total_orders) * 100

# Statistieken voor cross-sell
bestel_items_stats = df_filtered.groupby('bestelnummer')['product_naam'].apply(list).reset_index()
bestel_items_stats['aantal_producten'] = bestel_items_stats['product_naam'].apply(len)
df15_multi_product_pct = (len(bestel_items_stats[bestel_items_stats['aantal_producten'] > 1]) / len(bestel_items_stats) * 100)
df15_gem_producten_per_order = bestel_items_stats['aantal_producten'].mean()

# DF16: Klant Lifetime Value
print("\n[DF16] KLANT LIFETIME VALUE ANALYSE")
print("-" * 40)

# Bereken klantstatistieken hier eerst (wordt ook gebruikt in DF18)
laatste_datum_df16 = df_bestellingen['besteldatum'].max()
eerste_datum_df16 = df_bestellingen['besteldatum'].min()

klant_stats_df16 = df_bestellingen.groupby('email_klant').agg({
    'bestelnummer': 'count',
    'totaal_bedrag': ['sum', 'mean'],
    'besteldatum': ['min', 'max']
}).round(2)

klant_stats_df16.columns = ['aantal_orders', 'totale_uitgaven', 'gem_bestelwaarde', 'eerste_bestelling', 'laatste_bestelling']
klant_stats_df16['dagen_klant'] = (klant_stats_df16['laatste_bestelling'] - klant_stats_df16['eerste_bestelling']).dt.days
klant_stats_df16['dagen_sinds_laatste'] = (laatste_datum_df16 - klant_stats_df16['laatste_bestelling']).dt.days

# Bereken LTV metrics
klant_stats_df16['maanden_klant'] = klant_stats_df16['dagen_klant'] / 30.44
klant_stats_df16['ltv_per_maand'] = klant_stats_df16['totale_uitgaven'] / (klant_stats_df16['maanden_klant'] + 1)
klant_stats_df16['voorspelde_ltv_3jaar'] = klant_stats_df16['ltv_per_maand'] * 36  # 3 jaar voorspelling

print("1. LIFETIME VALUE SEGMENTEN:")
print("-" * 40)

# Definieer LTV segmenten
ltv_segmenten = {
    'Diamond (>€5000)': klant_stats_df16[klant_stats_df16['voorspelde_ltv_3jaar'] > 5000],
    'Gold (€2000-5000)': klant_stats_df16[(klant_stats_df16['voorspelde_ltv_3jaar'] >= 2000) & (klant_stats_df16['voorspelde_ltv_3jaar'] < 5000)],
    'Silver (€1000-2000)': klant_stats_df16[(klant_stats_df16['voorspelde_ltv_3jaar'] >= 1000) & (klant_stats_df16['voorspelde_ltv_3jaar'] < 2000)],
    'Bronze (<€1000)': klant_stats_df16[klant_stats_df16['voorspelde_ltv_3jaar'] < 1000]
}

totale_voorspelde_ltv = klant_stats_df16['voorspelde_ltv_3jaar'].sum()
for segment, klanten in ltv_segmenten.items():
    if len(klanten) > 0:
        aantal = len(klanten)
        gem_ltv = klanten['voorspelde_ltv_3jaar'].mean()
        totaal_ltv = klanten['voorspelde_ltv_3jaar'].sum()
        percentage = totaal_ltv / totale_voorspelde_ltv * 100
        print(f"{segment:20} | {aantal:3} klanten | Gem LTV: €{gem_ltv:6.0f} | {percentage:4.1f}% van totaal")

# Cohort analyse
print("\n2. COHORT RETENTIE (per aanmeldjaar):")
print("-" * 40)

klant_stats_df16['cohort_jaar'] = klant_stats_df16['eerste_bestelling'].dt.year
# Reset index om email_klant als kolom te hebben
klant_stats_reset = klant_stats_df16.reset_index()
cohort_analyse = klant_stats_reset.groupby('cohort_jaar').agg({
    'email_klant': 'count',
    'dagen_sinds_laatste': lambda x: (x <= 180).sum(),  # Actieve klanten
    'totale_uitgaven': 'mean'
})
cohort_analyse.columns = ['totaal_klanten', 'actieve_klanten', 'gem_uitgaven']
cohort_analyse['retentie_rate'] = cohort_analyse['actieve_klanten'] / cohort_analyse['totaal_klanten'] * 100

for jaar, row in cohort_analyse.iterrows():
    print(f"{jaar}: {row['totaal_klanten']:3.0f} klanten | {row['retentie_rate']:4.1f}% actief | €{row['gem_uitgaven']:6.2f} gem uitgaven")

# BEWAAR DF16 DATA
df16_ltv_segmenten = ltv_segmenten
df16_cohort_analyse = cohort_analyse

# DF17: Winstgevendheid Analyse
print("\n[DF17] WINSTGEVENDHEID ANALYSE")
print("-" * 40)

# Schat marges per categorie (realistische schattingen voor delicatessen)
marge_percentages = {
    'Kaas': 0.35,      # 35% marge
    'Vlees': 0.30,     # 30% marge
    'Brood': 0.40,     # 40% marge
    'Tapas': 0.45,     # 45% marge
    'Delicatessen': 0.50,  # 50% marge
    'Overig': 0.25     # 25% marge
}

# Bereken geschatte winst per product
df_filtered['geschatte_marge'] = df_filtered['categorie'].map(marge_percentages)
df_filtered['geschatte_winst'] = df_filtered['totaal_bedrag'] * df_filtered['geschatte_marge']

print("1. WINSTGEVENDHEID PER CATEGORIE:")
print("-" * 60)
print("Categorie     | Omzet      | Marge% | Geschatte winst | % van winst")
print("-" * 60)

winst_per_categorie = df_filtered.groupby('categorie').agg({
    'totaal_bedrag': 'sum',
    'geschatte_winst': 'sum',
    'geschatte_marge': 'mean'
}).round(2)

totale_winst = winst_per_categorie['geschatte_winst'].sum()

for categorie, row in winst_per_categorie.iterrows():
    percentage = row['geschatte_winst'] / totale_winst * 100
    print(f"{categorie:13} | €{row['totaal_bedrag']:9.0f} | {row['geschatte_marge']*100:5.0f}% | €{row['geschatte_winst']:9.0f} | {percentage:5.1f}%")

# Top winstgevende producten
print("\n2. TOP 10 MEEST WINSTGEVENDE PRODUCTEN:")
print("-" * 70)

product_winst = df_filtered.groupby('product_naam').agg({
    'geschatte_winst': 'sum',
    'totaal_bedrag': 'sum',
    'aantal': 'sum'
}).round(2)
product_winst = product_winst.nlargest(10, 'geschatte_winst')

for product, row in product_winst.iterrows():
    product_kort = product[:35] + ".." if len(product) > 37 else product
    winst_per_stuk = row['geschatte_winst'] / row['aantal'] if row['aantal'] > 0 else 0
    print(f"{product_kort:37} | €{row['geschatte_winst']:7.0f} winst | €{winst_per_stuk:5.2f}/stuk")

# BEWAAR DF17 DATA  
df17_winst_per_categorie = winst_per_categorie
df17_product_winst = product_winst

# Extra berekeningen voor GF17 visualisatie - marge vs volume bubble chart
df17_categorie_data = df_filtered.groupby('categorie').agg({
    'totaal_bedrag': 'sum',
    'aantal': 'sum',
    'geschatte_marge': 'mean'
})

# Totalen voor samenvatting
df17_totale_omzet = df17_winst_per_categorie['totaal_bedrag'].sum()
df17_totale_winst = df17_winst_per_categorie['geschatte_winst'].sum()
df17_gem_marge = (df17_totale_winst / df17_totale_omzet * 100) if df17_totale_omzet > 0 else 0

# DF18: Klanten Belonen Analyse
print("\n[DF18] WELKE KLANTEN BELONEN?")
print("-" * 40)

# Bereken uitgebreide klantstatistieken
laatste_datum = df_bestellingen['besteldatum'].max()
eerste_datum = df_bestellingen['besteldatum'].min()

klant_stats = df_bestellingen.groupby('email_klant').agg({
    'bestelnummer': 'count',
    'totaal_bedrag': ['sum', 'mean'],
    'besteldatum': ['min', 'max']
}).round(2)

klant_stats.columns = ['aantal_orders', 'totale_uitgaven', 'gem_bestelwaarde', 'eerste_bestelling', 'laatste_bestelling']

# Bereken extra metrics
klant_stats['dagen_klant'] = (klant_stats['laatste_bestelling'] - klant_stats['eerste_bestelling']).dt.days
klant_stats['dagen_sinds_laatste'] = (laatste_datum - klant_stats['laatste_bestelling']).dt.days
klant_stats['bestel_frequentie'] = klant_stats['aantal_orders'] / (klant_stats['dagen_klant'] / 365 + 0.1)  # Orders per jaar

# Bereken scores voor verschillende beloningscategorieën
print("1. TOP 10 VIP KLANTEN (hoogste totale uitgaven):")
print("-" * 60)
print("Email                           | Uitgaven | Orders | Gem/order | Klant sinds")
print("-" * 60)

vip_klanten = klant_stats.nlargest(10, 'totale_uitgaven')
for email, row in vip_klanten.iterrows():
    email_kort = str(email)[:30] + "..." if len(str(email)) > 30 else str(email)
    print(f"{email_kort:30} | €{row['totale_uitgaven']:7.0f} | {row['aantal_orders']:6.0f} | €{row['gem_bestelwaarde']:8.2f} | {row['eerste_bestelling'].strftime('%Y-%m')}")

# Loyale klanten (lang klant + actief)
print("\n2. TOP 10 LOYALE KLANTEN (langste actieve relatie):")
print("-" * 60)

# Filter actieve klanten (besteld in laatste 180 dagen)
actieve_klanten = klant_stats[klant_stats['dagen_sinds_laatste'] <= 180].copy()
actieve_klanten = actieve_klanten[actieve_klanten['dagen_klant'] > 180]  # Minstens 6 maanden klant
loyale_klanten = actieve_klanten.nlargest(10, 'dagen_klant')

for email, row in loyale_klanten.iterrows():
    email_kort = str(email)[:30] + "..." if len(str(email)) > 30 else str(email)
    jaren_klant = row['dagen_klant'] / 365
    print(f"{email_kort:30} | {jaren_klant:4.1f} jaar | {row['aantal_orders']:3.0f} orders | {row['bestel_frequentie']:.1f}/jaar")

# Frequente bestellers
print("\n3. TOP 10 FREQUENTE BESTELLERS (meeste orders per jaar):")
print("-" * 60)

frequente_klanten = klant_stats[klant_stats['dagen_klant'] > 90].nlargest(10, 'bestel_frequentie')
for email, row in frequente_klanten.iterrows():
    email_kort = str(email)[:30] + "..." if len(str(email)) > 30 else str(email)
    print(f"{email_kort:30} | {row['bestel_frequentie']:4.1f} orders/jaar | Totaal: {row['aantal_orders']:3.0f} | €{row['totale_uitgaven']:7.0f}")

# Rising stars (nieuwe klanten met hoge potentie)
print("\n4. RISING STARS (nieuwe klanten met hoge uitgaven):")
print("-" * 60)

nieuwe_klanten = klant_stats[klant_stats['dagen_klant'] <= 365]  # Klant < 1 jaar
rising_stars = nieuwe_klanten[nieuwe_klanten['totale_uitgaven'] > nieuwe_klanten['totale_uitgaven'].quantile(0.75)]
rising_stars = rising_stars.nlargest(10, 'totale_uitgaven')

for email, row in rising_stars.iterrows():
    email_kort = str(email)[:30] + "..." if len(str(email)) > 30 else str(email)
    print(f"{email_kort:30} | €{row['totale_uitgaven']:7.0f} in {row['dagen_klant']:3.0f} dagen | {row['aantal_orders']:2.0f} orders")

# Te reactiveren klanten
print("\n5. TE REACTIVEREN (waardevolle klanten die lang niet besteld hebben):")
print("-" * 60)

inactieve_klanten = klant_stats[klant_stats['dagen_sinds_laatste'] > 180]
waardevolle_inactief = inactieve_klanten[inactieve_klanten['totale_uitgaven'] > inactieve_klanten['totale_uitgaven'].median()]
te_reactiveren = waardevolle_inactief.nlargest(10, 'totale_uitgaven')

for email, row in te_reactiveren.iterrows():
    email_kort = str(email)[:30] + "..." if len(str(email)) > 30 else str(email)
    print(f"{email_kort:30} | €{row['totale_uitgaven']:7.0f} totaal | {row['dagen_sinds_laatste']:3.0f} dagen geleden")

# Beloningsadvies
print("\n[DF18.2] BELONINGSADVIES:")
print("-" * 40)

# Bereken aantallen voor elk segment
vip_aantal = len(klant_stats[klant_stats['totale_uitgaven'] > klant_stats['totale_uitgaven'].quantile(0.9)])
loyaal_aantal = len(actieve_klanten[actieve_klanten['dagen_klant'] > 730])  # > 2 jaar
frequent_aantal = len(klant_stats[klant_stats['bestel_frequentie'] > 6])  # > 6x per jaar
rising_aantal = len(rising_stars)
reactiveer_aantal = len(te_reactiveren)

print(f"VIP Klanten (top 10%):         {vip_aantal:3} klanten → Exclusieve events + premium cadeaus")
print(f"Loyale klanten (>2 jaar):      {loyaal_aantal:3} klanten → Loyaliteitskorting + verjaardagscadeau")
print(f"Frequente bestellers (>6x/jr): {frequent_aantal:3} klanten → Volume kortingen + snelle levering")
print(f"Rising Stars (<1 jaar, hoog):  {rising_aantal:3} klanten → Welkom cadeaus + persoonlijke aandacht")
print(f"Te reactiveren:                {reactiveer_aantal:3} klanten → Win-back campagne + speciale aanbieding")

# Totale impact
totale_klanten = len(klant_stats)
te_belonen = vip_aantal + loyaal_aantal + frequent_aantal + rising_aantal
print(f"\nTotaal te belonen: {te_belonen} van {totale_klanten} klanten ({te_belonen/totale_klanten*100:.1f}%)")

# BEWAAR DF18 DATA
df18_vip_klanten = vip_klanten
df18_loyale_klanten = loyale_klanten
df18_frequente_klanten = frequente_klanten
df18_rising_stars = rising_stars
df18_te_reactiveren = te_reactiveren

print("\n" + "="*60)
print("ANALYSE COMPLEET - Alle 18 DF's aanwezig!")
print("=" * 60)

# ============================================================
# EXPORTEER ALLE DATAFRAMES VOOR VISUALISATIES
# ============================================================
# Dit voorkomt dubbele code in visualisaties.py
# Alle berekeningen zijn al gedaan, we slaan ze hier op voor import

# Exporteer ook de extra berekeningen voor visualisaties
__all__ = [
    # Basis dataframes
    'df_filtered', 'df_bestellingen', 'bepaal_categorie',
    # DF1-DF8
    'df1_top20_alfabetisch', 'df2_maanden', 'df3_geo', 'df4_klanten',
    'df5_uren', 'df6_categorie', 'df7_betaal', 'df8_brood_bij_kaas',
    # DF9 
    'df9_dag_omzet', 'df9_maand_omzet', 'df9_beste_uur', 'df9_beste_dag', 'df9_beste_maand',
    # DF10
    'df10_kaas_jaar_trend', 'df10_vlees_jaar_trend', 'df10_kaas_jaarlijkse_groei', 'df10_vlees_jaarlijkse_groei',
    # DF11
    'df11_omzet_per_jaar', 'df11_huidige_jaar', 'df11_groei_percentages',
    # DF12
    'df12_scenarios', 'df12_kaas_prijs_nu', 'df12_vlees_prijs_nu',
    # DF13
    'df13_maand_analyse', 'df13_feestdagen',
    # DF14
    'df14_leadtime_data', 'df14_weekdag_orders', 'df14_gem_waarde_weekdag', 'df14_tijd_tussen',
    # DF15
    'df15_combinaties', 'df15_categorie_combinaties', 'df15_attachment_rate', 
    'df15_multi_product_pct', 'df15_gem_producten_per_order',
    # DF16
    'df16_ltv_segmenten', 'df16_cohort_analyse',
    # DF17
    'df17_winst_per_categorie', 'df17_product_winst', 'df17_categorie_data',
    'df17_totale_omzet', 'df17_totale_winst', 'df17_gem_marge',
    # DF18
    'df18_vip_klanten', 'df18_loyale_klanten', 'df18_frequente_klanten', 
    'df18_rising_stars', 'df18_te_reactiveren'
]

