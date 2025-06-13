"""
Dagelijkse Activiteit Analyse Module
=====================================

Analyseert wanneer de calculator het meest gebruikt wordt.
Bevat 3 visualisaties:
1. Lijn grafiek - berekeningen per dag over tijd
2. Bar chart - berekeningen per dag van de week  
3. Heatmap - activiteit per uur/dag matrix
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import os

from ..base_analysis import BaseAnalysis


class DagelijkseActiviteit(BaseAnalysis):
    """Analyse van dagelijkse calculator activiteit."""
    
    def __init__(self, data_manager=None, parent_frame=None, colors=None):
        """Initialiseer Dagelijkse Activiteit analyse."""
        super().__init__(data_manager, parent_frame, colors)
        self.name = "Dagelijkse Activiteit Analyse"
        self.figures = {}
        self.canvases = {}
        
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "📅 Dagelijkse Activiteit Analyse"
        
    def get_data(self):
        """Laad master_calculations.csv voor analyses."""
        try:
            # Direct pad naar master_calculations.csv
            # base_dir is gewoon "exports", niet "exports/exports"
            if hasattr(self.data_manager, 'base_dir'):
                if isinstance(self.data_manager.base_dir, str):
                    base_dir = self.data_manager.base_dir
                else:
                    base_dir = str(self.data_manager.base_dir)
                
                # Als base_dir al "exports" is, voeg het niet dubbel toe
                if base_dir.endswith('exports'):
                    master_path = os.path.join(base_dir, 'master_calculations.csv')
                else:
                    master_path = os.path.join(base_dir, 'exports', 'master_calculations.csv')
            else:
                # Fallback: gebruik relatief pad
                master_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'exports', 'master_calculations.csv')
            
            print(f"DEBUG: Looking for data at: {master_path}")
            print(f"DEBUG: File exists: {os.path.exists(master_path)}")
            
            if os.path.exists(master_path):
                df = pd.read_csv(master_path)
                print(f"DEBUG: Loaded {len(df)} rows from master_calculations.csv")
                
                # Parse timestamps - master_calculations heeft deze kolommen al
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
                    # Voeg date kolom toe als die niet bestaat
                    if 'date' not in df.columns:
                        df['date'] = df['timestamp'].dt.date
                return df
            else:
                print("DEBUG: master_calculations.csv not found!")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"DEBUG: Exception loading data: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
            
    def create_analysis_widgets(self):
        """Creëer de analyse widgets."""
        # Haal data op
        df = self.get_data()
        
        print(f"DEBUG create_analysis_widgets: DataFrame has {len(df)} rows")
        print(f"DEBUG columns: {df.columns.tolist() if not df.empty else 'NO COLUMNS'}")
        
        # TIJDELIJK: Laad hardcoded data als df empty is
        if df.empty:
            print("WARNING: DataFrame is empty, loading sample data")
            # Laad master_calculations direct
            import os
            master_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'exports', 'master_calculations.csv')
            if os.path.exists(master_path):
                print(f"Loading from: {master_path}")
                df = pd.read_csv(master_path)
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df['date'] = df['timestamp'].dt.date
                print(f"Loaded {len(df)} rows")
            else:
                print(f"File not found: {master_path}")
                self.show_no_data_message()
                return
            
        # Maak notebook voor de 3 grafieken
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Dagelijkse trend
        self.create_daily_trend_tab(df)
        
        # Tab 2: Weekdag analyse
        self.create_weekday_tab(df)
        
        # Tab 3: Uur/Dag heatmap
        self.create_heatmap_tab(df)
        
        # Status label
        self.status_label = tk.Label(
            self.main_frame,
            text=f"📊 {len(df)} berekeningen geanalyseerd",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.status_label.pack(pady=5)
        
    def create_daily_trend_tab(self, df):
        """Tab 1: Lijn grafiek van dagelijkse activiteit."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="📈 Dagelijkse Trend")
        
        # Bereken berekeningen per dag
        if 'date' not in df.columns:
            # Als date kolom niet bestaat, maak hem van timestamp
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_counts = df.groupby(df['date']).size()
        
        # Maak figuur
        fig = Figure(figsize=(10, 6), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Plot lijn grafiek
        ax.plot(daily_counts.index, daily_counts.values, 
                marker='o', linewidth=2, markersize=6,
                color=self.colors['primary'], label='Berekeningen')
        
        # Voeg gemiddelde lijn toe
        avg = daily_counts.mean()
        ax.axhline(y=avg, color=self.colors['secondary'], 
                   linestyle='--', alpha=0.7, 
                   label=f'Gemiddelde: {avg:.1f}')
        
        # Styling
        ax.set_xlabel('Datum', fontsize=12)
        ax.set_ylabel('Aantal Berekeningen', fontsize=12)
        ax.set_title('Dagelijkse Calculator Activiteit', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Roteer x-labels
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Tight layout
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Statistieken
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        stats_text = f"📊 Totaal: {daily_counts.sum()} | " \
                    f"📅 Dagen: {len(daily_counts)} | " \
                    f"📈 Max: {daily_counts.max()} | " \
                    f"📉 Min: {daily_counts.min()} | " \
                    f"➗ Gem: {avg:.1f}"
        
        tk.Label(stats_frame, text=stats_text, 
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        self.figures['daily'] = fig
        self.canvases['daily'] = canvas
        
    def create_weekday_tab(self, df):
        """Tab 2: Bar chart per dag van de week."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="📊 Weekdag Analyse")
        
        # Nederlandse dag namen
        dag_namen = {
            'Monday': 'Maandag',
            'Tuesday': 'Dinsdag', 
            'Wednesday': 'Woensdag',
            'Thursday': 'Donderdag',
            'Friday': 'Vrijdag',
            'Saturday': 'Zaterdag',
            'Sunday': 'Zondag'
        }
        
        # Bereken per weekdag
        df['weekday'] = df['day_of_week'].map(dag_namen)
        weekday_counts = df['weekday'].value_counts()
        
        # Sorteer op juiste volgorde
        dag_volgorde = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 
                       'Vrijdag', 'Zaterdag', 'Zondag']
        weekday_counts = weekday_counts.reindex(dag_volgorde, fill_value=0)
        
        # Maak figuur
        fig = Figure(figsize=(10, 6), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Maak bar chart met verschillende kleuren voor weekend
        colors = [self.colors['primary'] if d not in ['Zaterdag', 'Zondag'] 
                 else self.colors['accent'] for d in dag_volgorde]
        
        bars = ax.bar(weekday_counts.index, weekday_counts.values, color=colors)
        
        # Voeg waarde labels toe
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10)
        
        # Styling
        ax.set_xlabel('Dag van de Week', fontsize=12)
        ax.set_ylabel('Aantal Berekeningen', fontsize=12)
        ax.set_title('Calculator Gebruik per Weekdag', fontsize=14, pad=20)
        ax.grid(True, axis='y', alpha=0.3)
        
        # Voeg legenda toe
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(color=self.colors['primary'], label='Weekdag'),
            Patch(color=self.colors['accent'], label='Weekend')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Weekend vs weekdag statistieken
        weekdagen = weekday_counts[['Maandag', 'Dinsdag', 'Woensdag', 
                                   'Donderdag', 'Vrijdag']].sum()
        weekend = weekday_counts[['Zaterdag', 'Zondag']].sum()
        
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        stats_text = f"📅 Weekdagen: {weekdagen} ({weekdagen/(weekdagen+weekend)*100:.0f}%) | " \
                    f"🏖️ Weekend: {weekend} ({weekend/(weekdagen+weekend)*100:.0f}%) | " \
                    f"🏆 Drukste dag: {weekday_counts.idxmax()}"
        
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        self.figures['weekday'] = fig
        self.canvases['weekday'] = canvas
        
    def create_heatmap_tab(self, df):
        """Tab 3: Heatmap van activiteit per uur/dag."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="🔥 Uur/Dag Heatmap")
        
        # Maak pivot table voor heatmap
        heatmap_data = df.pivot_table(
            values='timestamp',
            index='hour_of_day',
            columns='day_of_week',
            aggfunc='count',
            fill_value=0
        )
        
        # Herorden kolommen
        dag_volgorde_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                          'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(columns=dag_volgorde_en, fill_value=0)
        
        # Nederlandse labels
        dag_labels = ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo']
        
        # Maak figuur
        fig = Figure(figsize=(10, 8), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Maak heatmap
        sns.heatmap(heatmap_data, ax=ax, cmap='YlOrRd', 
                   annot=True, fmt='d', cbar_kws={'label': 'Aantal Berekeningen'},
                   xticklabels=dag_labels, yticklabels=range(24))
        
        # Styling
        ax.set_xlabel('Dag van de Week', fontsize=12)
        ax.set_ylabel('Uur van de Dag', fontsize=12)
        ax.set_title('Activiteit Heatmap - Wanneer werk je?', fontsize=14, pad=20)
        
        # Voeg werkuren indicatie toe
        ax.axhline(y=9, color='blue', linewidth=1, alpha=0.3, linestyle='--')
        ax.axhline(y=17, color='blue', linewidth=1, alpha=0.3, linestyle='--')
        ax.text(6.5, 9, 'Werkuren', ha='right', va='bottom', 
               fontsize=8, color='blue', alpha=0.7)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Piek tijden analyse
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Vind piek uren
        hour_totals = df['hour_of_day'].value_counts().sort_index()
        piek_uur = hour_totals.idxmax()
        
        # Ochtend/middag/avond verdeling
        ochtend = hour_totals[6:12].sum()
        middag = hour_totals[12:18].sum()
        avond = hour_totals[18:24].sum()
        nacht = hour_totals[0:6].sum()
        
        stats_text = f"⏰ Piek uur: {piek_uur}:00 | " \
                    f"🌅 Ochtend: {ochtend} | " \
                    f"☀️ Middag: {middag} | " \
                    f"🌙 Avond: {avond} | " \
                    f"🌃 Nacht: {nacht}"
        
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        self.figures['heatmap'] = fig
        self.canvases['heatmap'] = canvas
        
    def analyze(self):
        """Voer de analyse uit en return resultaten."""
        df = self.get_data()
        
        if df.empty:
            return {}
            
        # Basis statistieken
        results = {
            'totaal_berekeningen': len(df),
            'unieke_dagen': df['date'].dt.date.nunique(),
            'eerste_berekening': df['timestamp'].min(),
            'laatste_berekening': df['timestamp'].max(),
            'gem_per_dag': len(df) / df['date'].dt.date.nunique() if df['date'].dt.date.nunique() > 0 else 0
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