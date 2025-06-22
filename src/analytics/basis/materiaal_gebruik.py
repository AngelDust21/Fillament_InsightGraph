"""
Materiaal Gebruik Analyse Module
=================================

Analyseert welke materialen het meest gebruikt worden.
Bevat 3 visualisaties:
1. Taart diagram - % verdeling materialen
2. Bar chart - aantal berekeningen per materiaal
3. Histogram - gewicht verdeling per materiaal type
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


class MateriaalGebruik(BaseAnalysis):
    """Analyse van materiaal gebruik in berekeningen."""
    
    def __init__(self, data_manager=None, parent_frame=None, colors=None):
        """Initialiseer Materiaal Gebruik analyse."""
        super().__init__(data_manager, parent_frame, colors)
        self.name = "Materiaal Gebruik Analyse"
        self.figures = {}
        self.canvases = {}
        
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "🎨 Materiaal Gebruik Analyse"
        
    def load_data(self):
        """Laad master_calculations.csv."""
        try:
            # Start vanaf de huidige file locatie
            current_file = os.path.abspath(__file__)
            
            # Ga naar de root van het project (waar exports folder is)
            # Van src/analytics/basis/materiaal_gebruik.py naar root is 3 niveau's omhoog
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
            
            # Pad naar master_calculations.csv
            master_path = os.path.join(project_root, 'exports', 'producten', 'master_calculations.csv')
            
            print(f"DEBUG: Project root: {project_root}")
            print(f"DEBUG: Looking for master_calculations.csv at: {master_path}")
            print(f"DEBUG: File exists: {os.path.exists(master_path)}")
            
            if os.path.exists(master_path):
                df = pd.read_csv(master_path)
                print(f"Loaded {len(df)} rows from master_calculations.csv")
                # Rename kolom voor compatibiliteit
                if 'weight' in df.columns:
                    df['weight_g'] = df['weight']
                return df
            else:
                print(f"master_calculations.csv not found at: {master_path}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
            
    def create_analysis_widgets(self):
        """Creëer de analyse widgets."""
        # Haal data op
        df = self.load_data()
        
        if df.empty:
            self.show_no_data_message()
            return
            
        # Maak notebook voor de 3 grafieken
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Taart diagram
        self.create_pie_chart_tab(df)
        
        # Tab 2: Bar chart per materiaal
        self.create_bar_chart_tab(df)
        
        # Tab 3: Gewicht histogram
        self.create_weight_histogram_tab(df)
        
        # Status label
        unique_materials = df['material'].nunique()
        self.status_label = tk.Label(
            self.main_frame,
            text=f"📊 {unique_materials} verschillende materialen geanalyseerd",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.status_label.pack(pady=5)
        
    def create_pie_chart_tab(self, df):
        """Tab 1: Taart diagram van materiaal verdeling."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="🥧 Materiaal Verdeling")
        
        # Professionele container met padding
        chart_container = tk.Frame(tab_frame, bg='white', relief=tk.FLAT, bd=1)
        chart_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header met titel en fullscreen knop
        header_frame = tk.Frame(chart_container, bg='white')
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        # Titel links
        tk.Label(
            header_frame,
            text="Materiaal Gebruik Verdeling",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#2C3E50'
        ).pack(side='left')
        
        # Fullscreen knop rechts
        fullscreen_btn = tk.Button(
            header_frame,
            text="⛶ Volledig Scherm",
            font=("Arial", 10),
            bg='#3498DB',
            fg='white',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=lambda: self.open_fullscreen('pie', 'Materiaal Gebruik Verdeling', df)
        )
        fullscreen_btn.pack(side='right')
        
        # Tel materialen
        material_counts = df['material'].value_counts()
        
        # Groepeer kleine materialen als "Overig"
        threshold = 0.02  # 2% threshold
        total = material_counts.sum()
        small_materials = material_counts[material_counts / total < threshold]
        
        if len(small_materials) > 0:
            # Voeg "Overig" toe
            material_counts = material_counts[material_counts / total >= threshold]
            material_counts['Overig'] = small_materials.sum()
        
        # Maak figuur met betere verhoudingen
        fig = Figure(figsize=(10, 8), facecolor='white', dpi=100)
        ax = fig.add_subplot(111)
        
        # Professioneel kleurenpalet
        colors = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6', 
                  '#1ABC9C', '#34495E', '#E67E22', '#16A085', '#27AE60']
        
        # Maak pie chart met betere styling
        wedges, texts, autotexts = ax.pie(
            material_counts.values,
            labels=material_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(material_counts)],
            pctdistance=0.85,
            shadow=False,
            explode=[0.05 if i == 0 else 0 for i in range(len(material_counts))]  # Highlight grootste
        )
        
        # Maak donut van pie chart
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        # Professionele titel
        ax.set_title('Materiaal Gebruik Verdeling', fontsize=18, pad=20, fontweight='bold')
        
        # Verbeter tekst leesbaarheid
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('medium')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        # Tight layout voor betere spacing
        fig.tight_layout(pad=2.0)
        
        # Embed in tkinter met padding
        canvas_frame = tk.Frame(chart_container, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Professionele info box onderaan
        info_frame = tk.Frame(tab_frame, bg='#F8F9FA', relief=tk.FLAT, bd=0)
        info_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Info content met betere layout
        info_content = tk.Frame(info_frame, bg='#F8F9FA')
        info_content.pack(expand=True, pady=15)
        
        # Top 5 in twee kolommen
        top_5 = material_counts.head(5)
        
        # Titel
        tk.Label(info_content, text="🏆 Top 5 Meest Gebruikte Materialen",
                font=("Arial", 12, "bold"), bg='#F8F9FA',
                fg='#2C3E50').pack(pady=(0, 10))
        
        # Grid voor materialen
        grid_frame = tk.Frame(info_content, bg='#F8F9FA')
        grid_frame.pack()
        
        for i, (mat, count) in enumerate(top_5.items()):
            row = i // 3
            col = i % 3
            
            mat_frame = tk.Frame(grid_frame, bg='white', relief=tk.RIDGE, bd=1)
            mat_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            tk.Label(mat_frame, text=mat, font=("Arial", 10, "bold"),
                    bg='white', fg='#2C3E50', pady=5).pack()
            tk.Label(mat_frame, text=f"{count} ({count/total*100:.1f}%)",
                    font=("Arial", 9), bg='white', fg='#7F8C8D').pack()
        
        self.figures['pie'] = fig
        self.canvases['pie'] = canvas
        
    def create_bar_chart_tab(self, df):
        """Tab 2: Bar chart van aantal berekeningen per materiaal."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="📊 Materiaal Frequentie")
        
        # Professionele container
        chart_container = tk.Frame(tab_frame, bg='white', relief=tk.FLAT, bd=1)
        chart_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header met titel en fullscreen knop
        header_frame = tk.Frame(chart_container, bg='white')
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        # Titel links
        tk.Label(
            header_frame,
            text="Top 10 Meest Gebruikte Materialen",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#2C3E50'
        ).pack(side='left')
        
        # Fullscreen knop rechts
        fullscreen_btn = tk.Button(
            header_frame,
            text="⛶ Volledig Scherm",
            font=("Arial", 10),
            bg='#3498DB',
            fg='white',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=lambda: self.open_fullscreen('bar', 'Materiaal Frequentie Analyse', df)
        )
        fullscreen_btn.pack(side='right')
        
        # Tel materialen - Top 10 voor betere leesbaarheid
        material_counts = df['material'].value_counts().head(10)
        
        # Categoriseer materialen
        basic_materials = ['PLA Basic', 'PETG Basic', 'ABS', 'ASA', 'TPU 95A']
        premium_materials = ['PLA Premium', 'PLA Silk', 'PLA Matte', 'PLA Wood']
        technical_materials = ['PC', 'PC Carbon', 'Nylon', 'PA12-CF', 'PA-CF']
        composite_materials = ['PETG-CF', 'Glass Fiber', 'Carbon Fiber']
        
        # Bepaal kleuren per categorie met moderne kleuren
        def get_color(material):
            if any(basic in material for basic in ['Basic', 'ABS', 'ASA', 'TPU']):
                return '#3498DB'  # Blauw voor basis
            elif any(premium in material for premium in ['Premium', 'Silk', 'Matte', 'Wood']):
                return '#2ECC71'  # Groen voor premium
            elif any(tech in material for tech in ['PC', 'Nylon', 'PA']):
                return '#E74C3C'  # Rood voor technisch
            else:
                return '#F39C12'  # Oranje voor composiet
        
        colors = [get_color(mat) for mat in material_counts.index]
        
        # Maak figuur met betere verhoudingen
        fig = Figure(figsize=(12, 7), facecolor='white', dpi=100)
        ax = fig.add_subplot(111)
        
        # Maak horizontale bar chart
        y_pos = np.arange(len(material_counts))
        bars = ax.barh(y_pos, material_counts.values, color=colors, height=0.7)
        
        # Styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(material_counts.index, fontsize=11)
        ax.set_xlabel('Aantal Berekeningen', fontsize=12, fontweight='medium')
        ax.set_title('Top 10 Meest Gebruikte Materialen', fontsize=16, pad=20, fontweight='bold')
        
        # Grid alleen op x-as
        ax.grid(True, axis='x', alpha=0.2, linestyle='--')
        ax.set_axisbelow(True)
        
        # Voeg waarde labels toe aan het einde van elke bar
        for i, (bar, value) in enumerate(zip(bars, material_counts.values)):
            ax.text(value + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{value}', ha='left', va='center', fontsize=10, fontweight='bold')
        
        # Adjust layout
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        
        # X-as limiet voor ruimte voor labels
        ax.set_xlim(0, max(material_counts.values) * 1.15)
        
        # Keer y-as om zodat hoogste bovenaan staat
        ax.invert_yaxis()
        
        fig.tight_layout(pad=2.0)
        
        # Embed in tkinter
        canvas_frame = tk.Frame(chart_container, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Professionele categorie statistieken
        stats_frame = tk.Frame(tab_frame, bg='#F8F9FA', relief=tk.FLAT, bd=0)
        stats_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Stats content
        stats_content = tk.Frame(stats_frame, bg='#F8F9FA')
        stats_content.pack(expand=True, pady=15)
        
        # Titel
        tk.Label(stats_content, text="📦 Materiaal Categorieën",
                font=("Arial", 12, "bold"), bg='#F8F9FA',
                fg='#2C3E50').pack(pady=(0, 10))
        
        # Grid voor categorieën
        cat_grid = tk.Frame(stats_content, bg='#F8F9FA')
        cat_grid.pack()
        
        # Tel per categorie
        basic_count = df[df['material'].str.contains('Basic|ABS|ASA|TPU', case=False, na=False)].shape[0]
        premium_count = df[df['material'].str.contains('Premium|Silk|Matte|Wood', case=False, na=False)].shape[0]
        technical_count = df[df['material'].str.contains('PC|Nylon|PA', case=False, na=False)].shape[0]
        composite_count = df[df['material'].str.contains('CF|Fiber|Carbon', case=False, na=False)].shape[0]
        
        categories = [
            ("Basis", basic_count, '#3498DB'),
            ("Premium", premium_count, '#2ECC71'),
            ("Technisch", technical_count, '#E74C3C'),
            ("Composiet", composite_count, '#F39C12')
        ]
        
        for i, (name, count, color) in enumerate(categories):
            cat_frame = tk.Frame(cat_grid, bg='white', relief=tk.RIDGE, bd=1)
            cat_frame.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            
            # Kleur indicator
            color_box = tk.Frame(cat_frame, bg=color, width=5)
            color_box.pack(side='left', fill='y')
            
            # Content
            content = tk.Frame(cat_frame, bg='white')
            content.pack(side='left', padx=15, pady=10)
            
            tk.Label(content, text=name, font=("Arial", 10, "bold"),
                    bg='white', fg='#2C3E50').pack(anchor='w')
            tk.Label(content, text=f"{count} items",
                    font=("Arial", 9), bg='white', fg='#7F8C8D').pack(anchor='w')
        
        self.figures['bar'] = fig
        self.canvases['bar'] = canvas
        
    def create_weight_histogram_tab(self, df):
        """Tab 3: Histogram van gewicht verdeling per materiaal type."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="⚖️ Gewicht Verdeling")
        
        # Professionele container
        chart_container = tk.Frame(tab_frame, bg='white', relief=tk.FLAT, bd=1)
        chart_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header met titel en fullscreen knop
        header_frame = tk.Frame(chart_container, bg='white')
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        # Titel links
        tk.Label(
            header_frame,
            text="Gewicht Verdeling per Top 6 Materialen",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#2C3E50'
        ).pack(side='left')
        
        # Fullscreen knop rechts
        fullscreen_btn = tk.Button(
            header_frame,
            text="⛶ Volledig Scherm",
            font=("Arial", 10),
            bg='#3498DB',
            fg='white',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=lambda: self.open_fullscreen('histogram', 'Gewicht Verdeling Analyse', df)
        )
        fullscreen_btn.pack(side='right')
        
        # Selecteer top 6 materialen
        top_materials = df['material'].value_counts().head(6).index
        
        # Filter data
        filtered_df = df[df['material'].isin(top_materials)]
        
        # Maak figuur met betere verhoudingen
        fig = Figure(figsize=(14, 8), facecolor='white', dpi=100)
        
        # Kleuren voor histogrammen
        hist_colors = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C']
        
        # 2x3 grid voor 6 materialen met betere spacing
        gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.25, 
                             left=0.08, right=0.96, top=0.92, bottom=0.08)
        
        for i, material in enumerate(top_materials):
            ax = fig.add_subplot(gs[i // 3, i % 3])
            
            # Filter data voor dit materiaal
            material_data = filtered_df[filtered_df['material'] == material]['weight_g']
            
            # Maak histogram met betere bins
            n, bins, patches = ax.hist(material_data, bins=15, 
                                      color=hist_colors[i], 
                                      alpha=0.8, 
                                      edgecolor='white',
                                      linewidth=1.2)
            
            # Voeg gemiddelde lijn toe
            mean_weight = material_data.mean()
            ax.axvline(mean_weight, color='#E74C3C', 
                      linestyle='--', linewidth=2.5,
                      label=f'Gem: {mean_weight:.0f}g')
            
            # Professionele styling
            ax.set_xlabel('Gewicht (gram)', fontsize=10, fontweight='medium')
            ax.set_ylabel('Frequentie', fontsize=10, fontweight='medium')
            ax.set_title(f'{material}', fontsize=12, fontweight='bold', pad=10)
            
            # Minimale grid
            ax.grid(True, alpha=0.15, linestyle='--')
            ax.set_axisbelow(True)
            
            # Verwijder top en right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(0.5)
            ax.spines['bottom'].set_linewidth(0.5)
            
            # Legend met betere positie
            ax.legend(fontsize=9, frameon=True, fancybox=True, 
                     shadow=False, loc='upper right')
            
            # Voeg statistieken box toe
            stats_text = f'n={len(material_data)}'
            ax.text(0.98, 0.90, stats_text,
                   transform=ax.transAxes, fontsize=9,
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            edgecolor=hist_colors[i], linewidth=1))
        
        # Overall titel
        fig.suptitle('Gewicht Verdeling per Top 6 Materialen', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        # Embed in tkinter
        canvas_frame = tk.Frame(chart_container, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Professionele gewicht statistieken
        stats_frame = tk.Frame(tab_frame, bg='#F8F9FA', relief=tk.FLAT, bd=0)
        stats_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Stats content
        stats_content = tk.Frame(stats_frame, bg='#F8F9FA')
        stats_content.pack(expand=True, pady=15)
        
        # Titel
        tk.Label(stats_content, text="📊 Gewicht Categorieën",
                font=("Arial", 12, "bold"), bg='#F8F9FA',
                fg='#2C3E50').pack(pady=(0, 10))
        
        # Grid voor gewicht ranges
        weight_grid = tk.Frame(stats_content, bg='#F8F9FA')
        weight_grid.pack()
        
        # Bereken gewicht ranges
        ranges = [
            ("🐁 Klein", "<50g", df[df['weight_g'] < 50].shape[0], '#3498DB'),
            ("🐕 Medium", "50-200g", df[(df['weight_g'] >= 50) & (df['weight_g'] < 200)].shape[0], '#2ECC71'),
            ("🐘 Groot", "200-500g", df[(df['weight_g'] >= 200) & (df['weight_g'] < 500)].shape[0], '#F39C12'),
            ("🦕 XL", ">500g", df[df['weight_g'] >= 500].shape[0], '#E74C3C')
        ]
        
        # Overall stats
        avg_weight = df['weight_g'].mean()
        max_weight = df['weight_g'].max()
        min_weight = df['weight_g'].min()
        
        for i, (icon_name, range_text, count, color) in enumerate(ranges):
            range_frame = tk.Frame(weight_grid, bg='white', relief=tk.RIDGE, bd=1)
            range_frame.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            
            # Content met padding
            content = tk.Frame(range_frame, bg='white')
            content.pack(padx=15, pady=10)
            
            # Icon en naam
            tk.Label(content, text=icon_name, font=("Arial", 11, "bold"),
                    bg='white', fg=color).pack()
            tk.Label(content, text=range_text, font=("Arial", 9),
                    bg='white', fg='#7F8C8D').pack()
            tk.Label(content, text=f"{count} items", font=("Arial", 10, "bold"),
                    bg='white', fg='#2C3E50').pack()
        
        # Overall stats onderaan
        overall_frame = tk.Frame(stats_content, bg='white', relief=tk.RIDGE, bd=1)
        overall_frame.pack(pady=(15, 0))
        
        overall_content = tk.Frame(overall_frame, bg='white')
        overall_content.pack(padx=20, pady=10)
        
        tk.Label(overall_content, 
                text=f"📏 Gemiddeld: {avg_weight:.0f}g  |  🏔️ Maximum: {max_weight:.0f}g  |  ⚖️ Minimum: {min_weight:.0f}g",
                font=("Arial", 10), bg='white', fg='#2C3E50').pack()
        
        self.figures['histogram'] = fig
        self.canvases['histogram'] = canvas
        
    def analyze(self):
        """Voer de analyse uit en return resultaten."""
        df = self.load_data()
        
        if df.empty:
            return {}
            
        # Basis statistieken
        results = {
            'totaal_materialen': df['material'].nunique(),
            'meest_gebruikt': df['material'].mode()[0] if not df['material'].mode().empty else 'N/A',
            'gemiddeld_gewicht': df['weight_g'].mean(),
            'totaal_gewicht': df['weight_g'].sum() / 1000,  # in kg
            'abrasive_percentage': (df['abrasive'].sum() / len(df) * 100) if 'abrasive' in df.columns else 0
        }
        
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

    def open_fullscreen(self, chart_type, title, df):
        """Open grafiek in volledig scherm venster."""
        # Maak nieuw toplevel venster
        fullscreen_window = tk.Toplevel(self.parent_frame)
        fullscreen_window.title(f"{title} - Volledig Scherm")
        fullscreen_window.geometry("1400x900")
        fullscreen_window.configure(bg='white')
        
        # Center het venster
        fullscreen_window.update_idletasks()
        x = (fullscreen_window.winfo_screenwidth() // 2) - (1400 // 2)
        y = (fullscreen_window.winfo_screenheight() // 2) - (900 // 2)
        fullscreen_window.geometry(f"+{x}+{y}")
        
        # Header frame
        header_frame = tk.Frame(fullscreen_window, bg='#2C3E50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#2C3E50')
        header_content.pack(expand=True, fill='both', padx=20)
        
        # Titel
        tk.Label(
            header_content,
            text=f"📊 {title}",
            font=("Arial", 20, "bold"),
            bg='#2C3E50',
            fg='white'
        ).pack(side='left', expand=True)
        
        # Sluiten knop
        close_btn = tk.Button(
            header_content,
            text="✕ Sluiten",
            font=("Arial", 12, "bold"),
            bg='#E74C3C',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=fullscreen_window.destroy
        )
        close_btn.pack(side='right')
        
        # Chart frame
        chart_frame = tk.Frame(fullscreen_window, bg='white')
        chart_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Hermaak de grafiek in groot formaat
        if chart_type == 'pie':
            self._create_fullscreen_pie(chart_frame, df)
        elif chart_type == 'bar':
            self._create_fullscreen_bar(chart_frame, df)
        elif chart_type == 'histogram':
            self._create_fullscreen_histogram(chart_frame, df)
            
    def _create_fullscreen_pie(self, parent, df):
        """Maak pie chart voor fullscreen weergave."""
        # Tel materialen
        material_counts = df['material'].value_counts()
        
        # Groepeer kleine materialen
        threshold = 0.02
        total = material_counts.sum()
        small_materials = material_counts[material_counts / total < threshold]
        
        if len(small_materials) > 0:
            material_counts = material_counts[material_counts / total >= threshold]
            material_counts['Overig'] = small_materials.sum()
        
        # Grote figuur voor fullscreen
        fig = Figure(figsize=(16, 10), facecolor='white', dpi=100)
        ax = fig.add_subplot(111)
        
        # Kleuren
        colors = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6', 
                  '#1ABC9C', '#34495E', '#E67E22', '#16A085', '#27AE60']
        
        # Maak pie chart
        wedges, texts, autotexts = ax.pie(
            material_counts.values,
            labels=material_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(material_counts)],
            pctdistance=0.85,
            shadow=False,
            explode=[0.05 if i == 0 else 0 for i in range(len(material_counts))]
        )
        
        # Donut
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        # Grote titel
        ax.set_title('Materiaal Gebruik Verdeling', fontsize=24, pad=30, fontweight='bold')
        
        # Grotere tekst
        for text in texts:
            text.set_fontsize(14)
            text.set_fontweight('medium')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_weight('bold')
        
        fig.tight_layout()
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_fullscreen_bar(self, parent, df):
        """Maak bar chart voor fullscreen weergave."""
        # Top 15 voor fullscreen
        material_counts = df['material'].value_counts().head(15)
        
        # Kleuren bepalen
        def get_color(material):
            if any(basic in material for basic in ['Basic', 'ABS', 'ASA', 'TPU']):
                return '#3498DB'
            elif any(premium in material for premium in ['Premium', 'Silk', 'Matte', 'Wood']):
                return '#2ECC71'
            elif any(tech in material for tech in ['PC', 'Nylon', 'PA']):
                return '#E74C3C'
            else:
                return '#F39C12'
        
        colors = [get_color(mat) for mat in material_counts.index]
        
        # Grote figuur
        fig = Figure(figsize=(16, 10), facecolor='white', dpi=100)
        ax = fig.add_subplot(111)
        
        # Bar chart
        y_pos = np.arange(len(material_counts))
        bars = ax.barh(y_pos, material_counts.values, color=colors, height=0.7)
        
        # Styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(material_counts.index, fontsize=14)
        ax.set_xlabel('Aantal Berekeningen', fontsize=16, fontweight='medium')
        ax.set_title('Top 15 Meest Gebruikte Materialen', fontsize=24, pad=30, fontweight='bold')
        
        ax.grid(True, axis='x', alpha=0.2, linestyle='--')
        ax.set_axisbelow(True)
        
        # Waarde labels
        for i, (bar, value) in enumerate(zip(bars, material_counts.values)):
            ax.text(value + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{value}', ha='left', va='center', fontsize=12, fontweight='bold')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlim(0, max(material_counts.values) * 1.15)
        ax.invert_yaxis()
        
        fig.tight_layout()
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _create_fullscreen_histogram(self, parent, df):
        """Maak histogram voor fullscreen weergave."""
        # Top 9 voor 3x3 grid
        top_materials = df['material'].value_counts().head(9).index
        filtered_df = df[df['material'].isin(top_materials)]
        
        # Grote figuur
        fig = Figure(figsize=(18, 11), facecolor='white', dpi=100)
        
        # Kleuren
        hist_colors = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6', 
                       '#1ABC9C', '#34495E', '#E67E22', '#16A085']
        
        # 3x3 grid
        gs = fig.add_gridspec(3, 3, hspace=0.30, wspace=0.25, 
                             left=0.06, right=0.96, top=0.92, bottom=0.06)
        
        for i, material in enumerate(top_materials):
            ax = fig.add_subplot(gs[i // 3, i % 3])
            
            material_data = filtered_df[filtered_df['material'] == material]['weight_g']
            
            n, bins, patches = ax.hist(material_data, bins=20, 
                                      color=hist_colors[i], 
                                      alpha=0.8, 
                                      edgecolor='white',
                                      linewidth=1.2)
            
            mean_weight = material_data.mean()
            ax.axvline(mean_weight, color='#E74C3C', 
                      linestyle='--', linewidth=3,
                      label=f'Gem: {mean_weight:.0f}g')
            
            ax.set_xlabel('Gewicht (gram)', fontsize=12, fontweight='medium')
            ax.set_ylabel('Frequentie', fontsize=12, fontweight='medium')
            ax.set_title(f'{material}', fontsize=14, fontweight='bold', pad=10)
            
            ax.grid(True, alpha=0.15, linestyle='--')
            ax.set_axisbelow(True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            ax.legend(fontsize=10, frameon=True, fancybox=True)
            
            stats_text = f'n={len(material_data)}'
            ax.text(0.98, 0.90, stats_text,
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                            edgecolor=hist_colors[i], linewidth=1))
        
        fig.suptitle('Gewicht Verdeling per Top 9 Materialen', 
                    fontsize=24, fontweight='bold', y=0.98)
        
        # Embed
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True) 