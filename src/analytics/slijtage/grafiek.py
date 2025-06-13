"""
Slijtage Grafiek Visualisaties - H2D Price Calculator
==================================================

Deze module visualiseert slijtage data in verschillende grafieken:
- Pie chart: Verdeling abrasieve vs normale materialen
- Line graph: Slijtage trend over tijd
- Bar chart: Kosten per materiaal type
- Heatmap: Gebruik per dag/uur

Educatieve waarde:
- Data visualisatie technieken
- Trend analyse voor maintenance planning
- Cost-benefit inzichten
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import seaborn as sns

from ..base_analysis import BaseAnalysis
from ...materials.material_properties import (
    get_material_properties,
    calculate_wear_cost,
    is_abrasive_material
)


class SlijtageGrafiek(BaseAnalysis):
    """Visualiseert slijtage data in verschillende grafiek types.
    
    Features:
    - Material usage distribution
    - Wear cost trends
    - Maintenance predictions
    - Usage heatmaps
    """
    
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "📊 Slijtage Visualisaties"
        
    def create_analysis_widgets(self) -> None:
        """Creëer de grafiek interface."""
        # Check data beschikbaarheid
        df = self.load_data()
        if df.empty:
            self.show_no_data_message()
            return
            
        # Notebook voor verschillende grafieken
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Material Distribution
        self.dist_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.dist_frame, text="📊 Materiaal Verdeling")
        self._create_distribution_chart()
        
        # Tab 2: Wear Cost Trends
        self.trend_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.trend_frame, text="📈 Slijtage Trend")
        self._create_trend_chart()
        
        # Tab 3: Cost Analysis
        self.cost_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.cost_frame, text="💰 Kosten Analyse")
        self._create_cost_chart()
        
        # Tab 4: Usage Heatmap
        self.heat_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.heat_frame, text="🔥 Gebruik Heatmap")
        self._create_heatmap()
        
        # Control panel onderaan
        self._create_control_panel()
        
    def _create_distribution_chart(self):
        """Maak pie/donut chart voor materiaal verdeling."""
        # Analyse frame
        analysis_frame = tk.Frame(self.dist_frame, bg=self.colors['white'])
        analysis_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Matplotlib figure
        self.dist_fig = Figure(figsize=(10, 6), facecolor='white')
        
        # Canvas
        self.dist_canvas = FigureCanvasTkAgg(self.dist_fig, master=analysis_frame)
        self.dist_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initial plot
        self._update_distribution_chart()
        
    def _update_distribution_chart(self):
        """Update materiaal verdeling charts."""
        df = self.load_data()
        
        # Clear figure
        self.dist_fig.clear()
        
        # Maak 2x2 subplot grid
        gs = self.dist_fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Abrasive vs Non-abrasive (uren)
        ax1 = self.dist_fig.add_subplot(gs[0, 0])
        if 'print_hours' not in df.columns:
            df['print_hours'] = df['weight'] / 20.0
            
        abrasive_hours = df[df['abrasive'] == True]['print_hours'].sum()
        normal_hours = df[df['abrasive'] == False]['print_hours'].sum()
        
        # Donut chart
        sizes = [abrasive_hours, normal_hours]
        labels = ['Abrasief', 'Normaal']
        colors = ['#FF6B6B', '#4ECDC4']
        explode = (0.05, 0)
        
        wedges, texts, autotexts = ax1.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            wedgeprops=dict(width=0.5)  # Donut effect
        )
        
        ax1.set_title('Print Uren Verdeling', fontsize=12, fontweight='bold')
        
        # 2. Top 5 Abrasieve Materialen
        ax2 = self.dist_fig.add_subplot(gs[0, 1])
        abrasive_df = df[df['abrasive'] == True]
        if not abrasive_df.empty:
            material_hours = abrasive_df.groupby('material')['print_hours'].sum()
            top_materials = material_hours.nlargest(5)
            
            bars = ax2.barh(top_materials.index, top_materials.values)
            ax2.set_xlabel('Uren')
            ax2.set_title('Top 5 Abrasieve Materialen', fontsize=12, fontweight='bold')
            
            # Kleur bars op basis van wear factor
            for i, (material, bar) in enumerate(zip(top_materials.index, bars)):
                props = get_material_properties(material)
                if props:
                    # Kleur op basis van wear factor
                    if props.nozzle_wear_factor >= 12:
                        bar.set_color('#FF4444')  # Extreme wear
                    elif props.nozzle_wear_factor >= 8:
                        bar.set_color('#FF8844')  # High wear
                    else:
                        bar.set_color('#FFBB44')  # Medium wear
        else:
            ax2.text(0.5, 0.5, 'Geen abrasieve prints', 
                    ha='center', va='center', transform=ax2.transAxes)
            
        # 3. Material Type Distribution
        ax3 = self.dist_fig.add_subplot(gs[1, :])
        
        # Groepeer materialen op type
        material_groups = {
            'PLA': ['PLA Basic', 'PLA Silk', 'PLA Matte', 'PLA Wood', 'PLA-CF'],
            'PETG': ['PETG Basic', 'PETG-CF', 'PETG-GF'],
            'ABS/ASA': ['ABS', 'ASA'],
            'PA (Nylon)': ['PA-CF', 'PA12-CF'],
            'Others': ['PC', 'TPU 95A']
        }
        
        group_hours = {}
        for group, materials in material_groups.items():
            group_hours[group] = df[df['material'].isin(materials)]['print_hours'].sum()
            
        # Stacked bar chart
        groups = list(group_hours.keys())
        normal_hours = []
        abrasive_hours = []
        
        for group, materials in material_groups.items():
            group_df = df[df['material'].isin(materials)]
            normal = group_df[group_df['abrasive'] == False]['print_hours'].sum()
            abrasive = group_df[group_df['abrasive'] == True]['print_hours'].sum()
            normal_hours.append(normal)
            abrasive_hours.append(abrasive)
            
        x = np.arange(len(groups))
        width = 0.6
        
        p1 = ax3.bar(x, normal_hours, width, label='Normaal', color='#4ECDC4')
        p2 = ax3.bar(x, abrasive_hours, width, bottom=normal_hours, 
                     label='Abrasief', color='#FF6B6B')
        
        ax3.set_ylabel('Print Uren')
        ax3.set_title('Gebruik per Materiaal Familie', fontsize=12, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(groups)
        ax3.legend()
        
        # Voeg waarde labels toe
        for i, (n, a) in enumerate(zip(normal_hours, abrasive_hours)):
            if n + a > 0:
                ax3.text(i, n + a + 1, f'{n+a:.0f}', ha='center', va='bottom')
        
        self.dist_canvas.draw()
        
    def _create_trend_chart(self):
        """Maak trend analyse charts."""
        analysis_frame = tk.Frame(self.trend_frame, bg=self.colors['white'])
        analysis_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Matplotlib figure
        self.trend_fig = Figure(figsize=(10, 6), facecolor='white')
        
        # Canvas
        self.trend_canvas = FigureCanvasTkAgg(self.trend_fig, master=analysis_frame)
        self.trend_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initial plot
        self._update_trend_chart()
        
    def _update_trend_chart(self):
        """Update trend charts."""
        df = self.load_data()
        
        # Clear figure
        self.trend_fig.clear()
        
        # Voeg print_hours toe als nodig
        if 'print_hours' not in df.columns:
            df['print_hours'] = df['weight'] / 20.0
            
        # Groepeer per dag
        df['date'] = df['timestamp'].dt.date
        daily_data = df.groupby(['date', 'abrasive'])['print_hours'].sum().unstack(fill_value=0)
        
        # Als er data is
        if not daily_data.empty:
            # 2 subplots
            ax1 = self.trend_fig.add_subplot(2, 1, 1)
            ax2 = self.trend_fig.add_subplot(2, 1, 2)
            
            # Plot 1: Cumulatieve slijtage
            cumulative_abrasive = daily_data.get(True, pd.Series(0, index=daily_data.index)).cumsum()
            cumulative_normal = daily_data.get(False, pd.Series(0, index=daily_data.index)).cumsum()
            
            ax1.plot(cumulative_abrasive.index, cumulative_abrasive.values, 
                    'r-', linewidth=2, label='Abrasief (Cumulatief)')
            ax1.plot(cumulative_normal.index, cumulative_normal.values, 
                    'b-', linewidth=2, label='Normaal (Cumulatief)')
            
            ax1.set_xlabel('Datum')
            ax1.set_ylabel('Cumulatieve Uren')
            ax1.set_title('Cumulatieve Print Uren Over Tijd', fontsize=12, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Roteer x-labels
            for label in ax1.get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')
            
            # Plot 2: Dagelijkse ratio
            daily_total = daily_data.sum(axis=1)
            daily_abrasive_pct = (daily_data.get(True, 0) / daily_total * 100).fillna(0)
            
            # Moving average
            if len(daily_abrasive_pct) > 7:
                ma7 = daily_abrasive_pct.rolling(window=7, center=True).mean()
                ax2.plot(ma7.index, ma7.values, 'g-', linewidth=2, 
                        label='7-dagen gemiddelde')
                
            ax2.bar(daily_abrasive_pct.index, daily_abrasive_pct.values, 
                   color='orange', alpha=0.6, label='Dagelijks %')
            
            ax2.axhline(y=30, color='r', linestyle='--', alpha=0.5, 
                       label='30% waarschuwing')
            
            ax2.set_xlabel('Datum')
            ax2.set_ylabel('Abrasief Percentage (%)')
            ax2.set_title('Dagelijks Abrasief Materiaal Percentage', 
                         fontsize=12, fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, 100)
            
            # Roteer x-labels
            for label in ax2.get_xticklabels():
                label.set_rotation(45)
                label.set_ha('right')
                
        else:
            ax = self.trend_fig.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, 'Onvoldoende data voor trend analyse', 
                   ha='center', va='center', transform=ax.transAxes)
            
        self.trend_fig.tight_layout()
        self.trend_canvas.draw()
        
    def _create_cost_chart(self):
        """Maak kosten analyse charts."""
        analysis_frame = tk.Frame(self.cost_frame, bg=self.colors['white'])
        analysis_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Matplotlib figure
        self.cost_fig = Figure(figsize=(10, 6), facecolor='white')
        
        # Canvas
        self.cost_canvas = FigureCanvasTkAgg(self.cost_fig, master=analysis_frame)
        self.cost_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initial plot
        self._update_cost_chart()
        
    def _update_cost_chart(self):
        """Update kosten charts."""
        df = self.load_data()
        
        # Clear figure
        self.cost_fig.clear()
        
        if df.empty:
            ax = self.cost_fig.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, 'Geen data beschikbaar', 
                   ha='center', va='center', transform=ax.transAxes)
            self.cost_canvas.draw()
            return
            
        # Bereken wear costs per materiaal
        material_costs = {}
        material_hours = {}
        
        if 'print_hours' not in df.columns:
            df['print_hours'] = df['weight'] / 20.0
            
        for material in df['material'].unique():
            material_df = df[df['material'] == material]
            total_hours = material_df['print_hours'].sum()
            
            # Bereken wear cost
            wear_cost = calculate_wear_cost(material, total_hours)
            
            material_costs[material] = wear_cost
            material_hours[material] = total_hours
            
        # Sorteer op kosten
        sorted_materials = sorted(material_costs.items(), key=lambda x: x[1], reverse=True)
        
        # Maak subplots
        ax1 = self.cost_fig.add_subplot(2, 2, 1)
        ax2 = self.cost_fig.add_subplot(2, 2, 2)
        ax3 = self.cost_fig.add_subplot(2, 1, 2)
        
        # Plot 1: Top 10 hoogste slijtage kosten
        top_materials = sorted_materials[:10]
        if top_materials:
            materials, costs = zip(*top_materials)
            y_pos = np.arange(len(materials))
            
            bars = ax1.barh(y_pos, costs)
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(materials)
            ax1.set_xlabel('Slijtage Kosten (€)')
            ax1.set_title('Top 10 Hoogste Slijtage Kosten', fontsize=12, fontweight='bold')
            
            # Kleur bars
            for i, (mat, bar) in enumerate(zip(materials, bars)):
                if is_abrasive_material(mat):
                    bar.set_color('#FF6B6B')
                else:
                    bar.set_color('#4ECDC4')
                    
            # Voeg waarde labels toe
            for i, cost in enumerate(costs):
                ax1.text(cost + 0.5, i, f'€{cost:.2f}', va='center')
                
        # Plot 2: Kosten per uur analyse
        ax2.scatter([], [], color='#FF6B6B', label='Abrasief', s=100)
        ax2.scatter([], [], color='#4ECDC4', label='Normaal', s=100)
        
        for material, hours in material_hours.items():
            if hours > 0:
                cost = material_costs[material]
                cost_per_hour = cost / hours
                
                color = '#FF6B6B' if is_abrasive_material(material) else '#4ECDC4'
                ax2.scatter(hours, cost_per_hour, color=color, alpha=0.6, s=100)
                
                # Label alleen significante punten
                if cost_per_hour > 0.5 or hours > 50:
                    ax2.annotate(material, (hours, cost_per_hour), 
                               xytext=(5, 5), textcoords='offset points',
                               fontsize=8, alpha=0.7)
                    
        ax2.set_xlabel('Totale Print Uren')
        ax2.set_ylabel('Slijtage Kosten per Uur (€/u)')
        ax2.set_title('Slijtage Kosten Efficiëntie', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Cumulatieve kosten over tijd
        df_sorted = df.sort_values('timestamp')
        df_sorted['cumulative_cost'] = 0
        
        cumulative = 0
        costs_timeline = []
        dates = []
        
        for _, row in df_sorted.iterrows():
            wear_cost = calculate_wear_cost(row['material'], row['print_hours'])
            cumulative += wear_cost
            costs_timeline.append(cumulative)
            dates.append(row['timestamp'])
            
        ax3.plot(dates, costs_timeline, 'g-', linewidth=2)
        ax3.fill_between(dates, costs_timeline, alpha=0.3, color='green')
        
        ax3.set_xlabel('Datum')
        ax3.set_ylabel('Cumulatieve Slijtage Kosten (€)')
        ax3.set_title('Totale Slijtage Kosten Over Tijd', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Format dates
        for label in ax3.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')
            
        # Voeg totaal label toe
        if len(costs_timeline) > 0:
            ax3.text(0.02, 0.98, f'Totaal: €{costs_timeline[-1]:.2f}', 
                    transform=ax3.transAxes, fontsize=12, fontweight='bold',
                    va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        self.cost_fig.tight_layout()
        self.cost_canvas.draw()
        
    def _create_heatmap(self):
        """Maak gebruik heatmap."""
        analysis_frame = tk.Frame(self.heat_frame, bg=self.colors['white'])
        analysis_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Matplotlib figure
        self.heat_fig = Figure(figsize=(10, 6), facecolor='white')
        
        # Canvas
        self.heat_canvas = FigureCanvasTkAgg(self.heat_fig, master=analysis_frame)
        self.heat_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Period selector
        control_frame = tk.Frame(self.heat_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(control_frame, text="Periode:", bg=self.colors['bg']).pack(side='left', padx=5)
        
        self.heat_period = tk.StringVar(value="week")
        periods = [("Week", "week"), ("Maand", "month"), ("Jaar", "year")]
        
        for text, value in periods:
            tk.Radiobutton(
                control_frame,
                text=text,
                variable=self.heat_period,
                value=value,
                command=self._update_heatmap,
                bg=self.colors['bg']
            ).pack(side='left', padx=5)
        
        # Initial plot
        self._update_heatmap()
        
    def _update_heatmap(self):
        """Update gebruik heatmap."""
        df = self.load_data()
        
        # Clear figure
        self.heat_fig.clear()
        
        if df.empty:
            ax = self.heat_fig.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, 'Geen data beschikbaar', 
                   ha='center', va='center', transform=ax.transAxes)
            self.heat_canvas.draw()
            return
            
        # Voeg print_hours toe als nodig
        if 'print_hours' not in df.columns:
            df['print_hours'] = df['weight'] / 20.0
            
        period = self.heat_period.get()
        
        # Filter data op periode
        now = datetime.now()
        if period == "week":
            start_date = now - timedelta(days=7)
            df_filtered = df[df['timestamp'] >= start_date]
        elif period == "month":
            start_date = now - timedelta(days=30)
            df_filtered = df[df['timestamp'] >= start_date]
        else:  # year
            start_date = now - timedelta(days=365)
            df_filtered = df[df['timestamp'] >= start_date]
            
        if df_filtered.empty:
            ax = self.heat_fig.add_subplot(1, 1, 1)
            ax.text(0.5, 0.5, f'Geen data voor geselecteerde periode', 
                   ha='center', va='center', transform=ax.transAxes)
            self.heat_canvas.draw()
            return
            
        # Maak pivot table voor heatmap
        df_filtered['hour'] = df_filtered['timestamp'].dt.hour
        df_filtered['weekday'] = df_filtered['timestamp'].dt.day_name()
        
        # Groepeer op dag en uur
        pivot = df_filtered.groupby(['weekday', 'hour'])['print_hours'].sum().unstack(fill_value=0)
        
        # Herorden weekdagen
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_names = ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo']
        
        # Filter en herorden
        available_days = [day for day in weekday_order if day in pivot.index]
        pivot = pivot.reindex(available_days)
        
        # Plot heatmap
        ax = self.heat_fig.add_subplot(1, 1, 1)
        
        if not pivot.empty:
            # Gebruik seaborn voor mooiere heatmap
            im = sns.heatmap(
                pivot,
                cmap='YlOrRd',
                annot=True,
                fmt='.1f',
                cbar_kws={'label': 'Print Uren'},
                ax=ax
            )
            
            # Update labels
            day_labels = [weekday_names[weekday_order.index(day)] for day in available_days]
            ax.set_yticklabels(day_labels, rotation=0)
            ax.set_xlabel('Uur van de Dag')
            ax.set_ylabel('Dag van de Week')
            ax.set_title(f'Print Activiteit Heatmap ({period.capitalize()})', 
                        fontsize=12, fontweight='bold')
            
            # Voeg grid toe voor leesbaarheid
            ax.set_xticks(np.arange(24) + 0.5, minor=True)
            ax.set_yticks(np.arange(len(available_days)) + 0.5, minor=True)
            ax.grid(which='minor', color='white', linestyle='-', linewidth=1)
            
        self.heat_fig.tight_layout()
        self.heat_canvas.draw()
        
    def _create_control_panel(self):
        """Maak control panel voor refresh en export."""
        control_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Refresh button
        tk.Button(
            control_frame,
            text="🔄 Refresh Grafieken",
            command=self.update_analysis,
            font=("Arial", 10),
            bg=self.colors['primary'],
            fg='white',
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        # Export button
        tk.Button(
            control_frame,
            text="💾 Export Grafieken",
            command=self.export_charts,
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        # Info label
        self.info_label = tk.Label(
            control_frame,
            text="",
            font=("Arial", 9),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.info_label.pack(side='right', padx=10)
        
    def analyze(self) -> Dict[str, Any]:
        """Basis analyse voor grafieken."""
        df = self.load_data()
        
        if df.empty:
            return {'total_records': 0, 'date_range': 'Geen data'}
            
        return {
            'total_records': len(df),
            'date_range': f"{df['timestamp'].min().date()} - {df['timestamp'].max().date()}"
        }
        
    def update_analysis(self) -> None:
        """Update alle grafieken."""
        # Update elke grafiek
        self._update_distribution_chart()
        self._update_trend_chart()
        self._update_cost_chart()
        self._update_heatmap()
        
        # Update info
        results = self.analyze()
        self.info_label.configure(
            text=f"📊 {results['total_records']} records | 📅 {results['date_range']}"
        )
        
    def export_charts(self):
        """Export alle grafieken als PNG bestanden."""
        from tkinter import filedialog, messagebox
        
        # Vraag om directory
        export_dir = filedialog.askdirectory(
            title="Selecteer Export Directory"
        )
        
        if not export_dir:
            return
            
        try:
            # Export elke grafiek
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Distribution chart
            self.dist_fig.savefig(
                f"{export_dir}/slijtage_verdeling_{timestamp}.png",
                dpi=300, bbox_inches='tight'
            )
            
            # Trend chart
            self.trend_fig.savefig(
                f"{export_dir}/slijtage_trend_{timestamp}.png",
                dpi=300, bbox_inches='tight'
            )
            
            # Cost chart
            self.cost_fig.savefig(
                f"{export_dir}/slijtage_kosten_{timestamp}.png",
                dpi=300, bbox_inches='tight'
            )
            
            # Heatmap
            self.heat_fig.savefig(
                f"{export_dir}/slijtage_heatmap_{timestamp}.png",
                dpi=300, bbox_inches='tight'
            )
            
            messagebox.showinfo(
                "Export Succesvol",
                f"✅ Grafieken geëxporteerd naar:\n{export_dir}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Export Fout",
                f"Kon grafieken niet exporteren:\n{str(e)}"
            ) 