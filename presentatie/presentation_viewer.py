import tkinter as tk
from tkinter import ttk, messagebox
import webview
import os
import subprocess
import sys
from pathlib import Path

def show_presentation():
    """
    Functie om de h2d_price_calculator presentatie te tonen
    """
    presentatie_map = Path(__file__).parent
    
    # Zoek eerst naar PDF versie
    pdf_bestand = presentatie_map / "h2d_price_calculator_presentation.pdf"
    
    if pdf_bestand.exists():
        # Toon PDF in webview venster
        print(f"PDF presentatie wordt geladen: {pdf_bestand.name}")
        file_url = f"file:///{pdf_bestand.absolute().as_posix()}"
        webview.create_window('H2D Price Calculator Presentatie (PDF)', file_url)
        webview.start()
        
if __name__ == "__main__":
    show_presentation() 