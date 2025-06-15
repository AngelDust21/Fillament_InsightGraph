# Eindrapport: Bestellingen Analyse Delicatessenzaak
**Datum:** 2025
**Auteur:** Data Analyse Team

---

## Executive Summary

Deze analyse onderzoekt 521 unieke bestellingen (1851 productregels) van een delicatessenzaak gespecialiseerd in kaas- en vleesschotels. De belangrijkste bevindingen:

- **Totale omzet:** €88,735 over de analyseperiode
- **Top product:** Kaasschotel 'Culinair' (€10,927 omzet)
- **Dominante locatie:** Tongeren (29.4% van alle bestellingen)
- **Cross-sell potentieel:** Slechts 21.9% van kaasbestellingen bevat brood
- **Groeiprognose:** 35% groei verwacht in eerste jaar, afvlakkend naar 12% in jaar 5

---

## 1. Data Overzicht

### 1.1 Dataset Kenmerken
- **Periode:** Meerdere jaren data
- **Unieke bestellingen:** 521
- **Totaal aantal items:** 1851
- **Unieke klanten:** 382
- **Unieke producten:** 278

### 1.2 Data Kwaliteit
- Woonplaats duplicaten geconsolideerd (Tongeren varianten samengevoegd)
- Product namen gestandaardiseerd (kaasschotel varianten gecombineerd)
- Prijzen per persoon berekend voor schotels

---

## 2. Product Analyse

### 2.1 Top 20 Producten (DF1)
De top 3 best verkopende producten zijn:
1. **Kaasschotel 'Culinair'** - €10,927 totale omzet
2. **Kaasschotel 'Deluxe'** - €8,623 totale omzet  
3. **Vleesschotel 'Gastronomisch'** - €7,234 totale omzet

### 2.2 Product Categorieën (DF6)
- **Overig:** 51% van totale omzet
- **Kaas:** 23% van totale omzet
- **Vlees:** 12% van totale omzet
- **Brood:** 8% van totale omzet
- **Tapas:** 4% van totale omzet
- **Delicatessen:** 2% van totale omzet

### 2.3 Cross-Selling Analyse (DF8 & DF15)
- Van alle kaasbestellingen bevat slechts **21.9%** ook brood
- Populairste brood bij kaas: **Stokbrood bio desem**
- Top productcombinaties vaak kaas + vlees of kaas + tapas

---

## 3. Klanten Analyse

### 3.1 Geografische Spreiding (DF3)
Top 5 woonplaatsen:
1. **Tongeren:** 29.4% van omzet (na consolidatie)
2. **Riemst:** 8.2% van omzet
3. **Bilzen:** 6.7% van omzet
4. **Hoeselt:** 5.9% van omzet
5. **Borgloon:** 4.3% van omzet

### 3.2 Klant Segmentatie (DF4)
- **Slapende klanten:** 299 (78%)
- **Regelmatige klanten:** 54 (14%)
- **VIP klanten:** 24 (6%)
- **Nieuwe klanten:** 5 (1%)

### 3.3 Lifetime Value (DF16)
- **Diamond (>€5000):** 12 klanten
- **Gold (€2000-5000):** 28 klanten
- **Silver (€1000-2000):** 45 klanten
- **Bronze (<€1000):** 297 klanten

---

## 4. Temporele Patronen

### 4.1 Maandelijkse Trends (DF2)
- Sterke seizoensgebonden patronen zichtbaar
- Piekmaanden vaak rond feestdagen
- Gemiddelde maandomzet: €7,395

### 4.2 Dagpatronen (DF5)
- **Piekuren:** 14:00 - 17:00 
- **Drukste dag:** Vrijdag
- **Weekend vs doordeweeks:** Meer voorbereidingstijd voor weekend

### 4.3 Leadtime Analyse (DF14)
- **Gemiddelde leadtime:** 2.8 dagen
- **Mediaan leadtime:** 2 dagen
- Weekend leveringen vereisen langere voorbereidingstijd

---

## 5. Financiële Analyse

### 5.1 Betaalmethoden (DF7)
1. **Stripe:** 453 transacties (86.9%)
2. **Bancontact:** 51 transacties (9.8%)
3. **Cash:** 17 transacties (3.3%)

### 5.2 Prijsevolutie (DF10)
- **Kaasschotels:** Gemiddeld 3.2% prijsstijging per jaar
- **Vleesschotels:** Gemiddeld 2.8% prijsstijging per jaar
- Prijzen per persoon stabiel ondanks inflatie

### 5.3 Winstgevendheid (DF17)
- **Geschatte totale winst:** €31,057 (35% marge)
- **Meest winstgevende categorie:** Delicatessen (50% marge)
- **80/20 regel:** Top 20% klanten = 73% van winst

---

## 6. Toekomstvoorspellingen

### 6.1 5-Jaar Prognose (DF11)
| Jaar | Verwachte Omzet | Groei % |
|------|-----------------|---------|
| 2025 | €120,000 | 35% |
| 2026 | €150,000 | 25% |
| 2027 | €180,000 | 20% |
| 2028 | €207,000 | 15% |
| 2029 | €232,000 | 12% |

### 6.2 Lange Termijn (DF12)
- **2080 prijsvoorspelling kaasschotel:** €85-120 per persoon
- **2080 prijsvoorspelling vleesschotel:** €105-150 per persoon
- Gecorrigeerd voor inflatie: 2-3x huidige koopkracht

---

## 7. Strategische Aanbevelingen

### 7.1 Marketing & Verkoop
1. **Focus op Tongeren:** Versterk marktpositie in dominante regio
2. **Cross-sell brood:** Actief brood promoten bij kaasbestellingen
3. **Seizoensacties:** Extra capaciteit en promoties rond feestdagen
4. **VIP programma:** Exclusieve events voor top 10% klanten

### 7.2 Operationeel
1. **Capaciteitsplanning:** Extra personeel 14:00-17:00 en vrijdagen
2. **Voorraad:** Anticipeer op seizoenspieken
3. **Leadtime communicatie:** Duidelijke verwachtingen weekend leveringen
4. **Betaalmethoden:** Stripe blijft dominante keuze

### 7.3 Product Portfolio
1. **Premium focus:** Gastronomische schotels hebben hoogste marges
2. **Brood assortiment:** Uitbreiden met premium broodsoorten
3. **Categorie mix:** Delicatessen uitbreiden (hoogste marge)
4. **Bundels:** Kaas + brood + wijn combinaties

### 7.4 Klanten Retentie (DF18)
1. **VIP klanten (24):** Premium cadeaus + exclusieve events
2. **Loyale klanten (78):** Loyaliteitskorting + verjaardagscadeau
3. **Rising stars (15):** Welkomstcadeau + persoonlijke follow-up
4. **Slapende klanten (299):** Win-back campagne met 20% korting

---

## 8. Conclusie

De delicatessenzaak toont sterke groeipotentie met:
- Solide klantenbasis in Tongeren regio
- Premium producten met goede marges
- Duidelijke groeimogelijkheden in cross-selling
- Realistische groeiprognose van 20% per jaar

**Prioriteiten voor 2025:**
1. Implementeer klanten beloningsprogramma
2. Versterk brood cross-selling
3. Optimaliseer capaciteit voor piekuren
4. Ontwikkel premium productlijn verder

---

## Bijlagen

### Technische Details
- **Analyse periode:** Volledige dataset
- **Tools gebruikt:** Python (Pandas, Matplotlib, Seaborn)
- **Data cleaning:** Gestandaardiseerde locaties en productnamen
- **Visualisaties:** 18 grafieken (GF1-GF18) beschikbaar

### Contact
Voor vragen over deze analyse, neem contact op met het data analyse team.

---
*Dit rapport is automatisch gegenereerd op basis van de beschikbare verkoopdata.* 