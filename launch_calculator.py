#!/usr/bin/env python3
"""
Universele launcher voor H2D Price Calculator
============================================

Dit script kan van overal worden uitgevoerd en zal altijd correct werken.
"""

import os
import sys
import subprocess

# Bepaal waar DIT script staat
script_dir = os.path.dirname(os.path.abspath(__file__))

print("🚀 H2D Price Calculator Universal Launcher")
print(f"📁 Script locatie: {script_dir}")

# Voeg de bedrijfsleider directory toe aan Python path
sys.path.insert(0, script_dir)

# Change naar de juiste directory
os.chdir(script_dir)
print(f"📂 Working directory: {os.getcwd()}")

# Start de GUI
try:
    # Importeer en start direct
    from src.interface.gui import H2DCalculatorGUI
    
    print("✅ GUI module geladen")
    print("🖥️  Starting GUI...")
    
    app = H2DCalculatorGUI()
    app.run()
    
except Exception as e:
    print(f"\n❌ Fout bij starten: {e}")
    print("\n💡 Probeer alternatief: start_gui.py")
    
    # Als directe import faalt, probeer via subprocess
    try:
        subprocess.run([sys.executable, "start_gui.py"], check=True)
    except:
        print("\n❌ Beide methodes gefaald!")
        input("\nDruk Enter om af te sluiten...")
        sys.exit(1) 