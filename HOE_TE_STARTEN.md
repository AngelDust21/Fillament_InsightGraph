# 🚀 HOE START IK DE H2D PRIJS CALCULATOR?

## ✅ SNELSTE METHODE - Dubbelklik!

1. **Windows Explorer:**
   - Open de folder `Eind Examen\bedrijfsleider\`
   - Dubbelklik op: `start_calculator.bat`
   - Klaar! 🎉

## 🔧 ALTERNATIEVE METHODES

### Methode 1: PowerShell Script
```powershell
# Rechtsklik op start_calculator.ps1
# Kies "Run with PowerShell"
```

### Methode 2: Command Line
```bash
cd "Eind Examen\bedrijfsleider"
python start_gui.py
```

### Methode 3: Direct vanuit elke locatie
```bash
python "C:\Users\soffi\Desktop\Eind Examen\bedrijfsleider\start_gui.py"
```

## ❌ WAT WERKT NIET

**NIET DOEN:**
```bash
# Dit geeft een import error!
python src/interface/gui.py
```

**WAAROM?** De GUI gebruikt relatieve imports die alleen werken als je de applicatie start via het speciale start script.

## 🐛 PROBLEMEN OPLOSSEN

### "Python niet gevonden"
- Installeer Python: https://www.python.org
- Zorg dat "Add to PATH" aangevinkt is tijdens installatie

### "ModuleNotFoundError: pyperclip"
```bash
pip install pyperclip
```

### "ImportError: attempted relative import"
- Gebruik ALLEEN de start scripts!
- Start NOOIT gui.py direct

## 📂 BESTANDSSTRUCTUUR

```
bedrijfsleider/
├── start_gui.py              ← START DIT! ✅
├── start_calculator.bat      ← OF DIT! ✅
├── start_calculator.ps1      ← OF DIT! ✅
├── start_calculator_direct.bat ← OF DIT! ✅
└── src/
    └── interface/
        └── gui.py            ← NIET direct starten! ❌
```

## 💡 PRO TIP

Maak een snelkoppeling op je bureaublad:
1. Rechtsklik op `start_calculator.bat`
2. Kies "Create shortcut"
3. Sleep naar bureaublad
4. Hernoem naar "H2D Calculator"

---

**Laatste update:** Januari 2025
**Door:** Soffia Moës 