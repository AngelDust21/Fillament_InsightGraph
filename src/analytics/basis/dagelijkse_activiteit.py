"""
Wekelijkse Activiteit Analyse Module
=====================================

Analyseert wanneer de calculator het meest gebruikt wordt per week.
Gebruikt data uit calculation_log.csv voor gebruikersactiviteit tracking.

Bevat 3 visualisaties:
1. Lijn grafiek - berekeningen per week over de laatste 52 weken
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
        """Initialiseer Wekelijkse Activiteit analyse."""
        super().__init__(data_manager, parent_frame, colors)
        self.name = "Wekelijkse Activiteit Analyse"
        self.figures = {}
        self.canvases = {}
        
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "📅 Wekelijkse Activiteit Analyse"
        
    def load_data(self):
        """Laad calculation_log.csv voor analyses."""
        try:
            # Start vanaf de huidige file locatie
            current_file = os.path.abspath(__file__)
            
            # Ga naar de root van het project (waar exports folder is)
            # Van src/analytics/basis/dagelijkse_activiteit.py naar root is 3 niveau's omhoog
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
            
            # Pad naar calculation_log.csv (in berekeningen folder)
            calc_log_path = os.path.join(project_root, 'exports', 'berekeningen', 'calculation_log.csv')
            
            print(f"DEBUG: Project root: {project_root}")
            print(f"DEBUG: Looking for calculation_log.csv at: {calc_log_path}")
            print(f"DEBUG: File exists: {os.path.exists(calc_log_path)}")
            
            if os.path.exists(calc_log_path):
                df = pd.read_csv(calc_log_path)
                print(f"DEBUG: Loaded {len(df)} rows from calculation_log.csv")
                
                # Converteer timestamp naar datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
                
                # Voeg dag van de week toe (altijd nodig voor de visualisaties)
                df['day_of_week'] = df['timestamp'].dt.day_name()
                
                # Gebruik de bestaande hour_of_day uit het CSV als die bestaat
                # Anders bereken het uit de timestamp
                if 'hour_of_day' not in df.columns:
                    print("DEBUG: hour_of_day kolom niet gevonden, berekenen uit timestamp")
                    df['hour_of_day'] = df['timestamp'].dt.hour
                else:
                    print(f"DEBUG: Gebruik bestaande hour_of_day kolom uit CSV")
                    # Zorg ervoor dat het integers zijn
                    df['hour_of_day'] = df['hour_of_day'].astype(int)
                
                # Voeg date kolom toe als die niet bestaat
                if 'date' not in df.columns:
                    df['date'] = df['timestamp'].dt.date
                    print(f"DEBUG: Added date column from timestamp")
                
                # Voeg week informatie toe voor wekelijkse analyse
                df['year'] = df['timestamp'].dt.year
                df['week'] = df['timestamp'].dt.isocalendar().week
                df['year_week'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
                
                # Debug: print hour verdeling
                print(f"DEBUG: Hour distribution:")
                print(df['hour_of_day'].value_counts().sort_index().head(10))
                
                return df
            else:
                print("DEBUG: calculation_log.csv not found!")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"DEBUG: Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
            
    def create_analysis_widgets(self):
        """Creëer de analyse widgets."""
        # Haal data op
        df = self.load_data()
        
        print(f"DEBUG create_analysis_widgets: DataFrame has {len(df)} rows")
        print(f"DEBUG columns: {df.columns.tolist() if not df.empty else 'NO COLUMNS'}")
        
        # TIJDELIJK: Laad hardcoded data als df empty is
        if df.empty:
            print("WARNING: DataFrame is empty, loading sample data")
            # Laad calculation_log direct
            import os
            calc_log_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'exports', 'berekeningen', 'calculation_log.csv')
            if os.path.exists(calc_log_path):
                print(f"Loading from: {calc_log_path}")
                df = pd.read_csv(calc_log_path)
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
                    df['date'] = df['timestamp'].dt.date
                    df['day_of_week'] = df['timestamp'].dt.day_name()
                    # Alleen hour_of_day toevoegen als die niet bestaat
                    if 'hour_of_day' not in df.columns:
                        df['hour_of_day'] = df['timestamp'].dt.hour
                    # Voeg week informatie toe
                    df['year'] = df['timestamp'].dt.year
                    df['week'] = df['timestamp'].dt.isocalendar().week
                    df['year_week'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
                print(f"Loaded {len(df)} rows")
            else:
                print(f"File not found: {calc_log_path}")
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
        """Tab 1: Lijn grafiek van wekelijkse activiteit."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="📈 Wekelijkse Trend")
        
        # Groepeer per week
        weekly_counts = df.groupby('year_week').size()
        
        # Sorteer op jaar-week
        weekly_counts = weekly_counts.sort_index()
        
        # Bepaal huidige week
        current_date = datetime.now()
        current_year_week = f"{current_date.year}-W{current_date.isocalendar().week:02d}"
        
        # Neem laatste 52 weken (1 jaar)
        if len(weekly_counts) > 52:
            weekly_counts = weekly_counts.iloc[-52:]
        
        # Maak figuur
        fig = Figure(figsize=(12, 6), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Plot lijn grafiek
        x_values = range(len(weekly_counts))
        y_values = weekly_counts.values
        week_labels = weekly_counts.index
        
        # Basis lijn
        ax.plot(x_values, y_values, 
                marker='o', linewidth=2, markersize=6,
                color=self.colors['primary'], label='Berekeningen per week')
        
        # Highlight huidige week als die in de data zit
        if current_year_week in week_labels:
            current_idx = list(week_labels).index(current_year_week)
            ax.scatter(current_idx, y_values[current_idx], 
                      color=self.colors['accent'], s=150, zorder=5,
                      label='Huidige week')
            # Voeg annotatie toe
            ax.annotate('Deze week', 
                       xy=(current_idx, y_values[current_idx]),
                       xytext=(current_idx, y_values[current_idx] + max(y_values) * 0.1),
                       ha='center', fontsize=10,
                       arrowprops=dict(arrowstyle='->', color=self.colors['accent']))
        
        # Voeg gemiddelde lijn toe
        avg = weekly_counts.mean()
        ax.axhline(y=avg, color=self.colors['secondary'], 
                   linestyle='--', alpha=0.7, 
                   label=f'Gemiddelde: {avg:.1f} per week')
        
        # Voeg trend lijn toe (optioneel)
        if len(weekly_counts) > 4:
            z = np.polyfit(x_values, y_values, 1)
            p = np.poly1d(z)
            ax.plot(x_values, p(x_values), color='red', 
                   linestyle=':', alpha=0.7, label='Trend')
        
        # Styling
        ax.set_xlabel('Week', fontsize=12)
        ax.set_ylabel('Aantal Berekeningen', fontsize=12)
        ax.set_title('Wekelijkse Calculator Activiteit (laatste 52 weken)', fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # X-as labels: toon alleen elke 4e week voor leesbaarheid
        tick_positions = list(range(0, len(week_labels), 4))
        tick_labels = [week_labels[i] for i in tick_positions]
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=45, ha='right')
        
        # Y-as altijd vanaf 0
        ax.set_ylim(bottom=0)
        
        # Tight layout
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, tab_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Statistieken frame
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Bereken extra statistieken
        laatste_4_weken = weekly_counts.iloc[-4:].mean() if len(weekly_counts) >= 4 else 0
        groei = ((y_values[-1] - y_values[0]) / y_values[0] * 100) if len(y_values) > 1 and y_values[0] > 0 else 0
        
        stats_text = f"📊 Totaal: {weekly_counts.sum()} | " \
                    f"📅 Weken: {len(weekly_counts)} | " \
                    f"📈 Beste week: {weekly_counts.max()} | " \
                    f"➗ Gem/week: {avg:.1f} | " \
                    f"🔥 Laatste 4 weken gem: {laatste_4_weken:.1f} | " \
                    f"📊 Groei: {groei:+.0f}%"
        
        tk.Label(stats_frame, text=stats_text, 
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        # Voeg week details toe
        if current_year_week in weekly_counts:
            current_week_count = weekly_counts[current_year_week]
            week_text = f"🎯 Deze week ({current_year_week}): {current_week_count} berekeningen"
            
            tk.Label(stats_frame, text=week_text,
                    font=("Arial", 10, "bold"), bg=self.colors['white'],
                    fg=self.colors['accent'], pady=5).pack()
        
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
        """Tab 3: Heatmap van activiteit per uur/dag over ALLE data uit master_calculations."""
        tab_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab_frame, text="🔥 Uur/Dag Heatmap")
        
        # Laad master_calculations.csv voor de heatmap
        # Dit geeft een completer beeld van alle berekeningen
        try:
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
            master_path = os.path.join(project_root, 'exports', 'producten', 'master_calculations.csv')
            
            if os.path.exists(master_path):
                # Laad master data voor heatmap
                master_df = pd.read_csv(master_path)
                master_df['timestamp'] = pd.to_datetime(master_df['timestamp'], format='mixed')
                master_df['day_of_week'] = master_df['timestamp'].dt.day_name()
                
                # Gebruik bestaande hour_of_day of bereken het
                if 'hour_of_day' not in master_df.columns:
                    master_df['hour_of_day'] = master_df['timestamp'].dt.hour
                else:
                    master_df['hour_of_day'] = master_df['hour_of_day'].astype(int)
                    
                print(f"DEBUG Heatmap: Loaded {len(master_df)} rows from master_calculations.csv")
                df_for_heatmap = master_df
            else:
                print("DEBUG Heatmap: master_calculations.csv not found, using calculation_log data")
                df_for_heatmap = df
        except Exception as e:
            print(f"DEBUG Heatmap: Error loading master data: {e}")
            df_for_heatmap = df
        
        # Nederlandse dag namen voor weergave
        dag_namen = {
            'Monday': 'Maandag',
            'Tuesday': 'Dinsdag', 
            'Wednesday': 'Woensdag',
            'Thursday': 'Donderdag',
            'Friday': 'Vrijdag',
            'Saturday': 'Zaterdag',
            'Sunday': 'Zondag'
        }
        
        # Maak pivot table voor heatmap - gebruik ALLE data uit master_calculations
        heatmap_data = df_for_heatmap.pivot_table(
            values='timestamp',
            index='hour_of_day',
            columns='day_of_week',
            aggfunc='count',
            fill_value=0
        )
        
        # Herorden kolommen naar Nederlandse weekdagen
        dag_volgorde_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                          'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(columns=dag_volgorde_en, fill_value=0)
        
        # BELANGRIJK: Zorg ervoor dat ALLE 24 uren aanwezig zijn in de index
        # Anders worden de uren verkeerd uitgelijnd in de heatmap
        all_hours = list(range(24))
        heatmap_data = heatmap_data.reindex(index=all_hours, fill_value=0)
        
        # Nederlandse labels
        dag_labels = ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo']
        
        # Maak figuur
        fig = Figure(figsize=(10, 8), facecolor=self.colors['bg'])
        ax = fig.add_subplot(111)
        
        # Maak heatmap
        sns.heatmap(heatmap_data, ax=ax, cmap='YlOrRd', 
                   annot=True, fmt='d', cbar_kws={'label': 'Totaal Aantal Berekeningen'},
                   xticklabels=dag_labels, yticklabels=range(24))
        
        # Styling
        ax.set_xlabel('Dag van de Week', fontsize=12)
        ax.set_ylabel('Uur van de Dag', fontsize=12)
        ax.set_title('Activiteit Heatmap - Alle Berekeningen (Master Data)', fontsize=14, pad=20)
        
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
        
        # Piek tijden analyse over ALLE master data
        stats_frame = tk.Frame(tab_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Vind piek uren over alle data
        hour_totals = df_for_heatmap['hour_of_day'].value_counts().sort_index()
        piek_uur = hour_totals.idxmax()
        
        # Bereken totaal aantal berekeningen per tijdzone
        ochtend = sum(hour_totals.get(h, 0) for h in range(6, 12))
        middag = sum(hour_totals.get(h, 0) for h in range(12, 18))
        avond = sum(hour_totals.get(h, 0) for h in range(18, 24))
        nacht = sum(hour_totals.get(h, 0) for h in range(0, 6))
        
        # Bereken percentages
        totaal = ochtend + middag + avond + nacht
        ochtend_pct = (ochtend / totaal * 100) if totaal > 0 else 0
        middag_pct = (middag / totaal * 100) if totaal > 0 else 0
        avond_pct = (avond / totaal * 100) if totaal > 0 else 0
        nacht_pct = (nacht / totaal * 100) if totaal > 0 else 0
        
        # Vind drukste dag/uur combinatie
        max_val = heatmap_data.max().max()
        max_location = heatmap_data.stack().idxmax() if max_val > 0 else (0, 'Monday')
        drukste_uur = max_location[0]
        drukste_dag = dag_namen.get(max_location[1], max_location[1])
        
        stats_text = f"⏰ Piek uur: {piek_uur}:00 ({hour_totals.get(piek_uur, 0)} totaal) | " \
                    f"🌅 Ochtend: {ochtend} ({ochtend_pct:.0f}%) | " \
                    f"☀️ Middag: {middag} ({middag_pct:.0f}%) | " \
                    f"🌙 Avond: {avond} ({avond_pct:.0f}%) | " \
                    f"🌃 Nacht: {nacht} ({nacht_pct:.0f}%)"
        
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 10), bg=self.colors['white'],
                fg=self.colors['text'], pady=5).pack()
        
        # Extra info over drukste moment en data bron
        extra_text = f"🔥 Drukste moment: {drukste_dag} om {drukste_uur}:00 uur ({max_val} berekeningen)"
        tk.Label(stats_frame, text=extra_text,
                font=("Arial", 10, "bold"), bg=self.colors['white'],
                fg=self.colors['accent'], pady=5).pack()
        
        # Toon welke data bron gebruikt is
        bron_text = f"📊 Data bron: {'master_calculations.csv' if df_for_heatmap is not df else 'calculation_log.csv'} ({len(df_for_heatmap)} berekeningen)"
        tk.Label(stats_frame, text=bron_text,
                font=("Arial", 9), bg=self.colors['white'],
                fg=self.colors['text'], pady=3).pack()
        
        self.figures['heatmap'] = fig
        self.canvases['heatmap'] = canvas
        
    def analyze(self):
        """Voer de analyse uit en return resultaten."""
        df = self.load_data()
        
        if df.empty:
            return {}
            
        # Wekelijkse statistieken
        weekly_counts = df.groupby('year_week').size()
        
        results = {
            'totaal_berekeningen': len(df),
            'unieke_weken': df['year_week'].nunique(),
            'eerste_berekening': df['timestamp'].min(),
            'laatste_berekening': df['timestamp'].max(),
            'gem_per_week': len(df) / df['year_week'].nunique() if df['year_week'].nunique() > 0 else 0,
            'beste_week': weekly_counts.idxmax() if not weekly_counts.empty else 'N/A',
            'beste_week_aantal': weekly_counts.max() if not weekly_counts.empty else 0
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