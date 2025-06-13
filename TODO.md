# TODO - H2D Price Calculator
*Laatst bijgewerkt: 5 februari 2025* ⚡ **BIJGEWERKT MET ACTUELE STATUS**

## 🏗️ ARCHITECTUUR OVERZICHT

### HUIDIGE BESTANDSSTRUCTUUR (ACTUELE STATUS)

```
bedrijfsleider/
├── start_gui.py              ✅ BESTAAT - Hoofdprogramma launcher
├── launch_calculator.py      ✅ BESTAAT - Alternatieve launcher
├── requirements.txt          ✅ BESTAAT - Python dependencies
├── TODO.md                   ✅ DIT BESTAND (BIJGEWERKT!)
│
├── exports/                  ✅ BESTAAT - Data opslag
│   ├── calculation_log.csv   ✅ BESTAAT - ALLE berekeningen
│   ├── master_calculations.csv ✅ BESTAAT - Bewuste exports
│   ├── berekeningen/        ✅ BESTAAT - Map voor individuele exports
│   ├── producten/           ✅ BESTAAT - Product export files
│   └── analyses/            ✅ BESTAAT - Analyse exports
│
└── src/                     ✅ BESTAAT - Source code
    ├── __init__.py          ✅ BESTAAT
    │
    ├── interface/           ✅ BESTAAT - User interfaces
    │   ├── gui.py           ✅ BESTAAT - Hoofd GUI (2425 regels!)
    │   ├── gui_analytics.py ✅ BESTAAT - Analytics GUI controller (461 regels)
    │   ├── cli.py           ✅ BESTAAT - Command line interface
    │   └── (uitleg files)   ✅ BESTAAT - Documentatie
    │
    ├── core/                ✅ BESTAAT - Business logica
    │   ├── calculator.py    ✅ BESTAAT - Prijs berekeningen
    │   └── cost_engine.py   ✅ BESTAAT - Kosten motor
    │
    ├── materials/           ✅ BESTAAT - Materiaal systeem
    │   ├── materials.py     ✅ BESTAAT - Materiaal definities
    │   └── material_properties.py ✅ BESTAAT - Properties (snelheden etc)
    │
    ├── products/            ✅ BESTAAT - Product management
    │   ├── product_model.py ✅ BESTAAT - Product data model
    │   ├── product_manager.py ✅ BESTAAT - Product CRUD operations
    │   └── product_charts.py ✅ BESTAAT - 6 product grafieken
    │
    ├── analytics/           ✅ BESTAAT - Analytics framework
    │   ├── base_analysis.py ✅ BESTAAT - Abstract base class (235 regels)
    │   ├── generate_test_data.py ✅ BESTAAT - Test data generator
    │   ├── sample_data_generator.py ✅ BESTAAT - Sample data helper
    │   │
    │   ├── basis/           ✅ VOLLEDIG GEÏMPLEMENTEERD! 🎉
    │   │   ├── __init__.py  ✅ BESTAAT - Module exports
    │   │   ├── dagelijkse_activiteit.py ✅ KLAAR - 379 regels, 3 grafieken
    │   │   ├── materiaal_gebruik.py ✅ KLAAR - 369 regels, 3 grafieken
    │   │   └── print_waardes.py ✅ KLAAR - 414 regels, 3 grafieken
    │   │
    │   ├── slijtage/        ✅ VOLLEDIG GEÏMPLEMENTEERD!
    │   │   ├── __init__.py  ✅ BESTAAT
    │   │   ├── teller.py    ✅ KLAAR - Abrasive uren teller (464 regels)
    │   │   └── productie_teller.py ✅ KLAAR - Productie calculator (363 regels)
    │   │
    │   ├── energie/         ❌ NOG LEEG (alleen __init__.py)
    │   ├── winstgevendheid/ ❌ NOG LEEG (alleen __init__.py)
    │   └── portfolio/       ❌ NOG LEEG (alleen __init__.py)
    │
    ├── config/              ✅ BESTAAT - Configuratie
    └── utils/               ✅ BESTAAT - Hulp functies
```

## 🎯 WAT IS AL KLAAR

### ✅ VOLLEDIG WERKENDE MODULES:

1. **Calculator Core** ✅
   - Volledig werkende prijs calculator
   - Material kosten berekening
   - Arbeidskosten, energie, overhead
   - Rush orders & multicolor support

2. **Data Management** ✅
   - 3-tier CSV systeem (log, master, exports)
   - 31 kolommen met complete details
   - Auto-save bij elke berekening

3. **Material System** ✅
   - 15+ materialen gedefinieerd
   - Properties: snelheid, dichtheid, prijs
   - Abrasive material support

4. **Product Management** ✅
   - CRUD operaties
   - Product catalogus
   - 6 werkende grafieken

5. **Analytics Framework** ✅
   - BaseAnalysis abstract class
   - Data caching
   - GUI integratie

6. **Slijtage Module** ✅ COMPLEET
   - AbrasiveTeller: uren tracking
   - ProductieTeller: productie stats
   - Beide met meerdere grafieken

7. **Basis Statistieken Module** ✅ COMPLEET! 🎉
   - DagelijkseActiviteit: 3 grafieken (trend, weekdag, heatmap)
   - MateriaalGebruik: 3 grafieken (taart, bar, histogram)
   - PrintWaardes: 3 grafieken (box plot, scatter, histogram)

## 🚧 WAT MOET ER NOG GEBOUWD WORDEN

### 1. KOSTEN ANALYSE MODULE - `src/analytics/kosten/`
**NIEUW TE MAKEN DIRECTORY**

#### Te maken bestanden:
```
src/analytics/kosten/
├── __init__.py              ❌ NIEUW - Module exports
├── marge_analyse.py         ❌ NIEUW - Winstmarge analyses
├── kosten_breakdown.py      ❌ NIEUW - Kosten structuur
└── prijs_patronen.py        ❌ NIEUW - Pricing patterns
```

##### `marge_analyse.py` zal bevatten:
- Class: `MargeAnalyse(BaseAnalysis)`
- Grafiek 1: Lijn grafiek - gemiddelde marge % over tijd
- Grafiek 2: Scatter plot - gewicht vs marge % met trendlijn
- Grafiek 3: Box plot - marge verdeling per materiaal

##### `kosten_breakdown.py` zal bevatten:
- Class: `KostenBreakdown(BaseAnalysis)`
- Grafiek 1: Gestapelde bar - materiaal vs arbeid vs energie
- Grafiek 2: Taart diagram - gemiddelde kosten verdeling
- Grafiek 3: Area chart - kosten ontwikkeling over tijd

##### `prijs_patronen.py` zal bevatten:
- Class: `PrijsPatronen(BaseAnalysis)`
- Grafiek 1: Bar chart - gemiddelde prijs per gram per materiaal
- Grafiek 2: Lijn grafiek - prijs trends over maanden
- Grafiek 3: Histogram - verkoop prijs frequentie

### 2. BUSINESS INSIGHTS MODULE - `src/analytics/business/`
**NIEUW TE MAKEN DIRECTORY**

#### Te maken bestanden:
```
src/analytics/business/
├── __init__.py              ❌ NIEUW - Module exports
├── configuratie_populariteit.py ❌ NIEUW - Populaire combos
├── order_type_vergelijking.py   ❌ NIEUW - Rush vs normal
└── size_impact_analysis.py      ❌ NIEUW - Size efficiency
```

##### `configuratie_populariteit.py` zal bevatten:
- Class: `ConfiguratiePopulariteit(BaseAnalysis)`
- Grafiek 1: Heatmap - materiaal vs gewicht categorieën matrix
- Grafiek 2: Bubble chart - materiaal populariteit (size=aantal, color=prijs)
- Grafiek 3: Stacked bar - normale vs multicolor vs spoed verdeling

##### `order_type_vergelijking.py` zal bevatten:
- Class: `OrderTypeVergelijking(BaseAnalysis)`
- Grafiek 1: Group bar chart - rush vs normal pricing
- Grafiek 2: Box plot - prijs verschillen per order type
- Grafiek 3: Pie chart - % rush vs normal orders

##### `size_impact_analysis.py` zal bevatten:
- Class: `SizeImpactAnalysis(BaseAnalysis)`
- Grafiek 1: Scatter plot - gewicht vs prijs per gram (efficiency curve)
- Grafiek 2: Line chart - break-even punten per materiaal
- Grafiek 3: Histogram - print tijd categorieën

### 3. ENERGIE MODULE INVULLEN - `src/analytics/energie/`
**DIRECTORY BESTAAT, MODULES ONTBREKEN**

#### Te maken bestanden:
```
src/analytics/energie/
├── __init__.py              ✅ BESTAAT (maar leeg)
├── verbruik_analyse.py      ❌ NIEUW - Energie verbruik per print
├── kosten_trends.py         ❌ NIEUW - Energie kosten over tijd
└── efficiency_metrics.py    ❌ NIEUW - kWh per gram/uur metrics
```

### 4. WINSTGEVENDHEID MODULE - `src/analytics/winstgevendheid/`
**DIRECTORY BESTAAT, MODULES ONTBREKEN**

#### Te maken bestanden:
```
src/analytics/winstgevendheid/
├── __init__.py              ✅ BESTAAT (maar leeg)
├── profit_trends.py         ❌ NIEUW - Winst ontwikkeling
├── top_performers.py        ❌ NIEUW - Best renderende prints
└── margin_distribution.py   ❌ NIEUW - Marge verdeling
```

### 5. PORTFOLIO MODULE - `src/analytics/portfolio/`
**DIRECTORY BESTAAT, MODULES ONTBREKEN**

#### Te maken bestanden:
```
src/analytics/portfolio/
├── __init__.py              ✅ BESTAAT (maar leeg)
├── product_mix.py           ❌ NIEUW - Product portfolio analyse
├── customer_insights.py     ❌ NIEUW - Klant patronen
└── growth_metrics.py        ❌ NIEUW - Groei indicatoren
```

## ⚠️ BELANGRIJKE UPDATES

### GUI Analytics Integratie
`gui_analytics.py` is al voorbereid voor ALLE modules:
- ✅ Basis statistieken tab werkt al!
- ⏳ Kosten/Business tabs tonen placeholder
- ⏳ Energie/Winstgevendheid/Portfolio nog niet in GUI

### Data Structuur
De basis modules gebruiken `master_calculations.csv` succesvol:
- Proven data loading pattern in BaseAnalysis
- Caching werkt perfect
- Error handling aanwezig

## 🎯 NIEUWE IMPLEMENTATIE VOLGORDE

### FASE 1: Kosten Analyse ⭐ PRIORITEIT
Dit is het meest logische volgende:
1. Maak directory `src/analytics/kosten/`
2. Begin met `marge_analyse.py`
3. Gebruik `DagelijkseActiviteit` als template
4. Test met echte data
5. Integreer in gui_analytics.py

### FASE 2: Energie Module
Vul de bestaande lege directory:
1. Kopieer structuur van basis module
2. Focus op energie verbruik metrics
3. Link aan printer_power_kw kolom

### FASE 3: Winstgevendheid
Bouw voort op kosten analyse:
1. Profit trends over tijd
2. Top performing products
3. ROI metrics

### FASE 4: Business Insights
Geavanceerde analyses:
1. Configuratie populariteit
2. Order type vergelijking
3. Size impact

### FASE 5: Portfolio
Strategische overzichten:
1. Product mix optimalisatie
2. Klant segmentatie
3. Groei projecties

## 📋 CHECKLIST VOOR NIEUWE MODULES

- [ ] Gebruik een werkende module als template (bijv. `dagelijkse_activiteit.py`)
- [ ] Inherit van BaseAnalysis
- [ ] Implementeer `get_title()`, `analyze()`, `create_analysis_widgets()`
- [ ] Maak 3 grafieken per module
- [ ] Test met `master_calculations.csv`
- [ ] Update `__init__.py` met exports
- [ ] Nederlandse UI teksten
- [ ] Matplotlib figures met juiste kleuren schema

## 🚫 NIET MEER NODIG

- ❌ Basis module bouwen (AL KLAAR!)
- ❌ Slijtage module aanpassen (WERKT PERFECT!)
- ❌ gui_analytics.py basis structuur (BESTAAT AL!)

## 💡 QUICK START NIEUWE MODULE

```python
# Kopieer deze template voor nieuwe modules:
from ..base_analysis import BaseAnalysis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import tkinter as tk
from tkinter import ttk

class NieuweAnalyse(BaseAnalysis):
    def __init__(self, data_manager=None, parent_frame=None, colors=None):
        super().__init__(data_manager, parent_frame, colors)
        self.name = "Nieuwe Analyse"
        
    def get_title(self) -> str:
        return "📊 Nieuwe Analyse"
        
    def create_analysis_widgets(self):
        df = self.get_data()
        if df.empty:
            self.show_no_data_message()
            return
            
        # Notebook voor tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Maak 3 tabs met grafieken
        # ... zie dagelijkse_activiteit.py voor voorbeelden
```

Deze TODO is nu volledig up-to-date! Begin met FASE 1: Kosten Analyse! 🚀