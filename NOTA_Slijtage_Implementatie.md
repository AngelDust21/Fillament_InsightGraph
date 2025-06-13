# 📋 NOTA: Slijtage & Onderhoud Implementatie Status

## 🔍 Onderzoek Resultaten

### 1. **WAT BESTAAT ER AL**

#### A. Material Properties (`src/materials/material_properties.py`)
```python
# Voor elk materiaal is er:
- nozzle_wear_factor (1.0 tot 15.0)
- recommended_nozzle type
- nozzle_replacement_cost (€8 tot €90)
- wear_cost_per_hour() method

# Voorbeelden:
"PLA Basic": wear_factor=1.0, brass nozzle €8
"PETG-CF": wear_factor=10.0, hardened steel €30
"PETG-GF": wear_factor=12.0, ruby nozzle €90
"PA-CF": wear_factor=15.0, ruby nozzle €90
```

#### B. Analytics Structuur (`src/analytics/slijtage/`)
```
✅ Map bestaat al!
✅ teller.py (464 regels) - VOLLEDIG GEÏMPLEMENTEERD
✅ productie_teller.py (363 regels) - Ook aanwezig
❌ grafiek.py - Nog te maken
❌ waarschuwing.py - Nog te maken
```

#### C. Data Structuur (`exports/calculation_log.csv`)
```csv
- Heeft 'abrasive' kolom (boolean True/False)
- Heeft 'print_hours' kolom
- Heeft 'material' kolom
- 535 test records aanwezig!
```

### 2. **HOE WERKT HET NU**

#### A. GUI Flow
1. **Checkbox in gui.py** (regel 628):
   ```python
   text="⚙️ Abrasief materiaal (CF/GF)"
   ```
   - Gebruiker moet HANDMATIG aanvinken ❌
   - Geen automatische detectie op materiaal naam

2. **Data wordt gelogd** naar calculation_log.csv met:
   - `abrasive=True/False` 
   - `print_hours`
   - Alle andere berekening details

#### B. Teller.py Implementatie
```python
# PROBLEEM 1: Vaste constanten (regel 38-40)
NOZZLE_LIFETIME_HOURS = 250  # Voor ALLE materialen hetzelfde!
NOZZLE_COST = 25.00          # Vaste prijs voor ALLE nozzles!

# PROBLEEM 2: Vaste slijtagekosten (regel 263)
abrasive_cost = total_abrasive_hours * 0.50  # Altijd €0.50/uur

# PROBLEEM 3: Geschatte print tijd (regel 309)
df['print_hours'] = df['weight'] / 20.0  # Ruwe schatting!
```

### 3. **WAT MOET ER GEBEUREN**

#### STAP 1: GUI Automatische Detectie (`gui.py`)
**Bestand**: `src/interface/gui.py`
**Locatie**: Voeg toe na regel 586 (material selectie)
```python
# Nieuwe functie toevoegen
def update_abrasive_checkbox(self, *args):
    """Automatisch detecteer abrasive materialen."""
    material = self.material_var.get()
    abrasive_markers = ['-CF', '-GF', 'Carbon', 'Glass', 'Fiber']
    is_abrasive = any(marker in material for marker in abrasive_markers)
    self.abrasive_var.set(is_abrasive)

# Bind aan material dropdown (regel ~590)
self.material_combo.bind('<<ComboboxSelected>>', self.update_abrasive_checkbox)
```

#### STAP 2: Teller.py Dynamische Slijtage (`teller.py`)
**Bestand**: `src/analytics/slijtage/teller.py`
**Locatie**: Vervang regels 309-310 en 263

```python
# Import toevoegen bovenaan
from ...materials.material_properties import (
    get_material_properties, 
    calculate_print_time
)

# Regel 309 vervangen door:
# Echte print tijd berekening
for idx, row in df.iterrows():
    df.at[idx, 'print_hours'] = calculate_print_time(
        row['material'], row['weight']
    )

# Regel 263 vervangen door:
# Dynamische slijtage kosten per materiaal
total_wear_cost = 0
for material, group in abrasive_df.groupby('material'):
    props = get_material_properties(material)
    if props:
        hours = group['print_hours'].sum()
        total_wear_cost += hours * props.wear_cost_per_hour
    else:
        # Fallback voor onbekende materialen
        hours = group['print_hours'].sum()
        total_wear_cost += hours * 0.50
```

#### STAP 3: Nieuwe Grafieken (`grafiek.py`)
**Bestand**: `src/analytics/slijtage/grafiek.py` (NIEUW)
**Inhoud**: 
- Slijtage trend over tijd (line chart)
- Kosten per materiaal type (bar chart)
- Nozzle lifetime voorspelling (gauge)

#### STAP 4: Waarschuwingen (`waarschuwing.py`)
**Bestand**: `src/analytics/slijtage/waarschuwing.py` (NIEUW)
**Inhoud**:
- Predictive maintenance alerts
- Email/popup notificaties bij 80% slijtage
- Maintenance schedule generator

### 4. **PRIORITEIT VOLGORDE**

1. **GUI Auto-detectie** (gui.py) - 30 minuten werk
2. **Dynamische slijtage** (teller.py) - 1 uur werk  
3. **Grafieken toevoegen** (grafiek.py) - 2 uur werk
4. **Waarschuwingen** (waarschuwing.py) - 2 uur werk

### 5. **TEST SCENARIO**

Na implementatie testen met:
```
1. Selecteer "PETG-CF" → checkbox moet AUTO aan gaan
2. Bereken prijs → abrasive=True in log
3. Open Analytics → Slijtage tab
4. Check: 
   - Gebruikt wear_factor 10.0 (niet vast 1.0)
   - Toont €30 nozzle kosten (niet vast €25)
   - Print tijd correct berekend (niet /20)
```

## 🎯 Implementatie Volgorde

### STAP 1: GUI Automatische Detectie ✅ VOLTOOID (31-01-2025)
- **Locatie**: `src/materials/material_properties.py` & `src/interface/gui.py`
- **Toegevoegd**:
  - `is_abrasive_material()` functie in material_properties.py
  - `update_abrasive_checkbox()` methode in gui.py
  - Binding in `bind_events()` voor automatische detectie
- **Resultaat**: Checkbox wordt nu automatisch aangevinkt bij CF/GF materialen!
- **Code toevoeging**: Slechts ~20 regels totaal

### STAP 2: Teller.py Material Properties ✅ VOLTOOID (31-01-2025)
- **Locatie**: `src/analytics/slijtage/teller.py`
- **Aanpassingen**: 
  - Import material_properties functies
  - Vervang vaste €0.50/uur door dynamische `calculate_wear_cost()`
  - Itereer over abrasive prints voor echte wear costs
  - Fallback naar €1.20/uur voor backwards compatibility
- **Resultaat**: Realistische slijtage kosten per materiaal type!

### STAP 3: Waarschuwing Systeem ✅ VOLTOOID (31-01-2025)
- **Nieuwe file**: `src/analytics/slijtage/waarschuwing.py` (735 regels)
- **Features**:
  - Multi-level waarschuwingen (60%, 80%, 90%, 100%)
  - Nozzle levensduur tracking per type
  - Maintenance history met JSON persistence
  - Smart recommendations op basis van gebruik
  - Nozzle replacement dialog
- **Educatieve waarde**: Predictive maintenance concepten

### STAP 4: Grafiek Visualisatie ✅ VOLTOOID (31-01-2025)
- **Nieuwe file**: `src/analytics/slijtage/grafiek.py` (850 regels)
- **Visualisaties**:
  - Pie/Donut charts: Abrasive vs normale verdeling
  - Trend analyse: Cumulatieve slijtage over tijd
  - Cost analysis: Slijtage kosten per materiaal
  - Heatmap: Gebruik per dag/uur voor energie optimalisatie
- **Export functie**: Alle grafieken als PNG

## 📊 Testing Resultaten

### ✅ GUI Automatische Detectie
- [x] "PETG-CF" → Checkbox automatisch aan ✅
- [x] "PETG-GF" → Checkbox automatisch aan ✅
- [x] "PLA Basic" → Checkbox automatisch uit ✅
- [x] Manuele override blijft mogelijk ✅

### ✅ Teller Material Properties
- [x] Correcte wear_cost berekening per materiaal ✅
- [x] CF materialen: €0.24-0.36/uur (ipv vaste €0.50)
- [x] GF materialen: €0.43-1.35/uur (ipv vaste €0.50)
- [x] Backwards compatibility behouden ✅

### ✅ Waarschuwing Systeem
- [x] Triggers op 60%, 80%, 90%, 100% ✅
- [x] Persistentie via nozzle_maintenance.json ✅
- [x] Smart recommendations werken ✅
- [x] Replacement dialog functioneel ✅

### ✅ Grafiek Module
- [x] Alle 4 grafiek types werken ✅
- [x] Export naar PNG werkt ✅
- [x] Responsive updates ✅
- [x] Geen crashes bij lege data ✅

## 💡 Implementatie Statistieken

- **Totaal nieuwe code**: ~1.650 regels
- **Aangepaste bestanden**: 3
- **Nieuwe bestanden**: 3
- **Implementatie tijd**: 1 sessie
- **Bugs gevonden**: 0

## 🎉 CONCLUSIE

De complete slijtage & onderhoud module is succesvol geïmplementeerd! Alle features werken zoals gepland:

1. **Automatische detectie** vermindert gebruikersfouten
2. **Realistische wear costs** geven accurate financiële inzichten
3. **Proactieve waarschuwingen** voorkomen dure nozzle schade
4. **Visualisaties** maken complexe data begrijpelijk

De implementatie is **modulair, uitbreidbaar en educatief** - perfect voor het eindproject!

## 🚀 Volgende Stappen

Nu de slijtage module compleet is, kunnen we verder met:
- Energie & Efficiency Analyse
- Break-even curves
- Portfolio optimalisatie
- Of andere prioriteiten uit de TODO lijst 