"""
Grafiek Uitleg Module - Gedetailleerde uitleg over wat elke grafiek laat zien
Dit bestand bevat uitleg over hoe je elke grafiek moet lezen en interpreteren
"""

# Dictionary met grafiek uitleg voor elke visualisatie
GRAFIEK_UITLEG = {
    "GF1: Top 20 Producten": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Een horizontale staafdiagram (barplot)
- 20 producten op de Y-as (verticaal)
- Omzet in euro's op de X-as (horizontaal)
- Producten gesorteerd van hoog naar laag
- Kleuren van donkerblauw (hoogste) naar lichtblauw (laagste)
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Product namen** (links): Dit zijn de exacte productnamen uit het assortiment
2. **Staaflengte**: Hoe langer de staaf, hoe meer omzet
3. **Getallen**: Exacte omzetbedragen staan bij elke staaf
4. **Volgorde**: Bovenste product = beste verkoper
5. **Kleurverloop**: Helpt snel de top 5-10 te identificeren
""",
        "betekenis": """
**Wat betekent dit?**
- De **80/20 regel**: Vaak komt 80% van je omzet van 20% producten
- **Bestsellers**: Deze 20 producten zijn je cashcows
- **Focus gebieden**: Waar je voorraad prioriteit moet liggen
- **Assortiment kracht**: Welke producten trekken klanten
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Top 5 producten**: Altijd op voorraad houden
✅ **Laatste 5**: Overweeg uit assortiment te halen
✅ **Marge check**: Controleer of top producten ook winstgevend zijn
✅ **Marketing**: Focus promoties op sub-top om deze te boosten
✅ **Inkoop**: Onderhandel betere prijzen voor top producten
"""
    },
    
    "GF2: Omzet Tijdlijn": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Een lijngrafiek met tijd op de X-as (horizontaal)
- Omzet in euro's op de Y-as (verticaal)  
- Blauwe lijn: maandelijkse omzet
- Rode stippellijn: 3-maands voortschrijdend gemiddelde
- Groene stippellijn: algemene trend
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Tijdas**: Van links (oudste data) naar rechts (nieuwste)
2. **Pieken**: Hoge punten = goede maanden
3. **Dalen**: Lage punten = slechte maanden
4. **Rode lijn**: Vlakt seizoenseffecten af
5. **Groene lijn**: Stijgend = groei, dalend = krimp
""",
        "betekenis": """
**Wat betekent dit?**
- **Seizoenspatronen**: December piek (feestdagen), zomer dip (vakantie)
- **Groeitrend**: Is het bedrijf groeiend of krimpend?
- **Volatiliteit**: Grote schommelingen = onvoorspelbaar
- **Cyclisch gedrag**: Terugkerende patronen per jaar
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Voorraadplanning**: Anticipeer op seizoenspieken
✅ **Personeelsplanning**: Meer staff in drukke maanden
✅ **Cashflow**: Reserveer geld voor rustige periodes
✅ **Marketing timing**: Plan campagnes voor dalmomenten
✅ **Groei strategie**: Bij dalende trend, actie vereist!
"""
    },
    
    "GF3: Geografische Spreiding": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Een taartdiagram (pie chart) of staafdiagram
- Verschillende plaatsnamen/regio's
- Percentages of aantallen bestellingen
- Kleuren per locatie
- Mogelijk een "Overig" categorie voor kleine plaatsen
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Grootte segmenten**: Groter = meer klanten uit die plaats
2. **Percentages**: Deel van totale klantenbestand
3. **Labels**: Plaatsnamen met cijfers
4. **Kleuren**: Elke plaats eigen kleur voor herkenning
5. **Legenda**: Koppelt kleuren aan plaatsen
""",
        "betekenis": """
**Wat betekent dit?**
- **Marktpenetratie**: Waar zitten je klanten?
- **Lokale dominantie**: Ben je sterk in eigen stad?
- **Groeipotentieel**: Welke gebieden onderbenut?
- **Bezorgkosten**: Verder weg = duurder bezorgen
- **Marketing focus**: Waar adverteren het meest loont
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Lokale marketing**: Versterk positie in top 3 plaatsen
✅ **Expansie**: Onderzoek potentieel in ondervertegenwoordigde gebieden  
✅ **Bezorgstrategie**: Minimale bestelbedragen per afstand
✅ **Partnerships**: Zoek lokale partners in verre gebieden
✅ **Klantonderzoek**: Waarom kopen mensen uit bepaalde plaatsen niet?
"""
    },
    
    "GF4: Klanten Segmentatie": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Een matrix/heatmap of scatter plot
- RFM scores (Recency, Frequency, Monetary)
- Klantgroepen in verschillende kleuren
- Mogelijk labels zoals "Champions", "At Risk"
- Aantallen klanten per segment
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Assen**: 
   - X-as: Frequency (hoe vaak koopt klant)
   - Y-as: Monetary (hoeveel geeft klant uit)
   - Kleur: Recency (hoe recent gekocht)
2. **Segmenten**: Verschillende klantgroepen
3. **Grootte**: Bolgrootte = aantal klanten
4. **Positie**: Rechtsboven = beste klanten
""",
        "betekenis": """
**Wat betekent dit?**
- **Champions (555)**: Recente, frequente, big spenders
- **Loyal Customers (X5X)**: Regelmatige kopers
- **At Risk (15X)**: Waren goed, nu inactief
- **New Customers (5XX)**: Recent eerste aankoop
- **Lost (111)**: Lang niet gekocht, lage waarde
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Champions**: VIP behandeling, exclusieve aanbiedingen
✅ **At Risk**: Win-back campagne, persoonlijke benadering
✅ **New Customers**: Welkomstkorting voor 2e aankoop
✅ **Loyal**: Loyaliteitsprogramma, beloningen
✅ **Lost**: Laatste poging of laten gaan
"""
    },
    
    "GF5: Bestellingen Heatmap": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Een heatmap (kleurenkaart)
- Dagen van de week horizontaal (ma-zo)
- Uren van de dag verticaal (0-23)
- Kleuren van licht (weinig) naar donker (veel)
- Getallen in vakjes = aantal bestellingen
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Zoek donkere vlekken**: Drukste momenten
2. **Lichte vlekken**: Rustige momenten
3. **Patronen**: Verticaal = zelfde tijd verschillende dagen
4. **Horizontaal**: Zelfde dag verschillende tijden
5. **Getallen**: Exacte aantallen bestellingen
""",
        "betekenis": """
**Wat betekent dit?**
- **Piekuren**: Wanneer klanten het meest bestellen
- **Daluren**: Rustige periodes
- **Weekpatronen**: Weekend vs doordeweeks
- **Lunch/diner**: Mogelijk pieken rond etenstijd
- **Opening/sluiting**: Activiteit buiten openingstijden?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Personeelsrooster**: Meer mensen tijdens pieken
✅ **Openingstijden**: Aanpassen aan klantgedrag
✅ **Online beschikbaarheid**: 24/7 of beperkt?
✅ **Marketing timing**: Stuur emails voor piekuren
✅ **Capaciteit**: Kan keuken/bezorging pieken aan?
"""
    },
    
    "GF6: Product Categorieën": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Een donut diagram (ring diagram)
- Product categorieën (Kazen, Brood, Dranken, etc.)
- Percentages per categorie
- Verschillende kleuren per segment
- Mogelijk omzetbedragen in legenda
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Segmentgrootte**: Groter = belangrijkere categorie
2. **Percentages**: Aandeel in totale omzet
3. **Gat in midden**: Maakt percentages beter leesbaar
4. **Kleuren**: Elke categorie eigen kleur
5. **Met klok mee**: Van groot naar klein
""",
        "betekenis": """
**Wat betekent dit?**
- **Portfolio balans**: Is assortiment evenwichtig?
- **Specialisatie**: Waar ben je sterk in?
- **Afhankelijkheid**: Te veel leunen op 1 categorie?
- **Groeikansen**: Kleine categorieën met potentie
- **Identiteit**: Wat voor winkel ben je?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Focus**: Versterk top 3 categorieën verder
✅ **Diversificatie**: Als 1 categorie >50%, risico!
✅ **Cross-selling**: Combineer grote met kleine categorieën
✅ **Inkoop**: Onderhandel beste deals voor top categorieën
✅ **Marketing**: Promoot ondervertegenwoordigde categorieën
"""
    },
    
    "GF7: Betaalmethoden": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Staafdiagram of taartdiagram
- Verschillende betaalmethoden (PIN, Cash, Online)
- Aantallen of percentages per methode
- Mogelijk gemiddelde orderwaarde per methode
- Trend over tijd (als lijngrafiek)
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Hoogte/grootte**: Populairste betaalmethode
2. **Vergelijking**: Verschillen tussen methoden
3. **Percentages**: Aandeel van totaal
4. **Trends**: Stijgende/dalende lijnen
5. **Extra info**: Gem. orderwaarde verschillen
""",
        "betekenis": """
**Wat betekent dit?**
- **Klantvoorkeur**: Hoe betalen mensen het liefst
- **Digitalisering**: Shift van cash naar digitaal
- **Orderwaarde**: Online betalers bestellen vaak meer
- **Kosten**: Elke methode heeft andere kosten
- **Fraude risico**: Cash = 0%, online = hoger
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Payment mix**: Optimaliseer beschikbare opties
✅ **Kosten reductie**: Stuur naar goedkoopste methode
✅ **Online push**: Als online hogere orderwaarde
✅ **Cash beleid**: Afbouwen of juist behouden?
✅ **Nieuwe methoden**: Klarna, crypto, etc?
"""
    },
    
    "GF8: Kaas + Brood Combinaties": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Matrix of netwerk diagram
- Kaassoorten en broodsoorten
- Verbindingen = vaak samen gekocht
- Dikte lijnen = frequentie
- Kleuren per producttype
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Knooppunten**: Elk product is een punt
2. **Verbindingen**: Lijnen = samen gekocht
3. **Lijndikte**: Dikker = vaker samen
4. **Clustering**: Producten die bij elkaar horen
5. **Isolatie**: Producten zonder verbindingen
""",
        "betekenis": """
**Wat betekent dit?**
- **Natuurlijke combinaties**: Oude kaas + waldkorn
- **Cross-sell kansen**: Suggesties voor klanten
- **Menu inspiratie**: Combinaties voor proeverijen
- **Voorraad**: Samen in/uit voorraad
- **Plaatsing**: Zet combinaties bij elkaar
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Combideals**: Maak pakketten van populaire combinaties
✅ **Winkelinrichting**: Plaats partners bij elkaar
✅ **Online suggesties**: "Vaak samen gekocht"
✅ **Voorraad**: Bestel combinaties samen
✅ **Marketing**: Promoot nieuwe combinaties
"""
    },
    
    "GF9: Verkooppatronen": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Meerdere lijnen of vlakken
- Verschillende producten/categorieën
- Patronen over tijd (dag/week/maand)
- Mogelijk seizoenscomponenten
- Trend indicatoren
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Tijdas**: Cyclische patronen identificeren
2. **Amplitude**: Hoogte van pieken en dalen
3. **Frequentie**: Hoe vaak patronen terugkeren
4. **Correlaties**: Producten die samen bewegen
5. **Anomalieën**: Uitschieters of verstoringen
""",
        "betekenis": """
**Wat betekent dit?**
- **Weekritme**: Ma rustig, vr/za druk
- **Maandpatroon**: Begin/eind maand effecten
- **Seizoenen**: Zomer/winter verschillen
- **Events**: Feestdagen, vakanties impact
- **Weer**: Invloed op bepaalde producten
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Voorspelbaarheid**: Plan op basis van patronen
✅ **Inventaris**: Cyclische voorraad management
✅ **Promoties**: Timing op natuurlijke dips
✅ **Personeel**: Flexibele roosters op patronen
✅ **Inkoop**: Seizoensgebonden bestellingen
"""
    },
    
    "GF10: Prijsevolutie": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Lijngrafiek met prijzen over tijd
- Verschillende productcategorieën
- Y-as: prijs per kg of per stuk
- X-as: tijd (kwartalen/jaren)
- Mogelijk inflatie benchmark lijn
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Stijgende lijnen**: Prijsverhoging
2. **Dalende lijnen**: Prijsverlaging
3. **Steilheid**: Snelheid van verandering
4. **Vergelijking**: Welke stijgt snelst?
5. **Benchmark**: Boven/onder inflatie?
""",
        "betekenis": """
**Wat betekent dit?**
- **Inflatie impact**: Kostprijsstijgingen
- **Marktpositie**: Kunnen we prijzen doorberekenen?
- **Elasticiteit**: Accepteren klanten verhogingen?
- **Concurrentie**: Hoe doen wij het vs markt?
- **Marge druk**: Stijgen kosten sneller dan prijzen?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Prijsstrategie**: Welke kunnen omhoog/omlaag?
✅ **Communicatie**: Uitleg bij grote stijgingen
✅ **Alternatieven**: Goedkopere opties bieden
✅ **Timing**: Geleidelijk vs shock verhogingen
✅ **Monitoring**: Vergelijk met concurrentie
"""
    },
    
    "GF11: Toekomstvoorspelling": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Historische data (doorgetrokken lijn)
- Voorspelling (stippellijn)
- Onzekerheidsband (gekleurd gebied)
- Trendlijn (mogelijk)
- 12 maanden vooruit
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Geschiedenis**: Basis voor voorspelling
2. **Projectie**: Verwachte ontwikkeling
3. **Band**: Boven/ondergrens (bijv. 95% zekerheid)
4. **Trend**: Algemene richting
5. **Seizoenen**: Terugkerende patronen
""",
        "betekenis": """
**Wat betekent dit?**
- **Groei verwachting**: Stijging of daling?
- **Onzekerheid**: Hoe breed is de band?
- **Planning basis**: Budget en targets
- **Risico's**: Wat als ondergrens realiteit wordt?
- **Kansen**: Wat als bovengrens haalbaar is?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Budgettering**: Gebruik middenscenario
✅ **Scenario planning**: Maak plan B voor ondergrens
✅ **Investeringen**: Bij groei, investeer tijdig
✅ **Kosten**: Bij krimp, reduceer vroeg
✅ **Monitoring**: Vergelijk actual vs forecast maandelijks
"""
    },
    
    "GF12: 55-jaar Voorspelling": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Zeer lange termijn projectie
- Mogelijk generatiewisselingen
- Verschillende scenario's (optimistisch/pessimistisch)
- Belangrijke mijlpalen
- Onzekerheid neemt toe over tijd
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Scenario's**: Verschillende toekomstpaden
2. **Divergentie**: Paden lopen uiteen
3. **Mijlpalen**: Belangrijke momenten
4. **Schaal**: Let op Y-as (lineair/log?)
5. **Aannames**: Welke factoren meegerekend?
""",
        "betekenis": """
**Wat betekent dit?**
- **Legacy planning**: Opvolging strategie
- **Lange termijn trends**: Demografisch, economisch
- **Duurzaamheid**: Is model houdbaar?
- **Innovatie nodig**: Waar vernieuwen?
- **Exit strategie**: Wanneer verkopen/stoppen?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Opvolging**: Start training volgende generatie
✅ **Modernisering**: Investeer in toekomst
✅ **Diversificatie**: Spreid risico's
✅ **Pensioenfonds**: Plan financieel vooruit
✅ **Cultuur**: Documenteer kennis en waarden
"""
    },
    
    "GF13: Seizoens & Feestdagen": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Kalender view of seizoensgrafiek
- Pieken rond feestdagen
- Seizoensgebonden patronen
- Vergelijking tussen jaren
- Event markers (kerst, pasen, etc.)
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Pieken**: Feestdag effecten
2. **Seizoenen**: Zomer/winter verschillen
3. **Consistentie**: Elk jaar hetzelfde?
4. **Grootte**: Welke feest grootste impact?
5. **Timing**: Hoeveel dagen voor/na feest?
""",
        "betekenis": """
**Wat betekent dit?**
- **Voorspelbare pieken**: Plan capaciteit
- **Marketing kansen**: Thema campagnes
- **Voorraad**: Seizoensproducten timing
- **Prijsstrategie**: Premium tijdens pieken?
- **Vakantie impact**: Dips tijdens schoolvakanties?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Jaarkalender**: Markeer alle belangrijke data
✅ **Thema's**: Ontwikkel seizoensaanbiedingen
✅ **Voorinkoop**: Bestel ruim op tijd
✅ **Personeel**: Vakantiespreiding rond pieken
✅ **Marketing**: Start campagnes 2-3 weken vooraf
"""
    },
    
    "GF14: Bestelpatronen": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Lead time analyse (tijd tussen bestellingen)
- Frequentie distributie
- Mogelijk cohort analyse
- Klantgedrag over tijd
- Gemiddelden en spreiding
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Distributie**: Meeste klanten bestellen elke X dagen
2. **Staart**: Extreme waarden (zeer snel/langzaam)
3. **Gemiddelde**: Typische bestelfrequentie
4. **Spreiding**: Hoe consistent is gedrag?
5. **Trends**: Wordt frequentie hoger/lager?
""",
        "betekenis": """
**Wat betekent dit?**
- **Klant ritme**: Natuurlijke bestelcyclus
- **Churn risico**: Te lange tijd = risico
- **Engagement**: Frequentie = betrokkenheid
- **Voorspelling**: Wanneer klant weer bestelt
- **Segmentatie**: Snelle vs langzame klanten
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Reminders**: Stuur op verwachte besteltijd
✅ **Abonnementen**: Bied voor regelmatige klanten
✅ **Re-activatie**: Alert bij uitblijven bestelling
✅ **Loyalty**: Beloon consistente frequentie
✅ **Voorraad**: Plan op basis van patronen
"""
    },
    
    "GF15: Cross-selling": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Product combinatie matrix
- Frequentie samen gekocht
- Lift/confidence scores
- Top combinaties ranking
- Netwerk van relaties
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Matrix cellen**: Donkerder = vaker samen
2. **Lift score**: >1 = bovengemiddeld samen
3. **Top lijst**: Beste combinaties bovenaan
4. **Symmetrie**: A+B = B+A
5. **Clusters**: Groepen die samenhangen
""",
        "betekenis": """
**Wat betekent dit?**
- **Natuurlijke sets**: Producten die horen bij elkaar
- **Suggestie kansen**: Wat kunnen we aanbevelen?
- **Bundle mogelijkheden**: Kant-en-klare pakketten
- **Winkelroute**: Logische productplaatsing
- **Online**: "Anderen kochten ook..."
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Product bundles**: Maak van top 5 combinaties
✅ **Kortingen**: 2e product X% korting
✅ **Plaatsing**: Zet combinaties naast elkaar
✅ **Training**: Leer staff suggesties doen
✅ **Online**: Implementeer recommendation engine
"""
    },
    
    "GF16: Customer Lifetime Value": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- CLV verdeling over klanten
- Histogram of scatter plot
- Segmentatie op waarde
- Mogelijk cohort vergelijking
- Pareto curve (cummulatief)
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Verdeling**: Veel lage CLV, weinig hoge
2. **Top 20%**: Vaak 80% van waarde
3. **Gemiddelde**: Typische klantwaarde
4. **Uitschieters**: Super waardevol/waardeloos
5. **Trend**: Stijgt CLV over tijd?
""",
        "betekenis": """
**Wat betekent dit?**
- **Klantwaarde**: Wie zijn de belangrijksten?
- **Investering**: Hoeveel mag acquisitie kosten?
- **Retentie focus**: Behoud hoge CLV klanten
- **Groei potentie**: Kan lage CLV omhoog?
- **Portfolio gezondheid**: Balans in klantenbestand
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **VIP programma**: Voor top 10% CLV klanten
✅ **Acquisitie budget**: Max 30% van gem CLV
✅ **Retentie**: Focus op top 20% klanten
✅ **Ontwikkeling**: Help midden groep groeien
✅ **Afscheid**: Verliesgevende klanten loslaten
"""
    },
    
    "GF17: Winstgevendheid": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Winstmarges per categorie/product
- Staafdiagram met percentages
- Mogelijk waterval diagram
- ROI per categorie
- Vergelijking met benchmarks
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Hoogte**: Winstmarge percentage
2. **Breedte**: Mogelijk omzetgrootte
3. **Kleuren**: Groen = goed, rood = slecht
4. **Lijn**: Target of industrie gemiddelde
5. **Labels**: Exacte percentages
""",
        "betekenis": """
**Wat betekent dit?**
- **Geldmakers**: Welke producten verdienen echt?
- **Verlieslijders**: Wat kost alleen maar geld?
- **Mix optimalisatie**: Balans volume vs marge
- **Prijsruimte**: Waar kunnen prijzen omhoog?
- **Kosten focus**: Waar moet efficiënter?
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Portfolio**: Push hoge marge producten
✅ **Pricing**: Verhoog waar mogelijk
✅ **Kosten**: Reduceer bij lage marges
✅ **Eliminatie**: Stop met verliesmakers
✅ **Innovatie**: Ontwikkel premium alternatieven
"""
    },
    
    "GF18: Klanten Belonen": {
        "wat_zie_je": """
**Wat zie je op deze grafiek?**
- Loyaliteits tiers (Bronze/Silver/Gold/Platinum)
- Aantal klanten per tier
- Gemiddelde waarde per tier
- Tier progressie over tijd
- Mogelijk churn per tier
""",
        "hoe_lezen": """
**Hoe lees je deze grafiek?**
1. **Piramide**: Veel bronze, weinig platinum
2. **Waarde**: Hogere tiers = meer omzet
3. **Percentages**: Verdeling klantenbestand
4. **Pijlen**: Upgrade/downgrade beweging
5. **Kleuren**: Tier identificatie
""",
        "betekenis": """
**Wat betekent dit?**
- **Loyaliteit**: Wie zijn trouwe klanten?
- **Aspiratie**: Stimulans om te groeien
- **Retentie**: Hogere tiers blijven langer
- **Investering**: ROI van beloningsprogramma
- **Segmentatie**: Verschillende behandeling per tier
""",
        "conclusies": """
**Conclusies & Acties:**
✅ **Tier benefits**: Maak verschil voelbaar
✅ **Upgrade paths**: Communiceer hoe te groeien
✅ **Retentie**: Extra aandacht bij tier daling
✅ **Exclusiviteit**: Platinum echt speciaal maken
✅ **Communicatie**: Personaliseer per tier niveau
"""
    }
}

def get_grafiek_uitleg(visualisatie_naam):
    """
    Haal complete grafiek uitleg op voor een visualisatie
    
    Parameters:
    visualisatie_naam (str): Naam van de visualisatie (bijv. "GF1: Top 20 Producten")
    
    Returns:
    dict: Dictionary met alle uitleg componenten
    """
    return GRAFIEK_UITLEG.get(visualisatie_naam, {
        "wat_zie_je": "Uitleg niet beschikbaar",
        "hoe_lezen": "Uitleg niet beschikbaar", 
        "betekenis": "Uitleg niet beschikbaar",
        "conclusies": "Uitleg niet beschikbaar"
    })

def get_alle_visualisaties():
    """
    Geef lijst van alle visualisaties met uitleg
    
    Returns:
    list: Lijst met namen van alle visualisaties
    """
    return list(GRAFIEK_UITLEG.keys())

# Algemene tips voor grafiek interpretatie
ALGEMENE_GRAFIEK_TIPS = """
## 📊 Algemene Tips voor Grafiek Interpretatie

### 1. **Kijk eerst naar de assen**
- Wat staat er op X-as (horizontaal)?
- Wat staat er op Y-as (verticaal)?
- Let op de schaal (lineair, logaritmisch?)

### 2. **Identificeer de hoofdboodschap**
- Wat springt er direct uit?
- Waar zijn de extremen?
- Wat is het patroon?

### 3. **Zoek naar trends**
- Stijgend, dalend, of stabiel?
- Seizoenspatronen?
- Uitschieters of anomalieën?

### 4. **Vergelijk met verwachtingen**
- Komt dit overeen met je gevoel?
- Zijn er verrassingen?
- Wat verklaart afwijkingen?

### 5. **Denk aan acties**
- Wat betekent dit voor het bedrijf?
- Welke beslissingen kun je nemen?
- Wat moet er veranderen?

### 6. **Wees kritisch**
- Klopt de data?
- Zijn er alternatieve verklaringen?
- Wat wordt NIET getoond?
""" 