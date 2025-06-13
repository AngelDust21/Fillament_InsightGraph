# TODO - H2D Price Calculator

## Project Status
- **Completion**: **99%** ✨
- **Last Updated**: 31 Januari 2025
- **Focus**: Testing & Documentatie
- **Latest Fix**: Automatische export probleem opgelost

## ✅ OPGELOST - Automatische Export Probleem (31 Jan 2025)

### Probleem Beschrijving
- **ISSUE**: Elke keer bij drukken op "Bereken" werd ALLES opgeslagen in master_calculations.csv
- **GEVOLG**: Master CSV werd vervuild met test berekeningen
- **GEBRUIKER**: Wilde alleen bewust opslaan, niet automatisch
- **LOCATIE**: `gui.py` regel 1563-1589 in `calculate_price()` functie

### Oplossing Geïmplementeerd ✅
1. **Data opslag is nu gesplitst in 3 categorieën:**
   - ✅ `calculation_log.csv` - Simpel logboek (timestamp, materiaal, gewicht, prijs)
   - ✅ `master_calculations.csv` - Alleen voor bewust opgeslagen berekeningen
   - ✅ Producten worden ook naar master geëxporteerd bij opslaan

2. **Wat is gedaan:**
   - ✅ Automatische export verwijderd uit `calculate_price()`
   - ✅ Nieuwe functie `log_calculation_simple()` in DataManager
   - ✅ Export naar master ALLEEN bij:
     - Klik op "Export CSV" knop → exporteert naar gekozen file + master
     - Klik op "Opslaan als Product" → exporteert naar master
   - ❌ Settings optie nog niet toegevoegd (nice-to-have)

3. **Logboek formaat (calculation_log.csv):**
   ```csv
   timestamp,material,weight_g,sell_price
   2025-01-31 10:30:00,PLA Basic,100,15.50
   ```

4. **Master formaat blijft hetzelfde** (met alle details)

### Resultaat
- ✅ Geen vervuiling van master data meer
- ✅ Gebruiker heeft volledige controle
- ✅ Simpel logboek voor tracking
- ✅ Betere performance (minder disk writes)

---

## 🎉 Recent Completions (30-31 Jan)

### Major Architecture Simplification ✅
- **VERWIJDERD**: Aparte JSON product database 
- **VERWIJDERD**: ProductStorage klasse (454 regels code!)
- **VEREENVOUDIGD**: ProductManager leest nu DIRECT uit master_calculations.csv
- **RESULTAAT**: "Less is more" - één centrale data bron!
- **72 producten** automatisch ingeladen uit CSV

### GUI & Data Management
1. **GUI Debugging Voltooid** ✅
   - Alle 4 tabs werken perfect
   - `update_product_stats()` gefixed
   - `get_statistics()` method uitgebreid met avg_margin
   - Indentatie fouten opgelost
   - Product initialisatie errors gefixed

2. **CSV Data Management** ✅
   - Master_calculations.csv als ENIGE databron
   - 72 realistische producten met marketing strategieën
   - Product IDs: numeriek formaat (202505300001)
   - Alle 2024 entries hebben nu productnamen

3. **Overbodige Files Verwijderd** ✅
   - `calc_20250530_022709.csv` (niet gerelateerd)
   - `start_calculator.ps1` (verouderd)
   - `convert_csv_to_products.py` (niet meer nodig)
   - `product_storage.py` (vervangen door directe CSV)
   - `h2d_products.json` (overbodig)

## High Priority Tasks

### 1. Testing Suite (Prioriteit: HOOGSTE)
- [ ] Unit tests voor nieuwe CSV-only ProductManager
- [ ] Integration tests voor GUI met CSV data
- [ ] Edge case testing (lege CSV, corrupte data)
- [ ] Performance testing met 1000+ producten

### 2. Documentatie Update
- [ ] README aanpassen voor nieuwe architectuur
- [ ] User manual updaten (CSV-only workflow)
- [ ] API documentatie voor vereenvoudigde ProductManager

## Medium Priority Tasks

### 3. Error Handling
- [ ] Robuuste CSV parsing (ontbrekende velden)
- [ ] Backup strategie voor master_calculations.csv
- [ ] Recovery mechanisme bij corrupte CSV

### 4. Performance Optimalisatie
- [ ] CSV caching strategie
- [ ] Lazy loading voor grote datasets
- [ ] Incremental updates ipv volledige reload

## Low Priority Tasks

### 5. Nice-to-Have Features
- [ ] CSV import wizard in GUI
- [ ] Geavanceerde filter opties
- [ ] Export naar andere formaten (Excel, PDF)
- [ ] Undo/Redo functionaliteit

## Completed Features ✅

### Core Functionality (100%)
- [x] Prijs berekening engine
- [x] Material cost tracking
- [x] Margin calculaties
- [x] Rush order support

### Product Management (100%)
- [x] CRUD operaties via CSV
- [x] Product search
- [x] Material filtering
- [x] Popularity tracking
- [x] Automatische CSV export

### GUI Implementation (100%)
- [x] Calculator tab
- [x] Products tab
- [x] Materials tab
- [x] Analysis tab
- [x] Responsive layout
- [x] Product tree view met CSV data

### Data Persistence (100%)
- [x] Direct CSV integratie
- [x] Master calculations tracking
- [x] Export functionaliteit
- [x] Een centrale databron

## Architecture Notes

### Vereenvoudigde Data Flow
```
GUI → ProductManager → master_calculations.csv
         ↓
    Memory Cache
```

### Voordelen Nieuwe Architectuur
1. **Simpliciteit**: Één bestand, één waarheid
2. **Transparantie**: CSV is leesbaar in Excel/tekst editor
3. **Geen sync issues**: Geen dubbele data opslag
4. **Minder code**: 500+ regels code verwijderd
5. **Sneller**: Direct CSV access zonder conversie

## Next Sprint Goals
1. Comprehensive testing suite
2. Production deployment guide
3. Performance benchmarking
4. User training materials

## 🏗️ Analytics Module Architectuur Plan

### Probleem: GUI wordt te groot
- `gui.py` is al 2267 regels!
- Analytics toevoegen zou nog eens 1000+ regels zijn
- Moeilijk te onderhouden en debuggen

### Oplossing: Modulaire Analytics Architectuur

#### Folder Structuur:
```
bedrijfsleider/
├── src/
│   ├── interface/
│   │   ├── gui.py          # Hoofd GUI (blijft zoals het is)
│   │   └── gui_analytics.py # Analytics GUI module
│   │
│   └── analytics/          # NIEUWE map voor alle analyses
│       ├── __init__.py
│       ├── base_analysis.py    # Basis klasse voor alle analyses
│       │
│       ├── slijtage/           # Slijtage & Onderhoud
│       │   ├── __init__.py
│       │   ├── teller.py       # Uren teller voor abrasive
│       │   ├── waarschuwing.py # Maintenance waarschuwingen
│       │   └── grafiek.py      # Slijtage visualisaties
│       │
│       ├── energie/            # Energie & Efficiency
│       │   ├── __init__.py
│       │   ├── heatmap.py      # Print activiteit heatmap
│       │   ├── efficiency.py   # Gewicht vs tijd analyse
│       │   └── kosten.py       # Energie kosten calculator
│       │
│       ├── winstgevendheid/    # Break-even & Marges
│       │   ├── __init__.py
│       │   ├── breakeven.py    # Break-even curves
│       │   ├── configuratie.py # Config impact analyse
│       │   └── risico.py       # Risk/reward matrix
│       │
│       └── portfolio/          # Materiaal Portfolio
│           ├── __init__.py
│           ├── pareto.py       # 80/20 analyse
│           └── optimalisatie.py # Portfolio advies
```

#### Implementatie Stappen:

1. **[ ] Maak analytics folder structuur**
   - Alle submappen aanmaken
   - __init__.py files toevoegen

2. **[ ] Implementeer base_analysis.py**
   ```python
   class BaseAnalysis:
       """Basis klasse voor alle analyses"""
       def __init__(self, data_manager):
           self.data_manager = data_manager
           
       def load_data(self):
           """Laad data uit calculation_log.csv"""
           pass
           
       def analyze(self):
           """Voer analyse uit"""
           pass
           
       def create_widgets(self, parent):
           """Maak GUI widgets"""
           pass
   ```

3. **[ ] Maak gui_analytics.py**
   - Aparte klasse `AnalyticsGUI`
   - Notebook met tab voor elke analyse categorie
   - Import alle analyse modules dynamisch

4. **[ ] Link analytics aan hoofdGUI**
   - In gui.py: Import gui_analytics
   - Analytics tab roept `AnalyticsGUI` aan
   - Pass data_manager door

5. **[ ] Implementeer analyses één voor één**
   - Start met break-even (meest educatief)
   - Dan slijtage tracking
   - Dan energie analyse
   - etc.

### Voordelen van deze aanpak:
✅ **Modulariteit**: Elke analyse is onafhankelijk
✅ **Onderhoudbaarheid**: Kleine, focused files
✅ **Testbaarheid**: Elke module apart te testen
✅ **Uitbreidbaarheid**: Nieuwe analyses makkelijk toe te voegen
✅ **Performance**: Lazy loading van analyses
✅ **Clean Code**: Scheiding van verantwoordelijkheden

### Code Voorbeeld:
```python
# In gui.py (analysis tab):
def create_analysis_tab(self):
    # Lazy import om startup snelheid te behouden
    from .gui_analytics import AnalyticsGUI
    
    # Maak analytics instance
    self.analytics_gui = AnalyticsGUI(
        parent=self.analysis_frame,
        data_manager=self.data_manager
    )
    self.analytics_gui.pack(fill='both', expand=True)

# In gui_analytics.py:
class AnalyticsGUI(tk.Frame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager
        self.create_notebook()
        self.load_analyses()
```

Dit houdt de code **proper, netjes en onderhoudbaar**!

## Analytics Tab - REALISTISCHE Implementatie (Gebaseerd op BESCHIKBARE Data)

### PROBLEEM: Geen verkoop/order data → Focus op OPERATIONELE analytics!

### FASE 1: Machine & Materiaal Analytics (Direct Haalbaar)

#### 1. **Slijtage & Onderhoud Dashboard** ✅ VOLTOOID (31-01-2025)
- [x] Teller: Totale uren met abrasieve materialen (CF/GF)
  - **Bestand**: `src/analytics/slijtage/teller.py` ✅ AANGEPAST
  - **Fix**: Dynamische wear_factor ipv vaste €0.50/uur ✅
- [x] Waarschuwing: "Nozzle vervanging na X uur abrasive printing"
  - **Bestand**: `src/analytics/slijtage/waarschuwing.py` ✅ GEMAAKT
  - **Features**: Multi-level warnings, maintenance history, smart recommendations
- [x] Grafiek: Abrasive vs normale materialen over tijd
  - **Bestand**: `src/analytics/slijtage/grafiek.py` ✅ GEMAAKT
  - **Visualisaties**: Pie charts, trend lines, cost analysis, heatmaps
- [x] Kosten impact: Extra slijtage kosten per print
  - **Bestand**: `teller.py` gebruikt nu echte material properties ✅
- [x] **GUI Fix**: Automatische abrasive detectie
  - **Bestand**: `src/interface/gui.py` ✅ GEÏMPLEMENTEERD
  - **Toegevoegd**: `update_abrasive_checkbox()` functie + binding

#### 2. **Energie & Efficiency Analyse**
- [ ] Heatmap: Print activiteit per uur/dag (voor stroom tarieven)
- [ ] Scatter: Gewicht vs print tijd (efficiency per materiaal)
- [ ] Staafdiagram: Gemiddelde kWh per materiaaltype
- [ ] Kosten analyse: Dag vs nacht tarief optimalisatie

#### 3. **Multicolor/AMS Gebruik Analyse**
- [ ] Donut chart: % prints met/zonder multicolor
- [ ] Impact analyse: Extra setup kosten vs marge
- [ ] Combinatie matrix: Multicolor × Rush × Abrasive
- [ ] Trend: Toename/afname multicolor gebruik

#### 4. **Winstgevendheid per Configuratie**
- [ ] Bubble chart: Gewicht vs Marge% vs Frequentie
- [ ] Top 10: Meest winstgevende parameter combinaties
- [ ] Bottom 10: Minst winstgevende prints (red flags)
- [ ] Break-even curve: Bij welk gewicht per materiaal

### FASE 2: Operationele Insights (Week 2)

#### 5. **Winstgevendheid Patronen (Educatief)**
- [ ] Break-even curves: Minimaal gewicht per materiaal voor winst
- [ ] Correlatie matrix: Welke parameters correleren met hoge winst
- [ ] Risk/Reward scatter: Marge% vs Variabiliteit
- [ ] Best practices: Top 10 meest succesvolle configuraties

#### 6. **Materiaal Portfolio Optimalisatie**
- [ ] Pareto: 80/20 analyse (welke materialen = 80% winst)
- [ ] Dode voorraad: Materialen nooit gebruikt
- [ ] Kruis-analyse: Materiaal × Opties × Marge
- [ ] Advies: "Drop deze materialen" / "Focus op deze"

#### 7. **Configuratie Impact Dashboard**
- [ ] Slider analyse: Impact van elke config parameter
- [ ] What-if: "Als energy_price +10%, dan..."
- [ ] Optimale settings suggester
- [ ] Historische config changes vs marge

### FASE 3: Predictive Analytics (Later)

#### 8. **Machine Maintenance Predictor**
- [ ] Voorspelling: Volgende onderhoud op basis van gebruik
- [ ] Kosten projectie: Onderhoudsbudget per kwartaal
- [ ] Risico analyse: Kans op storing bij huidige gebruik

#### 9. **Smart Pricing Suggesties**
- [ ] ML model: Optimale prijs op basis van historische marges
- [ ] Clustering: Groepeer similaire prints
- [ ] Anomalie detectie: Ongewone berekeningen

#### 10. **NIEUW: Verkoop Registratie Toevoegen**
- [ ] Simpele "Verkoop Registreren" knop in Products tab
- [ ] sales_log.csv: timestamp, product_id, quantity, price
- [ ] Dan pas: Echte omzet/verkoop analytics mogelijk!

### Educatieve Focus van Analytics

**Wat we WEL kunnen analyseren (met logboek data):**
1. **Break-even analyse** - Bij welk gewicht wordt print winstgevend?
2. **Configuratie optimalisatie** - Welke settings geven beste marge?
3. **Risk assessment** - Welke combinaties zijn gevaarlijk?
4. **Portfolio management** - 80/20 regel voor materialen
5. **Anomalie detectie** - Ongewone berekeningen spotten

**Wat we NIET kunnen (zonder verkoop data):**
- Echte verkoop aantallen
- Klant segmentatie
- Seizoenspatronen
- Order frequentie

### Implementatie Prioriteit

**Start met deze 3 (hoogste educatieve waarde):**
1. **Break-even Curves** - Direct toepasbaar, visueel duidelijk
2. **Config Impact Dashboard** - Sliders voor "what-if" scenarios
3. **Risk Matrix** - 2D plot van marge vs variabiliteit

**Libraries:** Blijf bij matplotlib (geen extra dependencies)

Dit geeft studenten **praktische business inzichten** uit echte data!