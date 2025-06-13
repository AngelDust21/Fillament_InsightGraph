"""
Product Charts Module - H2D Price Calculator
===========================================

Deze module biedt uitgebreide visualisaties voor product analyses
met een scrollbare interface voor meerdere grafieken.

Grafieken:
---------
1. Prijs Verdeling - Histogram van verkoopprijzen
2. Materiaal Analyse - Taartdiagram van materiaal gebruik
3. Marge Trends - Lijn grafiek van marges over tijd
4. Gewicht vs Prijs - Scatter plot met correlatie
5. Top Producten - Bar chart van meest winstgevende
6. Tijdlijn - Productie volume over tijd

EDUCATIEF DOEL:
--------------
Laat zien hoe data visualisatie inzicht geeft in:
- Welke producten het meest winstgevend zijn
- Welke materialen het meest gebruikt worden
- Hoe prijzen zich verhouden tot gewicht
- Trends in productie over tijd

Vereisten:
---------
- matplotlib voor grafieken
- tkinter voor scrollbare interface
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np

from .product_model import Product
from .product_manager import ProductManager


class ProductCharts:
    """Scrollbare product visualisatie interface.
    
    Toont 6 verschillende grafieken in een scrollbaar canvas
    met realtime updates vanuit de product database.
    """
    
    def __init__(self, parent: tk.Widget, product_manager: ProductManager, colors: Dict[str, str]):
        """Initialiseer charts module.
        
        Parameters:
        ----------
        parent : tk.Widget
            Parent widget voor de charts
        product_manager : ProductManager
            Manager voor product data toegang
        colors : Dict[str, str]
            Kleurenschema van hoofdGUI
        """
        self.parent = parent
        self.product_manager = product_manager
        self.colors = colors
        
        # Maak scrollbaar frame
        self.create_scrollable_frame()
        
        # Maak alle grafieken
        self.create_all_charts()
        
    def create_scrollable_frame(self) -> None:
        """Creëer scrollbaar canvas voor grafieken."""
        # Hoofdframe
        self.main_frame = tk.Frame(self.parent, bg=self.colors['bg'])
        self.main_frame.pack(fill='both', expand=True)
        
        # Canvas voor scroll
        self.canvas = tk.Canvas(self.main_frame, bg=self.colors['bg'])
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        # Configureer canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame binnen canvas voor content
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        # Bind resize events
        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Bind muiswiel voor scrollen
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_frame_configure(self, event=None) -> None:
        """Update scroll region bij frame resize."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def _on_canvas_configure(self, event=None) -> None:
        """Update canvas window breedte bij resize."""
        canvas_width = event.width if event else self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
    def _on_mousewheel(self, event) -> None:
        """Scroll met muiswiel."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def create_all_charts(self) -> None:
        """Creëer alle 6 grafieken in scrollbaar frame."""
        # Haal producten op
        products = self.product_manager.list_all()
        
        if not products:
            self._show_no_data_message()
            return
            
        # Chart 1: Prijs Verdeling
        self.create_price_distribution(products)
        
        # Chart 2: Materiaal Analyse
        self.create_material_analysis(products)
        
        # Chart 3: Marge Trends
        self.create_margin_trends(products)
        
        # Chart 4: Gewicht vs Prijs
        self.create_weight_price_scatter(products)
        
        # Chart 5: Top Producten
        self.create_top_products_bar(products)
        
        # Chart 6: Productie Tijdlijn
        self.create_production_timeline(products)
        
        # Update scroll region
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        
    def _show_no_data_message(self) -> None:
        """Toon bericht als geen data beschikbaar."""
        msg_frame = tk.Frame(self.scrollable_frame, bg=self.colors['white'], 
                           relief=tk.RAISED, bd=1)
        msg_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            msg_frame,
            text="📊 Geen product data beschikbaar",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(pady=50)
        
        tk.Label(
            msg_frame,
            text="Maak eerst enkele producten aan om grafieken te zien",
            font=("Arial", 11),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack()
        
    def create_price_distribution(self, products: List[Product]) -> None:
        """Chart 1: Histogram van verkoopprijzen."""
        frame = self._create_chart_frame("💰 Prijs Verdeling")
        
        # Maak figure
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Data
        prices = [p.sell_price for p in products if p.sell_price > 0]
        
        # Plot histogram
        ax.hist(prices, bins=20, color=self.colors['primary'], alpha=0.7, edgecolor='black')
        ax.set_xlabel('Verkoopprijs (€)')
        ax.set_ylabel('Aantal Producten')
        ax.set_title('Verdeling van Product Prijzen')
        ax.grid(True, alpha=0.3)
        
        # Voeg statistieken toe
        if prices:
            avg_price = np.mean(prices)
            ax.axvline(avg_price, color='red', linestyle='--', linewidth=2, 
                      label=f'Gemiddeld: €{avg_price:.2f}')
            ax.legend()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def create_material_analysis(self, products: List[Product]) -> None:
        """Chart 2: Taartdiagram van materiaal gebruik."""
        frame = self._create_chart_frame("🧵 Materiaal Analyse")
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Tel materialen
        material_counts = {}
        for p in products:
            material_counts[p.material] = material_counts.get(p.material, 0) + 1
            
        # Plot pie chart
        if material_counts:
            materials = list(material_counts.keys())
            counts = list(material_counts.values())
            
            colors_list = plt.cm.Set3(np.linspace(0, 1, len(materials)))
            wedges, texts, autotexts = ax.pie(counts, labels=materials, autopct='%1.1f%%',
                                              colors=colors_list, startangle=90)
            
            # Maak percentages beter leesbaar
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')
                
            ax.set_title('Materiaal Gebruik Verdeling')
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def create_margin_trends(self, products: List[Product]) -> None:
        """Chart 3: Marge trends over tijd."""
        frame = self._create_chart_frame("📈 Marge Trends")
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Sorteer op datum
        sorted_products = sorted(products, key=lambda p: p.created_at)
        
        # Groepeer per dag
        daily_margins = {}
        for p in sorted_products:
            date_key = p.created_at.date()
            if date_key not in daily_margins:
                daily_margins[date_key] = []
            if p.margin_pct > 0:
                daily_margins[date_key].append(p.margin_pct)
                
        # Bereken gemiddelde per dag
        if daily_margins:
            dates = sorted(daily_margins.keys())
            avg_margins = [np.mean(daily_margins[d]) for d in dates]
            
            ax.plot(dates, avg_margins, marker='o', linewidth=2, 
                   markersize=6, color=self.colors['secondary'])
            ax.fill_between(dates, avg_margins, alpha=0.3, color=self.colors['secondary'])
            
            ax.set_xlabel('Datum')
            ax.set_ylabel('Gemiddelde Marge (%)')
            ax.set_title('Marge Ontwikkeling Over Tijd')
            ax.grid(True, alpha=0.3)
            
            # Roteer x-labels
            fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def create_weight_price_scatter(self, products: List[Product]) -> None:
        """Chart 4: Scatter plot gewicht vs prijs."""
        frame = self._create_chart_frame("⚖️ Gewicht vs Prijs Analyse")
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Data
        weights = [p.weight_g for p in products if p.weight_g > 0 and p.sell_price > 0]
        prices = [p.sell_price for p in products if p.weight_g > 0 and p.sell_price > 0]
        
        if weights and prices:
            # Scatter plot
            scatter = ax.scatter(weights, prices, alpha=0.6, s=50, 
                               c=prices, cmap='viridis')
            
            # Trendlijn
            z = np.polyfit(weights, prices, 1)
            p = np.poly1d(z)
            ax.plot(weights, p(weights), "r--", alpha=0.8, 
                   label=f'Trend: €{z[0]:.3f}/gram')
            
            ax.set_xlabel('Gewicht (gram)')
            ax.set_ylabel('Verkoopprijs (€)')
            ax.set_title('Correlatie Gewicht en Prijs')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Colorbar
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Prijs (€)')
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def create_top_products_bar(self, products: List[Product]) -> None:
        """Chart 5: Top 10 meest winstgevende producten."""
        frame = self._create_chart_frame("🏆 Top Winstgevende Producten")
        
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Sorteer op winstmarge
        profitable = sorted([p for p in products if p.margin_pct > 0], 
                          key=lambda p: p.margin_pct, reverse=True)[:10]
        
        if profitable:
            names = [p.name[:20] + '...' if len(p.name) > 20 else p.name for p in profitable]
            margins = [p.margin_pct for p in profitable]
            
            # Maak bar chart
            bars = ax.barh(names, margins, color=self.colors['success'])
            
            # Voeg waarden toe
            for bar, margin in zip(bars, margins):
                width = bar.get_width()
                ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                       f'{margin:.1f}%', ha='left', va='center')
            
            ax.set_xlabel('Winstmarge (%)')
            ax.set_title('Top 10 Meest Winstgevende Producten')
            ax.grid(True, axis='x', alpha=0.3)
            
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def create_production_timeline(self, products: List[Product]) -> None:
        """Chart 6: Productie volume over tijd."""
        frame = self._create_chart_frame("📅 Productie Tijdlijn")
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Groepeer per week
        weekly_counts = {}
        for p in products:
            # Bepaal week start
            week_start = p.created_at.date() - timedelta(days=p.created_at.weekday())
            weekly_counts[week_start] = weekly_counts.get(week_start, 0) + 1
            
        if weekly_counts:
            weeks = sorted(weekly_counts.keys())
            counts = [weekly_counts[w] for w in weeks]
            
            # Bar chart
            ax.bar(weeks, counts, width=6, color=self.colors['primary'], alpha=0.7)
            
            ax.set_xlabel('Week')
            ax.set_ylabel('Aantal Producten')
            ax.set_title('Productie Volume per Week')
            ax.grid(True, axis='y', alpha=0.3)
            
            # Roteer labels
            fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_chart_frame(self, title: str) -> tk.Frame:
        """Maak frame voor individuele chart."""
        # Container
        container = tk.LabelFrame(
            self.scrollable_frame,
            text=title,
            font=("Arial", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.RAISED,
            bd=1
        )
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chart frame
        chart_frame = tk.Frame(container, bg='white')
        chart_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        return chart_frame
        
    def refresh_charts(self) -> None:
        """Herlaad alle grafieken met nieuwe data."""
        # Verwijder oude charts
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Maak nieuwe charts
        self.create_all_charts()


# Voorbeeld gebruik en test
if __name__ == "__main__":
    # Test window
    root = tk.Tk()
    root.title("Product Charts Test")
    root.geometry("900x700")
    
    # Test kleuren
    colors = {
        'bg': '#f0f0f0',
        'primary': '#2196F3',
        'secondary': '#FF9800',
        'success': '#4CAF50',
        'white': '#FFFFFF',
        'text': '#212121'
    }
    
    # Maak dummy product manager
    from product_manager import ProductManager
    pm = ProductManager()
    
    # Maak charts
    charts = ProductCharts(root, pm, colors)
    
    root.mainloop() 