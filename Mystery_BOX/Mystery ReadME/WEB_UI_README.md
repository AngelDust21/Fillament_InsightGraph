# 🧀 Mystery Box - Web Dashboard

Een interactieve web applicatie voor het bekijken van alle analyses en visualisaties van de Mystery Box bestellingen data.

## 🚀 Snel Starten

### 1. Installeer vereiste packages
```bash
cd "Mystery_BOX/Mystery ReadME"
pip install -r requirements.txt
```

### 2. Start de web applicatie

**Windows (vanuit Mystery ReadME map):**
```bash
start_web_ui.bat
```

**Of handmatig:**
```bash
cd "Mystery_BOX/Mystery ReadME/scripts"
streamlit run streamlit_app.py
```

## 📊 Functies

### Dashboard Overzicht
- **18 interactieve visualisaties** (GF1-GF18)
- **5 categorieën** voor makkelijke navigatie
- **Real-time statistieken** in de sidebar
- **Download functie** voor elke grafiek

### Categorieën

1. **📈 Basis Analyses (DF1-DF4)**
   - Top 20 Producten
   - Omzet Tijdlijn
   - Geografische Spreiding
   - Klanten Segmentatie

2. **🔥 Operationele Inzichten (DF5-DF8)**
   - Bestellingen Heatmap
   - Product Categorieën
   - Betaalmethoden
   - Kaas + Brood Combinaties

3. **📊 Geavanceerde Analyses (DF9-DF12)**
   - Verkooppatronen
   - Prijsevolutie
   - Toekomstvoorspelling
   - 55-jaar Voorspelling

4. **🎯 Marketing & Strategie (DF13-DF15)**
   - Seizoens & Feestdagen
   - Bestelpatronen
   - Cross-selling

5. **💰 Klant & Winst Analyses (DF16-DF18)**
   - Customer Lifetime Value
   - Winstgevendheid
   - Klanten Belonen

## 🛠️ Technische Details

### Architectuur
```
Mystery_BOX/
└── Mystery ReadME/
    ├── data/
    │   └── Bestellingen.csv       # Ruwe data
    ├── scripts/
    │   ├── data_cleaning.py       # Data voorbereiding (114 regels)
    │   ├── data_analyse.py        # Alle berekeningen (1197 regels)
    │   ├── visualisaties.py       # Grafiek generatie (1598 regels)
    │   └── streamlit_app.py       # Web UI (197 regels)
    ├── rapporten/                 # Analyse rapporten
    ├── requirements.txt           # Python dependencies
    └── start_web_ui.bat          # Start script
```

### Data Flow
1. **CSV** → `data_cleaning.py` → Schone data
2. Schone data → `data_analyse.py` → Berekende resultaten (DF1-DF18)
3. Resultaten → `visualisaties.py` → Matplotlib grafieken (GF1-GF18)
4. Grafieken → `streamlit_app.py` → **Web Dashboard**

## 💡 Tips voor Gebruik

### Navigatie
- Gebruik de **sidebar** om tussen analyses te schakelen
- Klik op een **categorie** om de visualisaties te zien
- Selecteer een **specifieke grafiek** met de radio buttons

### Interactie
- **Hover** over grafieken voor details
- **Download** elke grafiek als PNG (300 DPI)
- Gebruik **fullscreen mode** voor presentaties

### Performance
- Eerste keer laden kan even duren (data wordt ingelezen)
- Grafieken worden real-time gegenereerd
- Downloads zijn hoge resolutie voor rapporten

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port already in use" error
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Grafieken laden niet
- Check of alle scripts in de juiste folder staan
- Zorg dat `Bestellingen.csv` in de data folder staat

## 📸 Screenshots

### Hoofddashboard
- Categorie selectie in sidebar
- Live statistieken
- Interactieve grafieken

### Download Functie
- Elke grafiek kan gedownload worden
- Hoge resolutie (300 DPI)
- PNG formaat voor presentaties

## 🔗 Gerelateerde Scripts

- `data_analyse.py` - Voor directe data analyse
- `visualisaties.py` - Voor individuele grafieken
- `eindrapport_bestellingen_analyse.md` - Volledig rapport

## 📝 Updates

**Versie 1.0** (2024)
- Initiële release met alle 18 visualisaties
- Download functionaliteit
- Responsive design 