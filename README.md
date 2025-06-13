# 🎯 Fillament InsightGraph

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)](https://www.microsoft.com/windows)

Een geavanceerde **3D Print Prijs Calculator** met ingebouwde slijtage-analyse en filament tracking. Ontwikkeld voor H2D om nauwkeurige prijsberekeningen te maken voor 3D print projecten.

## ✨ Kernfuncties

### 📊 **Prijsberekening**
- Automatische kostprijsberekening op basis van:
  - Materiaalverbruik (filament)
  - Printtijd en energie
  - Slijtage van onderdelen
  - Overhead kosten

### 🔧 **Slijtage Tracking**
- Real-time monitoring van printer onderdelen
- Voorspellend onderhoud waarschuwingen
- Nozzle levensduur tracking
- Productie teller voor statistieken

### 📈 **Analytics Dashboard**
- Dagelijkse activiteit overzichten
- Materiaalgebruik analyses
- Winstgevendheid rapporten
- Export mogelijkheden (CSV, Excel)

### 🖥️ **Moderne Interface**
- Intuïtieve GUI gebouwd met Tkinter
- Dark/Light mode ondersteuning
- Clipboard integratie voor snelle kopieerfunctie
- Responsive design

## 🚀 Snelstart

### Vereisten
- Python 3.7 of hoger
- Windows 10/11
- 100MB vrije schijfruimte

### Installatie

1. **Clone deze repository:**
```bash
git clone https://github.com/AngelDust21/Fillament_InsightGraph.git
cd Fillament_InsightGraph
```

2. **Installeer dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start de applicatie:**
```bash
python start_gui.py
```

Of gebruik één van de meegeleverde shortcuts:
- `start_calculator.bat` (dubbelklik)
- `start_calculator.ps1` (PowerShell)

## 📁 Project Structuur

```
Fillament_InsightGraph/
├── start_gui.py              # Hoofd startpunt voor de applicatie
├── start_calculator.bat      # Windows batch script
├── start_calculator.ps1      # PowerShell script
├── requirements.txt          # Project dependencies
├── src/                      # Broncode
│   ├── core/                # Kern berekeningslogica
│   ├── interface/           # GUI componenten
│   ├── analytics/           # Data analyse modules
│   ├── config/              # Configuratie bestanden
│   └── utils/               # Hulp functies
├── data/                    # Data bestanden
├── exports/                 # Export directory
└── presentatie/            # Presentatie materialen
```

## 🔬 Technische Details

### Gebruikte Technologieën
- **Python 3.7+** - Hoofdprogrammeertaal
- **Tkinter** - GUI Framework
- **Tabulate** - Tabel formatting
- **Pyperclip** - Clipboard functionaliteit
- **JSON** - Data opslag
- **CSV** - Export formaat

### Architectuur
Het project volgt een modulaire MVC architectuur:
- **Model**: Core pricing en cost engines
- **View**: Tkinter GUI interface
- **Controller**: Business logic en data flow

## 📚 Documentatie

Gedetailleerde documentatie is beschikbaar in de volgende bestanden:
- [HOE_TE_STARTEN.md](HOE_TE_STARTEN.md) - Installatie en gebruik
- [TODO.md](TODO.md) - Roadmap en geplande features
- [NOTA_Slijtage_Implementatie.md](NOTA_Slijtage_Implementatie.md) - Technische implementatie details
- [NOTA_Slijtage_Onderhoud.md](NOTA_Slijtage_Onderhoud.md) - Onderhoudsrichtlijnen

## 🤝 Bijdragen

Dit is een privé project voor H2D. Voor vragen of suggesties, neem contact op met de ontwikkelaar.

## 👩‍💻 Ontwikkelaar

**Soffia Moës**  
Student Software Development  
Contact: [Via GitHub](https://github.com/AngelDust21)

## 📄 Licentie

Dit project is eigendom van Soffia Moës en ontwikkeld voor H2D. Alle rechten voorbehouden.

---

<p align="center">
  <strong>Fillament InsightGraph</strong> - Slimme 3D Print Calculaties 🚀
</p> 