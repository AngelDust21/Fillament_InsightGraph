# 📋 NOTA: Slijtage & Onderhoud Code Analyse

## 📍 Huidige Status

### ✅ WAT ER AL IS:

1. **Material Properties** (`src/materials/material_properties.py`)
   - Bevat `nozzle_wear_factor` voor elk materiaal
   - CF materialen: wear_factor 8.0-15.0 (hoge slijtage)
   - GF materialen: wear_factor 12.0-15.0 (extreme slijtage)
   - Normale materialen: wear_factor 1.0-2.0
   - Berekent `wear_cost_per_hour()`

2. **Cost Engine** (`src/core/cost_engine.py`)
   - Heeft `abrasive` boolean parameter
   - Berekent `surcharge_abrasive` (€0.50/uur)
   - Wordt doorgegeven aan `CostBreakdown`

3. **Analytics Module** (`src/analytics/slijtage/`)
   - Map bestaat al! ✅
   - `teller.py` - 464 regels - VOLLEDIG GEÏMPLEMENTEERD
   - `productie_teller.py` - 363 regels

4. **Data Logging** (`exports/calculation_log.csv`)
   - Master calculations CSV wordt gebruikt
   - Bevat `abrasive` kolom (boolean)
   - Bevat `print_hours` kolom

5. **GUI Integration** 
   - `gui_analytics.py` laadt analytics modules
   - `create_analysis_tab()` in `gui.py` 

### ❌ WAT ONTBREEKT:

1. **Print Hours**
   - Wordt GESCHAT op basis van gewicht (20g/uur)
   - Geen echte print_hours uit material properties
   
2. **Koppeling Material Properties**
   - `teller.py` gebruikt NIET de wear_factor uit material_properties
   - Gebruikt vaste €0.50/uur voor ALLE abrasive materialen

## 📂 Map Structuur

```
bedrijfsleider/
├── src/
│   ├── analytics/
│   │   ├── slijtage/
│   │   │   ├── __init__.py      ✅ Bestaat
│   │   │   ├── teller.py        ✅ Volledig geïmplementeerd
│   │   │   ├── productie_teller.py ✅ Bestaat
│   │   │   ├── waarschuwing.py  ❌ Nog te maken
│   │   │   └── grafiek.py       ❌ Nog te maken
│   │   │
│   │   └── base_analysis.py     ✅ Base class voor alle analyses
│   │
│   ├── materials/
│   │   └── material_properties.py ✅ Bevat wear factors
│   │
│   └── interface/
│       ├── gui.py              ✅ Hoofdinterface
│       └── gui_analytics.py    ✅ Analytics loader
│
└── exports/
    ├── master_calculations.csv  ✅ Hoofddata
    └── calculation_log.csv      ✅ Simpel logboek
```

## 🔧 Bestaande Functionaliteit in `teller.py`

### Wat het AL doet:
1. **Telt totale uren** met abrasieve materialen
2. **Berekent slijtagekosten** (€0.50/uur vast)
3. **Nozzle wear percentage** (op basis van 250 uur levensduur)
4. **Vervangingen teller** (hoeveel keer nozzle vervangen)
5. **Periode analyses** (vandaag/week/maand/totaal)
6. **Waarschuwingen** bij 80% slijtage
7. **Mooie GUI** met progress bars en statistieken

### Code Fragmenten:

```python
# Constantes in teller.py
NOZZLE_LIFETIME_HOURS = 250  # Gemiddelde levensduur
NOZZLE_COST = 25.00          # Vervangingskosten
WARNING_THRESHOLD = 0.8       # 80% waarschuwing

# Slijtage berekening (VAST €0.50/uur)
abrasive_cost = total_abrasive_hours * 0.50
```

## 🚀 TODO: Verbeteringen

### 1. **Koppel Material Properties**
   - Gebruik ECHTE wear_factor per materiaal
   - Bereken dynamische slijtagekosten ipv vaste €0.50
   - Toon aanbevolen nozzle type

### 2. **Gebruik Echte Print Hours**
   - Haal print speed uit material_properties
   - Bereken accurate print_hours ipv schatting

### 3. **Nieuwe Features**
   - `waarschuwing.py` - Predictive maintenance
   - `grafiek.py` - Slijtage trends over tijd

### 4. **Data Verbetering**
   - Track nozzle type per print
   - Log maintenance events
   - Voorspel volgende onderhoud

## 📊 Bestaande Data Flow

```
GUI Berekening
    ↓
calculate_price() [gui.py]
    ↓
log_calculation_simple() [data_manager.py]
    ↓
calculation_log.csv (met abrasive boolean)
    ↓
AbrasiveTeller.load_data() [teller.py]
    ↓
Analyse & Visualisatie
```

## ⚡ Quick Wins

1. **Print Hours Fix**
   ```python
   # In teller.py, regel ~309
   # NU: df['print_hours'] = df['weight'] / 20.0
   # BETER: Gebruik material_properties speed
   ```

2. **Dynamische Slijtage**
   ```python
   # In teller.py
   # NU: abrasive_cost = hours * 0.50
   # BETER: abrasive_cost = hours * material.wear_cost_per_hour
   ```

3. **Material Info Toevoegen**
   ```python
   # Toon recommended_nozzle uit material_properties
   # Toon echte wear_factor per materiaal
   ```

## 🎯 Conclusie

De basis is er al! De `teller.py` werkt en toont mooie visualisaties. 
Hoofdprobleem: gebruikt VASTE waardes ipv dynamische material properties.

**Prioriteit**: Koppel de bestaande material_properties aan de teller voor
realistische slijtage berekeningen per materiaal type.

## 🎮 GUI Implementatie Details

### Abrasive Checkbox
In `gui.py` (regels 627-635):
```python
self.abrasive_check = tk.Checkbutton(
    options_frame,
    text="⚙️ Abrasief materiaal (CF/GF)",
    variable=self.abrasive_var,
    font=("Arial", 10),
    bg=self.colors['white'],
    command=self.calculate_price
)
```

### Gebruik in Calculate Price
In `gui.py` (regel 1547):
```python
abrasive=self.abrasive_var.get()  # Boolean option
```

### ⚠️ PROBLEEM: Geen Automatische Detectie!
- Gebruiker moet HANDMATIG checkbox aanvinken
- Geen automatische detectie op basis van materiaal naam
- CF/GF materialen worden NIET automatisch herkend

## 🔨 PRIORITEIT FIXES

### 1. **Automatische Abrasive Detectie** (HOOGSTE PRIORITEIT)
```python
# In gui.py, on_input_change() of material selectie:
def check_abrasive_material(self, material_name):
    """Automatisch detecteer abrasive materialen."""
    abrasive_materials = ['-CF', '-GF', 'CF ', 'GF ', 'Carbon', 'Glass']
    is_abrasive = any(marker in material_name for marker in abrasive_materials)
    self.abrasive_var.set(is_abrasive)
```

### 2. **Koppel Material Properties aan Teller**
```python
# In teller.py, analyze():
from ...materials.material_properties import get_material_properties

# Voor elk materiaal in de data:
props = get_material_properties(material_name)
if props:
    wear_cost = props.wear_cost_per_hour * print_hours
else:
    wear_cost = 0.50 * print_hours  # Fallback
```

### 3. **Echte Print Hours Berekening**
```python
# In teller.py, vervang:
df['print_hours'] = df['weight'] / 20.0

# Door:
from ...materials.material_properties import calculate_print_time
df['print_hours'] = df.apply(
    lambda row: calculate_print_time(row['material'], row['weight']), 
    axis=1
)
```

## 📝 Implementatie Stappenplan

1. **STAP 1: Automatische Abrasive Detectie** (gui.py)
   - Voeg material change handler toe
   - Update abrasive checkbox automatisch
   - Gebruiker kan nog steeds overschrijven

2. **STAP 2: Material Properties Integratie** (teller.py)
   - Import material_properties functies
   - Gebruik echte wear_factor per materiaal
   - Bereken dynamische slijtagekosten

3. **STAP 3: Nieuwe Grafieken** (grafiek.py)
   - Slijtage trend over tijd
   - Kosten per materiaal type
   - Nozzle lifetime voorspelling

4. **STAP 4: Waarschuwingen Systeem** (waarschuwing.py)
   - Predictive maintenance alerts
   - Email/popup notificaties
   - Maintenance schedule generator

## 🎯 Expected Results

Na implementatie:
- ✅ CF/GF materialen worden AUTOMATISCH herkend
- ✅ Slijtagekosten zijn DYNAMISCH per materiaal
- ✅ Print tijden zijn ACCURAAT berekend
- ✅ Gebruikers krijgen PROACTIEVE waarschuwingen
- ✅ Data-driven maintenance planning mogelijk 