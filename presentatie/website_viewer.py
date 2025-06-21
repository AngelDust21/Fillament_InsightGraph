import tkinter as tk
from tkinter import ttk
import webview

def open_website():
    """
    Functie om de website te openen in een venster
    """
    # URL van de website die getoond moet worden
    url = "https://akool.com/apps/streaming-avatar/share/MxBm7kCuQt"
    
    # Maak een venster aan met de website
    webview.create_window('Website Viewer', url)
    webview.start()

if __name__ == "__main__":
    # Start de applicatie
    open_website() 