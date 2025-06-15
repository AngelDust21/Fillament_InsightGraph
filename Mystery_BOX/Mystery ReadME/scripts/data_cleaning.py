import pandas as pd
import os

def clean_bestellingen_data():
    
    # Krijg het pad van dit script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Het Bestellingen.csv bestand staat nu in de data folder
    csv_path = os.path.join(script_dir, '..', 'data', 'Bestellingen.csv')
    
    # Lees de dataset in
    df = pd.read_csv(csv_path)
    
    # Behoud alleen nodige kolommen - gebruik 'betaalmethode' met kleine letter
    df_filtered = df[['Bestelnummer', 'Gemaakt op', 'Tijd', 'E-mailadres contactpersoon', 
                      'Item', 'Aantal', 'Prijs', 'Totaal', 'Woonplaats van facturering', 
                      'Postcode voor facturering', 'betaalmethode']].copy()
    
    # Hernoem kolommen naar Nederlands
    df_filtered.columns = ['bestelnummer', 'besteldatum', 'besteltijd', 'email_klant', 
                          'product_naam', 'aantal', 'prijs_per_stuk', 'totaal_bedrag', 
                          'woonplaats', 'postcode', 'betaalmethode']
    
    # Verwijder rijen met missende waarden
    df_filtered = df_filtered.dropna()
    
    # BELANGRIJK: Standaardiseer woonplaatsnamen
    # Verwijder extra spaties, converteer naar title case
    df_filtered['woonplaats'] = df_filtered['woonplaats'].str.strip()  # Verwijder spaties
    df_filtered['woonplaats'] = df_filtered['woonplaats'].str.title()  # Eerste letter hoofdletter
    
    # Fix specifieke gevallen
    df_filtered['woonplaats'] = df_filtered['woonplaats'].replace({
        'Tongeren-Borgloon': 'Tongeren',  # Combineer varianten
        '3730 Hoeselt': 'Hoeselt',        # Verwijder postcodes uit plaatsnamen
        '3720 Kortessem': 'Kortessem'
    })
    
    # Verwijder speciale karakters en fix alle Tongeren varianten
    df_filtered.loc[df_filtered['woonplaats'].str.contains('Tongeren', na=False), 'woonplaats'] = 'Tongeren'
    
    # NIEUW: Standaardiseer productnamen
    # Fix dubbele kaasschotels
    df_filtered['product_naam'] = df_filtered['product_naam'].replace({
        # Kaasschotel culinair varianten - ALLES samenvoegen naar hoofdproduct
        "Kaasschotel 'culinair' Hoofdgerecht 250 gr. p.p.": "Kaasschotel 'culinair' Hoofdgerecht",
        "Kaasbox 'culinair' Hoofdgerecht": "Kaasschotel 'culinair' Hoofdgerecht",
        "Kaasbox 'culinair' Hoofdgerecht 250 gr. p.p.": "Kaasschotel 'culinair' Hoofdgerecht",
        "Kaasbox 'culinair' Hoofdgerecht 250 p.p.": "Kaasschotel 'culinair' Hoofdgerecht",
        "Gastronomische Kaasschotel - Hoofdgerecht": "Kaasschotel 'culinair' Hoofdgerecht",
        
        # Kaasbox culinair avondmaal naar dessert
        "Kaasbox 'culinair' Avondmaal": "Kaasschotel 'culinair' Dessert",
        "Kaasbox 'culinair' Avondmaal 200 gr. p.p.": "Kaasschotel 'culinair' Dessert",
        
        # Klasieke kaasschotel = traditioneel
        "Klasieke Kaasschotel - Hoofdgerecht": "Kaasschotel 'traditioneel' Hoofdgerecht",
        "Klasieke Kaasschotel - Dessert": "Kaasschotel 'traditioneel' Dessert",
        "Kaasbox 'traditioneel' Hoofdgerecht 250 gr. p.p.": "Kaasschotel 'traditioneel' Hoofdgerecht",
        "Kaasbox 'traditioneel' Hoofdgerecht 250 p.p.": "Kaasschotel 'traditioneel' Hoofdgerecht",
        "Kaasschotel 'traditioneel' Hoofdgerecht 250 gr. p.p.": "Kaasschotel 'traditioneel' Hoofdgerecht",
        
        # Only-Cheese varianten samenvoegen
        "Kaasschotel 'Only-Cheese' Hoofdgerecht culinair": "Kaasschotel 'Only-Cheese' Hoofdgerecht",
        "Gastronomische kaasselectie alleen kaas - Hoofdgerecht": "Kaasschotel 'Only-Cheese' Hoofdgerecht",
        
        # Fix spatie inconsistentie bij Only-Cheese
        "Kaasschotel 'Only-Cheese ' Hoofdgerecht": "Kaasschotel 'Only-Cheese' Hoofdgerecht",
        "Kaasschotel 'Only-Cheese ' Dessert": "Kaasschotel 'Only-Cheese' Dessert",
        
        # Kaasbox varianten - standaardiseer "gr." en "p.p."
        "Kaasbox 'traditioneel' Avondmaal 200 p.p.": "Kaasbox 'traditioneel' Avondmaal 200 gr. p.p.",
        "Kaasbox 'traditioneel' Dessert 150 p.p.": "Kaasbox 'traditioneel' Dessert 150 gr. p.p.",
        
        # Vleesschotel varianten samenvoegen
        "Gastronomische Vleesschotel - Hoofdgerecht": "Vleesschotel Rok4 'culinair'",
        "Vleesbox Rok4 'culinair'": "Vleesschotel Rok4 'culinair'",
        "Klasieke Vleesschotel - Hoofdgerecht": "Vleesschotel Traditioneel",
        "Vleesbox Traditioneel": "Vleesschotel Traditioneel",
        
        # Tapasschotel varianten samenvoegen
        "Gastronomische Tapasschotel": "Luxe Tapasschotel",
        
        # Raclette varianten samenvoegen
        "Premium Raclette schotel": "Gastronomische Raclette Schotel"
    })
    
    # Converteer datum naar datetime
    df_filtered['besteldatum'] = pd.to_datetime(df_filtered['besteldatum'], format='%b %d, %Y', errors='coerce')
    
    # BELANGRIJK: Groepeer per bestelling
    # Maak een aparte dataset op bestellingniveau
    df_bestellingen = df_filtered.groupby('bestelnummer').agg({
        'besteldatum': 'first',
        'besteltijd': 'first', 
        'email_klant': 'first',
        'totaal_bedrag': 'first',  # Totaal staat bij elke regel van een bestelling
        'woonplaats': 'first',
        'postcode': 'first',
        'betaalmethode': 'first',
        'product_naam': lambda x: ', '.join(x),  # Combineer alle producten
        'aantal': 'sum'  # Tel alle items op
    }).reset_index()
    
    print(f"Data cleaning klaar!")
    print(f"Items niveau: {len(df_filtered)} rijen")
    print(f"Bestellingen niveau: {len(df_bestellingen)} unieke bestellingen")
    
    return df_filtered, df_bestellingen

# Als dit script direct wordt uitgevoerd
if __name__ == "__main__":
    df_filtered, df_bestellingen = clean_bestellingen_data() 