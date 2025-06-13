#!/usr/bin/env python3
"""
Start script voor de H2D Prijs Calculator GUI

Dit script zorgt ervoor dat alle imports correct werken door:
1. Het juiste pad toe te voegen aan sys.path
2. De GUI module correct te importeren
3. De applicatie te starten

Gebruik: python start_gui.py
"""

import sys
import os
import traceback

print("=== H2D Price Calculator Start Script ===")
print(f"Python versie: {sys.version}")

# Voeg de bedrijfsleider directory toe aan het Python path
# Dit zorgt ervoor dat alle relatieve imports werken
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# We voegen de huidige directory (bedrijfsleider) toe, NIET src
sys.path.insert(0, current_dir)
print(f"Python path updated: {sys.path[0]}")

try:
    print("\nImporteren van GUI module...")
    # Nu kunnen we de GUI importeren als een module binnen src
    from src.interface.gui import H2DCalculatorGUI
    print("[OK] GUI module succesvol geimporteerd")
except Exception as e:
    print(f"[FOUT] Fout bij importeren GUI: {e}")
    traceback.print_exc()
    input("\nDruk op Enter om af te sluiten...")
    sys.exit(1)

def main():
    """Start de GUI applicatie"""
    print("[START] H2D Prijs Calculator wordt gestart...")
    
    try:
        # Maak data directory aan als deze niet bestaat
        data_dir = os.path.join(current_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"[INFO] Data directory aangemaakt: {data_dir}")
        
        # Maak en start de GUI
        app = H2DCalculatorGUI()
        print("[OK] GUI succesvol geinitialiseerd")
        print("[INFO] Applicatie venster is geopend...")
        app.run()
        
    except Exception as e:
        print(f"\n[FOUT] Fout bij starten van GUI: {e}")
        print(f"   Type: {type(e).__name__}")
        print("\n[DEBUG] Debug informatie:")
        print(f"   Current dir: {current_dir}")
        print(f"   Python path: {sys.path[:3]}...")
        
        # Print volledige stack trace
        print("\n[TRACE] Volledige foutmelding:")
        traceback.print_exc()
        
        # Extra debug voor import errors
        if isinstance(e, ImportError):
            print("\n[TIP] Tip: Controleer of alle vereiste modules geinstalleerd zijn:")
            print("   pip install pyperclip")
            print("\n[INFO] Verwachte structuur:")
            print("   bedrijfsleider/")
            print("     +-- start_gui.py (dit bestand)")
            print("     +-- src/")
            print("         +-- interface/")
            print("         |   +-- gui.py")
            print("         +-- core/")
            print("         +-- materials/")
            print("         +-- ...")
        
        # Wacht op Enter om venster open te houden
        print("\n[WACHT] Druk op Enter om af te sluiten...")
        input()
        sys.exit(1)
    
    # Als de GUI normaal afsluit
    print("\n[OK] H2D Prijs Calculator is afgesloten")
    print("[WACHT] Druk op Enter om dit venster te sluiten...")
    input()

if __name__ == "__main__":
    main() 