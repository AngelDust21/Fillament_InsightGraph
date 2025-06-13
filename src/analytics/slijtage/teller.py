"""
Abrasive Material Teller - H2D Price Calculator
==============================================

Deze module houdt bij hoeveel uren er met abrasieve materialen
is geprint. Dit is belangrijk voor:
- Nozzle vervanging planning
- Onderhoud kosten tracking
- Slijtage waarschuwingen

Educatieve waarde:
- Laat zien hoe kleine variabelen (0.50€/uur) grote impact hebben
- Belang van preventief onderhoud
- Data-driven maintenance beslissingen
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
import os

from ..base_analysis import BaseAnalysis
from ...materials.material_properties import (
    get_material_properties, 
    calculate_wear_cost,
    is_abrasive_material
)


class AbrasiveTeller(BaseAnalysis):
    """Telt en analyseert abrasieve materiaal gebruik.
    
    Houdt bij:
    - Totale uren met abrasieve materialen
    - Geschatte nozzle slijtage
    - Onderhouds waarschuwingen
    - Kosten impact
    """
    
    # Constantes voor slijtage berekeningen
    NOZZLE_LIFETIME_HOURS = 250  # Gemiddelde levensduur hardened nozzle
    NOZZLE_COST = 25.00  # Kosten vervanging nozzle
    WARNING_THRESHOLD = 0.8  # Waarschuwing bij 80% slijtage
    
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "🔧 Abrasive Material Uren Teller"
        
    def create_analysis_widgets(self) -> None:
        """Creëer de teller interface."""
        # Check of er data is
        df = self.load_data()
        if df.empty:
            self.show_no_data_message()
            return
            
        # Hoofdcontainer met 3 kolommen
        container = tk.Frame(self.main_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)
        
        # === LINKER KOLOM: Teller Display ===
        self._create_counter_display(container)
        
        # === MIDDEN KOLOM: Progress Bars ===
        self._create_progress_display(container)
        
        # === RECHTER KOLOM: Waarschuwingen ===
        self._create_warning_display(container)
        
        # === ONDERSTE SECTIE: Details ===
        self._create_details_section()
        
        # Initial update - alleen als alle widgets bestaan
        try:
            self.update_analysis()
        except Exception as e:
            print(f"Waarschuwing: Kon analyse niet updaten: {e}")
        
    def _create_counter_display(self, parent: tk.Frame) -> None:
        """Creëer de hoofdteller display."""
        left_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5), pady=5)
        
        # Titel met info knop
        title_frame = tk.Frame(left_frame, bg=self.colors['white'])
        title_frame.pack(pady=(10, 5))
        
        tk.Label(
            title_frame,
            text="Abrasieve Uren",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(side='left')
        
        # Info knop
        info_btn = tk.Button(
            title_frame,
            text="ℹ️",
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            bd=1,
            relief=tk.FLAT,
            cursor='hand2',
            command=self._show_info_dialog
        )
        info_btn.pack(side='left', padx=(10, 0))
        self._create_tooltip(info_btn, "Uitleg over deze module")
        
        # Diagram knop
        diagram_btn = tk.Button(
            title_frame,
            text="📊",
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['secondary'],
            bd=1,
            relief=tk.FLAT,
            cursor='hand2',
            command=self._show_relationship_diagram
        )
        diagram_btn.pack(side='left', padx=(5, 0))
        self._create_tooltip(diagram_btn, "Visueel diagram van de relatie")
        
        # Grote teller
        self.counter_label = tk.Label(
            left_frame,
            text="0.0",
            font=("Arial", 36, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        self.counter_label.pack()
        
        tk.Label(
            left_frame,
            text="totale uren",
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack()
        
        # Separator
        tk.Frame(left_frame, height=2, bg=self.colors['light_gray']).pack(fill='x', pady=10, padx=20)
        
        # Kosten impact
        tk.Label(
            left_frame,
            text="Extra Slijtagekosten",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack()
        
        self.cost_label = tk.Label(
            left_frame,
            text="€ 0.00",
            font=("Arial", 16, "bold"),
            bg=self.colors['white'],
            fg=self.colors['secondary']
        )
        self.cost_label.pack()
        
    def _create_progress_display(self, parent: tk.Frame) -> None:
        """Creëer nozzle slijtage progress bars."""
        middle_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        middle_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Titel
        tk.Label(
            middle_frame,
            text="Nozzle Slijtage Status",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=(10, 15))
        
        # Progress container
        progress_container = tk.Frame(middle_frame, bg=self.colors['white'])
        progress_container.pack(fill='both', expand=True, padx=20)
        
        # Huidige nozzle levensduur
        tk.Label(
            progress_container,
            text="Huidige Nozzle:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).pack(anchor='w')
        
        self.nozzle_progress = ttk.Progressbar(
            progress_container,
            orient='horizontal',
            length=200,
            mode='determinate'
        )
        self.nozzle_progress.pack(fill='x', pady=(5, 10))
        
        self.nozzle_percent_label = tk.Label(
            progress_container,
            text="0% versleten",
            font=("Arial", 9),
            bg=self.colors['white']
        )
        self.nozzle_percent_label.pack()
        
        # Separator
        tk.Frame(progress_container, height=2, bg=self.colors['light_gray']).pack(fill='x', pady=15)
        
        # Vervangingen teller
        tk.Label(
            progress_container,
            text="Totaal Vervangingen:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).pack(anchor='w')
        
        self.replacements_label = tk.Label(
            progress_container,
            text="0 keer",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        self.replacements_label.pack()
        
        # Link naar maintenance tab
        tk.Frame(progress_container, height=2, bg=self.colors['light_gray']).pack(fill='x', pady=10)
        
        link_label = tk.Label(
            progress_container,
            text="💡 Zie 'Maintenance' tab voor\nhuidige nozzle details",
            font=("Arial", 9, "italic"),
            bg=self.colors['white'],
            fg=self.colors['secondary'],
            cursor='hand2'
        )
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: self._show_maintenance_hint())
        
    def _create_warning_display(self, parent: tk.Frame) -> None:
        """Creëer waarschuwingen panel."""
        right_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        right_frame.pack(side='left', fill='both', expand=True, padx=(5, 0), pady=5)
        
        # Titel
        tk.Label(
            right_frame,
            text="⚠️ Waarschuwingen",
            font=("Arial", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        ).pack(pady=(10, 15))
        
        # Waarschuwingen container
        self.warnings_frame = tk.Frame(right_frame, bg=self.colors['white'])
        self.warnings_frame.pack(fill='both', expand=True, padx=10)
        
        # Placeholder
        self.no_warnings_label = tk.Label(
            self.warnings_frame,
            text="✅ Geen waarschuwingen",
            font=("Arial", 11),
            bg=self.colors['white'],
            fg='green'
        )
        self.no_warnings_label.pack(pady=20)
        
    def _create_details_section(self) -> None:
        """Creëer gedetailleerde statistieken sectie."""
        details_frame = tk.LabelFrame(
            self.main_frame,
            text="📊 Gedetailleerde Statistieken",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        details_frame.pack(fill='x', pady=(10, 0))
        
        # Grid voor statistieken
        stats_grid = tk.Frame(details_frame, bg=self.colors['white'])
        stats_grid.pack(padx=20, pady=10)
        
        # Kolom headers
        headers = ["Periode", "Abrasieve Uren", "Totale Uren", "Percentage", "Impact"]
        for i, header in enumerate(headers):
            tk.Label(
                stats_grid,
                text=header,
                font=("Arial", 10, "bold"),
                bg=self.colors['white'],
                fg=self.colors['text']
            ).grid(row=0, column=i, padx=10, pady=5, sticky='w')
            
        # Data rijen (worden gevuld door update_analysis)
        self.stats_labels = []
        periods = ["Vandaag", "Deze Week", "Deze Maand", "Totaal"]
        for i, period in enumerate(periods):
            row_labels = []
            for j in range(5):
                label = tk.Label(
                    stats_grid,
                    text="-",
                    font=("Arial", 9),
                    bg=self.colors['white'],
                    fg=self.colors['text']
                )
                label.grid(row=i+1, column=j, padx=10, pady=3, sticky='w')
                row_labels.append(label)
            self.stats_labels.append(row_labels)
            
    def analyze(self) -> Dict[str, Any]:
        """Analyseer abrasieve materiaal gebruik."""
        df = self.load_data()
        if df.empty:
            return self._empty_results()
            
        # Debug info
        print(f"DEBUG Teller: Geladen {len(df)} records")
        if 'abrasive' in df.columns:
            print(f"DEBUG Teller: Abrasive kolom gevonden, type: {df['abrasive'].dtype}")
            print(f"DEBUG Teller: Unieke waarden: {df['abrasive'].unique()}")
        
        # Bereken print_hours als deze niet bestaat
        if 'print_hours' not in df.columns:
            # Schat print tijd op basis van gewicht (ongeveer 20g/uur gemiddeld)
            # Dit is een ruwe schatting die varieert per materiaal
            df['print_hours'] = df['weight'] / 20.0
            
        # Filter alleen abrasieve prints
        abrasive_df = df[df['abrasive'] == True].copy()
        
        # Bereken totalen
        total_abrasive_hours = abrasive_df['print_hours'].sum()
        total_all_hours = df['print_hours'].sum()
        abrasive_percentage = (total_abrasive_hours / total_all_hours * 100) if total_all_hours > 0 else 0
        
        # Bereken slijtage kosten - NU MET ECHTE MATERIAL PROPERTIES!
        total_wear_cost = 0
        for _, row in abrasive_df.iterrows():
            material_name = row.get('material', 'Unknown')
            print_hours = row.get('print_hours', 0)
            
            # Gebruik de echte wear cost calculator
            wear_cost = calculate_wear_cost(material_name, print_hours)
            total_wear_cost += wear_cost
            
        # Voor backwards compatibility, als we geen materiaal data hebben
        if total_wear_cost == 0 and total_abrasive_hours > 0:
            # Fallback naar gemiddelde van CF/GF materialen (ongeveer €1.20/uur)
            total_wear_cost = total_abrasive_hours * 1.20
        
        # Bereken nozzle status
        nozzle_wear_percent = (total_abrasive_hours % self.NOZZLE_LIFETIME_HOURS) / self.NOZZLE_LIFETIME_HOURS * 100
        replacements = int(total_abrasive_hours // self.NOZZLE_LIFETIME_HOURS)
        
        # Periode analyses
        now = datetime.now()
        today = now.date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        periods = {
            'today': self._analyze_period(abrasive_df, df, today, today),
            'week': self._analyze_period(abrasive_df, df, week_start, today),
            'month': self._analyze_period(abrasive_df, df, month_start, today),
            'total': {
                'abrasive_hours': total_abrasive_hours,
                'total_hours': total_all_hours,
                'percentage': abrasive_percentage,
                'cost': total_wear_cost
            }
        }
        
        # Genereer waarschuwingen
        warnings = []
        if nozzle_wear_percent >= self.WARNING_THRESHOLD * 100:
            warnings.append({
                'level': 'high',
                'message': f'Nozzle is {nozzle_wear_percent:.0f}% versleten!'
            })
        
        if abrasive_percentage > 30:
            warnings.append({
                'level': 'medium',
                'message': f'{abrasive_percentage:.0f}% van prints zijn abrasief'
            })
            
        return {
            'total_abrasive_hours': total_abrasive_hours,
            'total_cost': total_wear_cost,
            'nozzle_wear_percent': nozzle_wear_percent,
            'replacements': replacements,
            'periods': periods,
            'warnings': warnings
        }
        
    def _analyze_period(self, abrasive_df: pd.DataFrame, all_df: pd.DataFrame,
                       start_date, end_date) -> Dict[str, float]:
        """Analyseer een specifieke periode."""
        # Zorg dat print_hours bestaat
        if 'print_hours' not in abrasive_df.columns:
            abrasive_df['print_hours'] = abrasive_df['weight'] / 20.0
        if 'print_hours' not in all_df.columns:
            all_df['print_hours'] = all_df['weight'] / 20.0
            
        # Filter op datum range
        mask_abrasive = (abrasive_df['timestamp'].dt.date >= start_date) & \
                       (abrasive_df['timestamp'].dt.date <= end_date)
        mask_all = (all_df['timestamp'].dt.date >= start_date) & \
                   (all_df['timestamp'].dt.date <= end_date)
        
        period_abrasive_df = abrasive_df[mask_abrasive]
        period_all_df = all_df[mask_all]
        
        period_abrasive_hours = period_abrasive_df['print_hours'].sum()
        period_all_hours = period_all_df['print_hours'].sum()
        
        percentage = (period_abrasive_hours / period_all_hours * 100) if period_all_hours > 0 else 0
        
        # Bereken wear cost voor deze periode met echte material properties
        period_wear_cost = 0
        for _, row in period_abrasive_df.iterrows():
            material_name = row.get('material', 'Unknown')
            print_hours = row.get('print_hours', 0)
            wear_cost = calculate_wear_cost(material_name, print_hours)
            period_wear_cost += wear_cost
            
        # Fallback als geen material data
        if period_wear_cost == 0 and period_abrasive_hours > 0:
            period_wear_cost = period_abrasive_hours * 1.20
        
        return {
            'abrasive_hours': period_abrasive_hours,
            'total_hours': period_all_hours,
            'percentage': percentage,
            'cost': period_wear_cost
        }
        
    def _empty_results(self) -> Dict[str, Any]:
        """Return lege resultaten structuur."""
        return {
            'total_abrasive_hours': 0,
            'total_cost': 0,
            'nozzle_wear_percent': 0,
            'replacements': 0,
            'periods': {
                'today': {'abrasive_hours': 0, 'total_hours': 0, 'percentage': 0, 'cost': 0},
                'week': {'abrasive_hours': 0, 'total_hours': 0, 'percentage': 0, 'cost': 0},
                'month': {'abrasive_hours': 0, 'total_hours': 0, 'percentage': 0, 'cost': 0},
                'total': {'abrasive_hours': 0, 'total_hours': 0, 'percentage': 0, 'cost': 0}
            },
            'warnings': []
        }
        
    def update_analysis(self) -> None:
        """Update de visualisatie met nieuwe data."""
        results = self.analyze()
        
        # Update hoofdteller
        self.counter_label.configure(text=f"{results['total_abrasive_hours']:.1f}")
        self.cost_label.configure(text=f"€ {results['total_cost']:.2f}")
        
        # Update nozzle progress
        self.nozzle_progress['value'] = results['nozzle_wear_percent']
        self.nozzle_percent_label.configure(text=f"{results['nozzle_wear_percent']:.0f}% versleten")
        
        # Kleur progress bar op basis van slijtage
        if results['nozzle_wear_percent'] >= 80:
            self.nozzle_percent_label.configure(fg='red')
        elif results['nozzle_wear_percent'] >= 60:
            self.nozzle_percent_label.configure(fg='orange')
        else:
            self.nozzle_percent_label.configure(fg='green')
            
        # Update vervangingen
        self.replacements_label.configure(text=f"{results['replacements']} keer")
        
        # Update waarschuwingen
        self._update_warnings(results['warnings'])
        
        # Update statistieken tabel
        self._update_stats_table(results['periods'])
        
    def _update_warnings(self, warnings: list) -> None:
        """Update waarschuwingen display."""
        # Clear bestaande waarschuwingen
        for widget in self.warnings_frame.winfo_children():
            widget.destroy()
            
        if not warnings:
            # Geen waarschuwingen
            tk.Label(
                self.warnings_frame,
                text="✅ Geen waarschuwingen",
                font=("Arial", 11),
                bg=self.colors['white'],
                fg='green'
            ).pack(pady=20)
        else:
            # Toon waarschuwingen
            for warning in warnings:
                color = 'red' if warning['level'] == 'high' else 'orange'
                icon = '🔴' if warning['level'] == 'high' else '🟡'
                
                warning_frame = tk.Frame(self.warnings_frame, bg=self.colors['white'])
                warning_frame.pack(fill='x', pady=5)
                
                tk.Label(
                    warning_frame,
                    text=f"{icon} {warning['message']}",
                    font=("Arial", 10),
                    bg=self.colors['white'],
                    fg=color,
                    wraplength=200,
                    justify='left'
                ).pack(anchor='w')
                
    def _update_stats_table(self, periods: Dict[str, Dict]) -> None:
        """Update de statistieken tabel."""
        period_keys = ['today', 'week', 'month', 'total']
        period_names = ['Vandaag', 'Deze Week', 'Deze Maand', 'Totaal']
        
        for i, (key, name) in enumerate(zip(period_keys, period_names)):
            data = periods[key]
            
            # Update rij
            self.stats_labels[i][0].configure(text=name)
            self.stats_labels[i][1].configure(text=f"{data['abrasive_hours']:.1f} u")
            self.stats_labels[i][2].configure(text=f"{data['total_hours']:.1f} u")
            self.stats_labels[i][3].configure(text=f"{data['percentage']:.0f}%")
            self.stats_labels[i][4].configure(text=f"€ {data['cost']:.2f}")
            
            # Highlight hoge percentages
            if data['percentage'] > 30:
                self.stats_labels[i][3].configure(fg='red')
            elif data['percentage'] > 20:
                self.stats_labels[i][3].configure(fg='orange')
            else:
                self.stats_labels[i][3].configure(fg=self.colors['text'])
                
    def _show_info_dialog(self):
        """Toon uitleg over de Abrasieve Uren Teller."""
        info_window = tk.Toplevel(self.main_frame)
        info_window.title("Info - Abrasieve Uren Teller")
        info_window.geometry("600x550")
        info_window.configure(bg='white')
        
        # Center het venster
        info_window.update_idletasks()
        x = (info_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (info_window.winfo_screenheight() // 2) - (550 // 2)
        info_window.geometry(f"+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(info_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📚 Uitleg: Abrasieve Uren Teller",
            font=("Arial", 16, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(expand=True)
        
        # Content
        content_frame = tk.Frame(info_window, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        info_text = """
🔧 WAT DOET DEZE MODULE?

Deze module houdt het TOTALE gebruik van abrasieve materialen bij sinds het begin.
Dit omvat alle prints met Carbon Fiber (CF) of Glass Fiber (GF) materialen.

📊 WAT BETEKENEN DE GETALLEN?

• Abrasieve Uren: Totaal aantal uren dat er met CF/GF is geprint
• Slijtagekosten: Extra kosten door nozzle vervanging (€1.20/uur gemiddeld)
• Progress Bar: Toont slijtage van de HUIDIGE nozzle (0-100%)
• Vervangingen: Aantal keer dat een nozzle vervangen zou moeten zijn

⚡ VERSCHIL MET MAINTENANCE TAB:

• Deze tab: Toont HISTORISCH TOTAAL (alle abrasieve uren ooit)
• Maintenance tab: Toont HUIDIGE NOZZLE status (sinds laatste vervanging)

Voorbeeld:
- Totaal 506 uren abrasief geprint = 2x nozzle vervangen
- Huidige nozzle: 76% versleten (190 van 250 uur gebruikt)

💡 WAAROM IS DIT BELANGRIJK?

Abrasieve materialen slijten nozzles veel sneller:
• Brass nozzle: Ongeschikt voor CF/GF
• Hardened Steel: ~250 uur levensduur
• Ruby nozzle: ~1500 uur levensduur (duurder maar economischer)

De teller helpt je om:
1. Onderhoudskosten te voorspellen
2. Te beslissen wanneer een duurdere nozzle rendabel is
3. Preventief onderhoud te plannen
"""
        
        text_widget = tk.Text(
            content_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg='white',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', info_text)
        text_widget.configure(state='disabled')
        
        # Close button
        close_btn = tk.Button(
            info_window,
            text="Sluiten",
            font=("Arial", 11),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=8,
            bd=0,
            cursor='hand2',
            command=info_window.destroy
        )
        close_btn.pack(pady=10)
        
        # Focus
        info_window.focus_set()
        info_window.grab_set()
        
    def _show_maintenance_hint(self):
        """Toon hint over maintenance tab."""
        messagebox.showinfo(
            "Maintenance Tab",
            "De 'Maintenance' tab toont details over je HUIDIGE nozzle:\n\n"
            "• Hoeveel % de huidige nozzle versleten is\n"
            "• Wanneer je moet vervangen\n"
            "• Slimme aanbevelingen\n\n"
                         "Terwijl deze tab het TOTAAL van alle abrasieve uren toont.",
            parent=self.main_frame
        )
        
    def _show_relationship_diagram(self):
        """Toon visueel diagram van de relatie tussen de tabs."""
        diagram_window = tk.Toplevel(self.main_frame)
        diagram_window.title("Relatie Diagram - Slijtage Modules")
        diagram_window.geometry("800x600")
        diagram_window.configure(bg='white')
        
        # Center het venster
        diagram_window.update_idletasks()
        x = (diagram_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (diagram_window.winfo_screenheight() // 2) - (600 // 2)
        diagram_window.geometry(f"+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(diagram_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 Visuele Uitleg: Relatie tussen Abrasieve Uren & Maintenance",
            font=("Arial", 16, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(expand=True)
        
        # Canvas voor diagram
        canvas = tk.Canvas(diagram_window, width=760, height=450, bg='white', highlightthickness=0)
        canvas.pack(pady=20)
        
        # Teken het diagram
        self._draw_relationship_diagram(canvas)
        
        # Close button
        close_btn = tk.Button(
            diagram_window,
            text="Sluiten",
            font=("Arial", 11),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=8,
            bd=0,
            cursor='hand2',
            command=diagram_window.destroy
        )
        close_btn.pack(pady=10)
        
        diagram_window.focus_set()
        diagram_window.grab_set()
        
    def _draw_relationship_diagram(self, canvas):
        """Teken het relatie diagram op de canvas."""
        # Kleuren
        color_total = '#E8F5E9'  # Licht groen
        color_current = '#FFF3E0'  # Licht oranje
        color_relation = '#E3F2FD'  # Licht blauw
        
        # Box 1: Abrasieve Uren Teller (Links)
        canvas.create_rectangle(30, 50, 330, 180, fill=color_total, outline='#4CAF50', width=2)
        canvas.create_text(180, 70, text="🔧 ABRASIEVE UREN TELLER", font=("Arial", 14, "bold"), fill='#2E7D32')
        canvas.create_text(180, 95, text="Historisch Totaal", font=("Arial", 11, "italic"), fill='#388E3C')
        canvas.create_text(180, 130, text="506 totale uren", font=("Arial", 20, "bold"), fill='#1B5E20')
        canvas.create_text(180, 155, text="met CF/GF materialen", font=("Arial", 10), fill='#2E7D32')
        
        # Box 2: Maintenance (Rechts)
        canvas.create_rectangle(430, 50, 730, 180, fill=color_current, outline='#FF9800', width=2)
        canvas.create_text(580, 70, text="⚠️ MAINTENANCE", font=("Arial", 14, "bold"), fill='#E65100')
        canvas.create_text(580, 95, text="Huidige Nozzle Status", font=("Arial", 11, "italic"), fill='#F57C00')
        canvas.create_text(580, 130, text="76% versleten", font=("Arial", 20, "bold"), fill='#E65100')
        canvas.create_text(580, 155, text="(190 van 250 uur)", font=("Arial", 10), fill='#F57C00')
        
        # Pijlen naar beneden
        canvas.create_line(180, 180, 180, 250, arrow=tk.LAST, width=3, fill='#4CAF50')
        canvas.create_line(580, 180, 580, 250, arrow=tk.LAST, width=3, fill='#FF9800')
        
        # Berekening boxes
        canvas.create_rectangle(80, 250, 280, 320, fill='#F5F5F5', outline='#9E9E9E', width=1)
        canvas.create_text(180, 270, text="Nozzle levensduur:", font=("Arial", 10), fill='#424242')
        canvas.create_text(180, 285, text="250 uur per stuk", font=("Arial", 11, "bold"), fill='#212121')
        canvas.create_text(180, 305, text="506 ÷ 250 = 2.02", font=("Arial", 10), fill='#616161')
        
        canvas.create_rectangle(480, 250, 680, 320, fill='#F5F5F5', outline='#9E9E9E', width=1)
        canvas.create_text(580, 270, text="Sinds installatie:", font=("Arial", 10), fill='#424242')
        canvas.create_text(580, 285, text="190 uur geprint", font=("Arial", 11, "bold"), fill='#212121')
        canvas.create_text(580, 305, text="190 ÷ 250 = 76%", font=("Arial", 10), fill='#616161')
        
        # Pijlen naar relatie box
        canvas.create_line(180, 320, 380, 380, arrow=tk.LAST, width=2, fill='#757575')
        canvas.create_line(580, 320, 380, 380, arrow=tk.LAST, width=2, fill='#757575')
        
        # Relatie box (Onderaan)
        canvas.create_rectangle(200, 380, 560, 480, fill=color_relation, outline='#2196F3', width=3)
        canvas.create_text(380, 400, text="🔗 RELATIE", font=("Arial", 14, "bold"), fill='#0D47A1')
        canvas.create_text(380, 425, text="Je hebt al 2 nozzles volledig opgebruikt", font=("Arial", 11), fill='#1565C0')
        canvas.create_text(380, 445, text="en bent nu 76% bezig met de 3e nozzle", font=("Arial", 11), fill='#1565C0')
        canvas.create_text(380, 465, text="Totaal: 2.02 × 250 = ±506 uur", font=("Arial", 10, "italic"), fill='#1976D2')
        
        # Educatieve tip onderaan
        canvas.create_text(380, 520, text="💡 TIP: Bij 80% slijtage krijg je een waarschuwing om een nieuwe nozzle te bestellen!", 
                          font=("Arial", 10, "italic"), fill='#666666')
                          
    def _create_tooltip(self, widget, text):
        """Creëer een simpele tooltip voor een widget."""
        def on_enter(event):
            # Maak tooltip window
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                font=("Arial", 9),
                bg='#FFFFE0',
                fg='black',
                relief=tk.SOLID,
                borderwidth=1,
                padx=5,
                pady=2
            )
            label.pack()
            
            # Sla tooltip op in widget
            widget.tooltip = tooltip
            
        def on_leave(event):
            # Verwijder tooltip
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
                
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave) 