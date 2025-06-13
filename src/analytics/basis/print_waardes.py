"""
Print Waardes Analyse Module
=============================

Analyseert de typische waardes van prints (gewicht, tijd, prijs).
Bevat 3 visualisaties:
1. Box plot - gewicht spreiding per materiaal
2. Scatter plot - gewicht vs print tijd
3. Histogram - prijs verdeling
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import os

from ..base_analysis import BaseAnalysis


class PrintWaardes(BaseAnalysis):
    """Analyse van print waardes (gewicht, tijd, prijs)."""
    
    def __init__(self, data_manager=None, parent_frame=None, colors=None):
        """Initialiseer Print Waardes analyse."""
        super().__init__(data_manager, parent_frame, colors)
        self.name = "Print Waardes Analyse"
        self.figures = {}
        self.canvases = {}
        
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "📊 Print Waardes Analyse"
        
    def get_data(self):
        """Laad data voor analyses uit master_calculations.csv."""
        # Gebruik alleen master_calculations.csv als primaire bron
        df = self.load_data()
        
        # Rename kolommen voor compatibiliteit
        if 'weight' in df.columns and 'weight_g' not in df.columns:
            df['weight_g'] = df['weight']
            
        # Debug: print beschikbare kolommen
        print(f"DEBUG print_waardes - Beschikbare kolommen: {df.columns.tolist() if not df.empty else 'GEEN DATA'}")
        print(f"DEBUG print_waardes - Aantal rijen: {len(df)}")
            
        return df
            
    def create_analysis_widgets(self):
        """Creëer de analyse widgets."""
        # Haal data op
        df = self.get_data()
        
        if df.empty:
            self.show_no_data_message()
            return
            
        # Maak notebook voor de 3 grafieken
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Box plot gewicht per materiaal
        self.create_weight_boxplot_tab(df)
        
        # Tab 2: Scatter plot gewicht vs tijd
        self.create_weight_time_scatter_tab(df)
        
        # Tab 3: Histogram prijs verdeling
        self.create_price_histogram_tab(df)
        
        # Status label met algemene stats
        avg_weight = df['weight_g'].mean()
        avg_price = df['sell_price'].mean()
        avg_margin = df['margin_pct'].mean()
        
        status_text = f"📊 Gemiddelden: {avg_weight:.0f}g | €{avg_price:.2f} | Marge: {avg_margin:.1f}%"
        
        self.status_label = tk.Label(
            self.main_frame,
            text=status_text,
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.status_label.pack(pady=5)
        
    def create_weight_boxplot_tab(self, df):
        """Tab 1: Box plot van gewicht spreiding per materiaal."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="📦 Gewicht Spreiding")
        
        # Selecteer top 10 materialen
        top_materials = df['material'].value_counts().head(10).index
        filtered_df = df[df['material'].isin(top_materials)]
        
        # Maak figuur
        fig = Figure(figsize=(12, 8), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Bereid data voor per materiaal
        data_to_plot = []
        labels = []
        
        for material in top_materials:
            material_weights = filtered_df[filtered_df['material'] == material]['weight_g']
            data_to_plot.append(material_weights.values)
            labels.append(material)
        
        # Maak box plot
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                       notch=True, showmeans=True)
        
        # Kleuren voor boxes
        colors_list = plt.cm.Set3(np.linspace(0, 1, len(bp['boxes'])))
        
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Stijl de boxplot elementen
        for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color='black')
        
        # Draai x-labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Styling
        ax.set_xlabel('Materiaal Type', fontsize=12)
        ax.set_ylabel('Gewicht (gram)', fontsize=12)
        ax.set_title('Gewicht Spreiding per Materiaal Type', fontsize=14, pad=20)
        ax.grid(True, axis='y', alpha=0.3)
        
        # Voeg annotaties toe voor outliers
        ax.text(0.98, 0.98, '○ = outliers\n□ = mean\n— = median',
               transform=ax.transAxes, fontsize=9,
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Statistieken tabel
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Bereken Q1, Q3 en IQR voor totale dataset
        q1 = df['weight_g'].quantile(0.25)
        q3 = df['weight_g'].quantile(0.75)
        iqr = q3 - q1
        median = df['weight_g'].median()
        
        stats_text = f"📊 Totale Dataset: " \
                    f"Q1: {q1:.0f}g | " \
                    f"Mediaan: {median:.0f}g | " \
                    f"Q3: {q3:.0f}g | " \
                    f"IQR: {iqr:.0f}g | " \
                    f"Outliers: {len(df[(df['weight_g'] < q1 - 1.5*iqr) | (df['weight_g'] > q3 + 1.5*iqr)])}"
        
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        self.figures['boxplot'] = fig
        self.canvases['boxplot'] = canvas
        
    def create_weight_time_scatter_tab(self, df):
        """Tab 2: Scatter plot van gewicht vs prijs."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="💰 Gewicht vs Prijs")
        
        # Filter extreme outliers voor betere visualisatie
        df_filtered = df[(df['weight_g'] < df['weight_g'].quantile(0.99)) & 
                        (df['sell_price'] < df['sell_price'].quantile(0.99))]
        
        # Maak figuur
        fig = Figure(figsize=(10, 8), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Kleur op basis van materiaal categorie
        def get_material_category(material):
            if 'CF' in material or 'Carbon' in material or 'Glass' in material:
                return 'Composiet'
            elif 'PLA' in material:
                return 'PLA Varianten'
            elif material in ['PC', 'Nylon', 'ASA', 'ABS']:
                return 'Technisch'
            else:
                return 'Overig'
        
        df_filtered['category'] = df_filtered['material'].apply(get_material_category)
        
        # Kleurenmap
        color_map = {
            'PLA Varianten': self.colors['primary'],
            'Technisch': self.colors['secondary'],
            'Composiet': '#FF6B6B',
            'Overig': '#95A5A6'
        }
        
        # Plot per categorie
        for category, color in color_map.items():
            category_data = df_filtered[df_filtered['category'] == category]
            ax.scatter(category_data['weight_g'], category_data['sell_price'],
                      alpha=0.6, s=30, c=color, label=category, edgecolors='black', linewidth=0.5)
        
        # Voeg trendlijn toe
        z = np.polyfit(df_filtered['weight_g'], df_filtered['sell_price'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(df_filtered['weight_g'].min(), df_filtered['weight_g'].max(), 100)
        ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, 
                label=f'Trend: €{z[0]:.3f}/g')
        
        # Bereken correlatie
        correlation = df_filtered['weight_g'].corr(df_filtered['sell_price'])
        
        # Styling
        ax.set_xlabel('Gewicht (gram)', fontsize=12)
        ax.set_ylabel('Verkoopprijs (€)', fontsize=12)
        ax.set_title(f'Relatie tussen Gewicht en Prijs (r={correlation:.3f})', 
                    fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Voeg info box toe
        info_text = f'n = {len(df_filtered)}\nCorrelatie: {correlation:.3f}'
        ax.text(0.05, 0.95, info_text,
               transform=ax.transAxes, fontsize=10,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Prijs statistieken per categorie
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Bereken gemiddelde prijs per gram voor verschillende categorieën
        df_filtered['price_per_gram'] = df_filtered['sell_price'] / df_filtered['weight_g']
        
        price_stats = df_filtered.groupby('category')['price_per_gram'].mean()
        
        stats_text = "💰 Gem. Prijs per Gram: " + " | ".join(
            [f"{cat}: €{price:.3f}/g" for cat, price in price_stats.items()]
        )
        
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        self.figures['scatter'] = fig
        self.canvases['scatter'] = canvas
        
    def create_price_histogram_tab(self, df):
        """Tab 3: Histogram van prijs verdeling."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="💰 Prijs Verdeling")
        
        # Filter extreme outliers
        df_filtered = df[df['sell_price'] < df['sell_price'].quantile(0.98)]
        
        # Maak figuur met 2 subplots
        fig = Figure(figsize=(12, 8), facecolor=self.colors['bg'])
        
        # Subplot 1: Algemene prijs verdeling
        ax1 = fig.add_subplot(2, 1, 1)
        
        # Histogram
        n, bins, patches = ax1.hist(df_filtered['sell_price'], bins=50, 
                                   color=self.colors['primary'], alpha=0.7, 
                                   edgecolor='black', linewidth=0.5)
        
        # Voeg gemiddelde en mediaan lijnen toe
        mean_price = df_filtered['sell_price'].mean()
        median_price = df_filtered['sell_price'].median()
        
        ax1.axvline(mean_price, color='red', linestyle='dashed', linewidth=2,
                   label=f'Gemiddelde: €{mean_price:.2f}')
        ax1.axvline(median_price, color='green', linestyle='dashed', linewidth=2,
                   label=f'Mediaan: €{median_price:.2f}')
        
        # Kleur bins op basis van prijs ranges
        for i, patch in enumerate(patches):
            if bins[i] < 20:
                patch.set_facecolor('#3498DB')  # Blauw voor goedkoop
            elif bins[i] < 50:
                patch.set_facecolor(self.colors['primary'])  # Groen voor normaal
            elif bins[i] < 100:
                patch.set_facecolor('#F39C12')  # Oranje voor duur
            else:
                patch.set_facecolor('#E74C3C')  # Rood voor premium
        
        ax1.set_xlabel('Verkoop Prijs (€)', fontsize=12)
        ax1.set_ylabel('Frequentie', fontsize=12)
        ax1.set_title('Prijs Verdeling van Berekeningen', fontsize=14)
        ax1.grid(True, axis='y', alpha=0.3)
        ax1.legend()
        
        # Subplot 2: Prijs per gram analyse
        ax2 = fig.add_subplot(2, 1, 2)
        
        # Bereken prijs per gram
        df_filtered['price_per_gram'] = df_filtered['sell_price'] / df_filtered['weight_g']
        ppg_filtered = df_filtered[df_filtered['price_per_gram'] < 
                                   df_filtered['price_per_gram'].quantile(0.98)]
        
        # Histogram voor prijs per gram
        ax2.hist(ppg_filtered['price_per_gram'], bins=50,
                color=self.colors['secondary'], alpha=0.7,
                edgecolor='black', linewidth=0.5)
        
        # Gemiddelde lijn
        mean_ppg = ppg_filtered['price_per_gram'].mean()
        ax2.axvline(mean_ppg, color='red', linestyle='dashed', linewidth=2,
                   label=f'Gemiddelde: €{mean_ppg:.3f}/g')
        
        ax2.set_xlabel('Prijs per Gram (€/g)', fontsize=12)
        ax2.set_ylabel('Frequentie', fontsize=12)
        ax2.set_title('Prijs per Gram Verdeling', fontsize=14)
        ax2.grid(True, axis='y', alpha=0.3)
        ax2.legend()
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Prijs statistieken
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Bereken prijs ranges
        budget = df[df['sell_price'] < 20].shape[0]
        normal = df[(df['sell_price'] >= 20) & (df['sell_price'] < 50)].shape[0]
        premium = df[(df['sell_price'] >= 50) & (df['sell_price'] < 100)].shape[0]
        luxury = df[df['sell_price'] >= 100].shape[0]
        
        # Marge statistieken
        avg_margin = df['margin_pct'].mean()
        
        stats_text = f"💵 Budget (<€20): {budget} | " \
                    f"💰 Normaal (€20-50): {normal} | " \
                    f"💎 Premium (€50-100): {premium} | " \
                    f"👑 Luxe (>€100): {luxury} | " \
                    f"📈 Gem. Marge: {avg_margin:.1f}%"
        
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        self.figures['histogram'] = fig
        self.canvases['histogram'] = canvas
        
    def analyze(self):
        """Voer de analyse uit en return resultaten."""
        df = self.get_data()
        
        if df.empty:
            return {}
            
        # Basis statistieken
        results = {
            'gemiddeld_gewicht': df['weight_g'].mean(),
            'gemiddelde_prijs': df['sell_price'].mean(),
            'gemiddelde_marge': df['margin_pct'].mean(),
            'totale_omzet': df['sell_price'].sum(),
            'totale_winst': df['profit_amount'].sum()
        }
        
        # Voeg print tijd toe als het bestaat
        if 'print_hours' in df.columns:
            results['gemiddelde_tijd'] = df['print_hours'].mean()
        
        return results
        
    def update_analysis(self):
        """Update de analyse met nieuwe data."""
        # Clear oude widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Hermaak widgets
        self.create_title()
        self.create_analysis_widgets()
        self.create_refresh_button() 