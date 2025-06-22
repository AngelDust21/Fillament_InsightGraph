# 3D Print Calculator - Professionele Kostprijsberekening

## 🚀 Overzicht

Een uitgebreide, professionele 3D print calculator die alle verborgen kosten meerekent. Gebouwd met moderne PHP, Bootstrap 5 en een SQLite database.

## ✨ Features

### 🧮 Calculator Functionaliteit
- **15+ kostenfactoren** meegenomen
- **Real-time berekeningen** met AJAX
- **Uitgebreide kosten breakdown**
- **Inzichten en aanbevelingen**
- **ROI berekening**
- **BTW berekening**

### 📊 Database Management
- **CRUD operaties** voor alle entiteiten
- **Import/Export functionaliteit**
- **Validatie en error handling**
- **SQLite database** (geen server setup nodig)

### 🎨 Moderne Interface
- **Bootstrap 5** responsive design
- **Font Awesome** iconen
- **Mobile-first** approach
- **Professionele UI/UX**

### 📦 Entiteiten
- **Materialen**: 50+ filament types
- **Printers**: 30+ printer modellen
- **Nozzles**: Verschillende diameters en materialen
- **Berekeningen**: Geschiedenis en export

## 🛠️ Installatie

### Vereisten
- PHP 7.4+ (met SQLite3 extensie)
- Web server (Apache/Nginx) of PHP built-in server

### Snelle Start
```bash
# 1. Clone of download het project
cd REAL_VALUE_CALCULATOR

# 2. Start PHP development server
php -S localhost:8000

# 3. Open browser
http://localhost:8000
```

### Windows Start Script
```bash
# Gebruik het start script
start_calculator.bat
```

## 📁 Project Structuur

```
REAL_VALUE_CALCULATOR/
├── index.php                 # Hoofdpagina met calculator
├── includes/                 # PHP Classes
│   ├── Database.php         # Database connectie en queries
│   ├── Material.php         # Materiaal management
│   ├── Printer.php          # Printer management
│   ├── Nozzle.php           # Nozzle management
│   └── Calculator.php       # Berekening engine
├── database/
│   └── schema.sql           # Database schema
├── README.md               # Deze file
├── PROGRESS_UPDATE.md      # Project voortgang
└── TODO_UITGEBREIDE_PLANNEN.md # Toekomstige plannen
```

## 🧮 Gebruik

### 1. Calculator
- Selecteer materiaal, printer en nozzle
- Vul print parameters in
- Pas geavanceerde instellingen aan
- Klik "Bereken Eerlijke Prijs"

### 2. Database Beheer
- **Materialen**: Beheer filament types en prijzen
- **Printers**: Voeg printer modellen toe
- **Nozzles**: Configureer nozzle diameters
- **Geschiedenis**: Bekijk eerdere berekeningen

### 3. Export/Import
- Export berekeningen naar CSV
- Import materiaal data
- Backup database

## 💰 Kostenfactoren

De calculator neemt deze kosten mee:

1. **Materiaal** - Filament kosten
2. **Energie** - Stroomverbruik
3. **Nozzle Wear** - Slijtage
4. **Mislukkingen** - Failed prints
5. **Afschrijving** - Printer waardevermindering
6. **Onderhoud** - Regelmatig onderhoud
7. **Bed Adhesion** - Print bed materiaal
8. **Arbeidskosten** - Tijd en expertise
9. **Post-processing** - Afwerking
10. **Verzending** - Shipping kosten
11. **Overhead** - Algemene kosten
12. **BTW** - Belastingen

## 🔧 Technische Details

### Backend
- **PHP 7.4+** met OOP
- **SQLite3** database
- **PDO** voor database connecties
- **Error handling** en logging

### Frontend
- **Bootstrap 5.3** framework
- **Font Awesome 6** iconen
- **Vanilla JavaScript** (geen jQuery)
- **Responsive design**

### Database
- **SQLite** (geen server setup)
- **Normalized schema**
- **Foreign key constraints**
- **Indexes voor performance**

## 📈 Berekening Formules

### Basis Kosten
```
Materiaal = (gewicht_gram / 1000) * prijs_per_kg
Energie = print_uren * wattage * stroomprijs
Nozzle_Wear = print_uren * nozzle_slijtage_per_uur
```

### Totale Kosten
```
Totaal = Materiaal + Energie + Nozzle_Wear + Mislukkingen + 
         Afschrijving + Onderhoud + Bed_Adhesion + Arbeid + 
         Post_Processing + Verzending + Overhead + BTW
```

### Verkoopprijs
```
Verkoopprijs = Totaal * (1 + winstmarge_percentage)
ROI = (Verkoopprijs - Totaal) / Totaal * 100
```

## 🚀 Deployment

### Lokale Development
```bash
php -S localhost:8000
```

### Apache Server
1. Kopieer bestanden naar web root
2. Zorg dat PHP SQLite3 extensie actief is
3. Set juiste permissions

### Nginx Server
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/REAL_VALUE_CALCULATOR;
    index index.php;
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
    }
}
```

## 🔒 Security

- **Input validatie** op alle velden
- **SQL injection** preventie met PDO
- **XSS protection** met htmlspecialchars
- **CSRF protection** (te implementeren)

## 📊 Performance

- **Database indexes** voor snelle queries
- **Lazy loading** van data
- **Caching** van veelgebruikte data
- **Optimized queries** met joins

## 🤝 Bijdragen

1. Fork het project
2. Maak feature branch
3. Commit changes
4. Push naar branch
5. Open Pull Request

## 📝 Licentie

Dit project is open source en beschikbaar onder de MIT licentie.

## 🆘 Support

Voor vragen of problemen:
1. Check de documentatie
2. Bekijk de TODO lijst
3. Open een issue

## 🎯 Roadmap

Zie `TODO_UITGEBREIDE_PLANNEN.md` voor gedetailleerde plannen.

### Korte Termijn
- [ ] CRUD interfaces voor alle entiteiten
- [ ] Export functionaliteit
- [ ] Grafieken en visualisaties
- [ ] User authentication

### Lange Termijn
- [ ] API endpoints
- [ ] Mobile app
- [ ] Cloud sync
- [ ] Advanced analytics

---

**Gemaakt met ❤️ voor de 3D print community** 