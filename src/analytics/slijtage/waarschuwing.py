"""
Nozzle Maintenance Waarschuwing Systeem - H2D Price Calculator
===========================================================

Deze module geeft proactieve waarschuwingen voor nozzle onderhoud
gebaseerd op actuele slijtage data. Features:
- Real-time tracking van nozzle levensduur
- Multi-level waarschuwingen (80%, 90%, 100%)
- Maintenance history tracking
- Smart recommendations per materiaal type

Educatieve waarde:
- Predictive maintenance concepten
- Cost-benefit analyse van preventief onderhoud
- Data-driven beslissingen
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import json
import os

from ..base_analysis import BaseAnalysis
from ...materials.material_properties import (
    get_material_properties,
    get_nozzle_recommendation,
    MATERIAL_PROPERTIES
)


class MaintenanceWarningSystem(BaseAnalysis):
    """Intelligent waarschuwing systeem voor nozzle onderhoud.
    
    Houdt bij:
    - Huidige nozzle status en levensduur
    - Maintenance history
    - Cost-benefit analyses
    - Smart recommendations
    """
    
    # Waarschuwing niveaus
    WARNING_LEVELS = {
        'low': {'threshold': 60, 'color': '#FFA500', 'icon': '🟡'},
        'medium': {'threshold': 80, 'color': '#FF6347', 'icon': '🟠'},
        'high': {'threshold': 90, 'color': '#FF0000', 'icon': '🔴'},
        'critical': {'threshold': 100, 'color': '#8B0000', 'icon': '⚠️'}
    }
    
    # Nozzle levensduur per type (in uren abrasief printen)
    NOZZLE_LIFETIMES = {
        'Brass 0.4mm': 50,           # Niet geschikt voor abrasief
        'Brass 0.6mm': 50,           # Niet geschikt voor abrasief
        'Hardened 0.4mm': 250,       # Standaard voor CF/GF
        'Hardened 0.6mm': 250,       # Standaard voor CF/GF
        'Hardened Steel': 250,       # Standaard voor CF/GF
        'Ruby Nozzle': 1500,         # Premium optie
        'Tungsten Carbide': 1000     # Premium optie
    }
    
    def __init__(self, data_manager, parent_frame=None, colors=None):
        super().__init__(data_manager, parent_frame, colors)
        
        # Bepaal maintenance file pad op een veiligere manier
        try:
            if hasattr(data_manager, 'base_path'):
                base_dir = os.path.dirname(data_manager.base_path)
            elif hasattr(data_manager, 'base_dir'):
                base_dir = data_manager.base_dir
            else:
                # Fallback naar project root
                base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
                
            self.maintenance_file = os.path.join(base_dir, 'nozzle_maintenance.json')
        except Exception as e:
            print(f"Waarschuwing: Kon maintenance file pad niet bepalen: {e}")
            # Gebruik huidige directory als fallback
            self.maintenance_file = 'nozzle_maintenance.json'
            
        self.load_maintenance_data()
        
    def load_maintenance_data(self):
        """Laad maintenance history uit persistent storage."""
        try:
            if os.path.exists(self.maintenance_file):
                with open(self.maintenance_file, 'r') as f:
                    self.maintenance_data = json.load(f)
            else:
                self.maintenance_data = {
                    'current_nozzle': {
                        'type': 'Hardened Steel',
                        'install_date': datetime.now().isoformat(),
                        'accumulated_hours': 0,
                        'material_history': {}
                    },
                    'history': []
                }
        except Exception as e:
            print(f"Waarschuwing: Kon maintenance data niet laden: {e}")
            self.maintenance_data = self._default_maintenance_data()
            
    def save_maintenance_data(self):
        """Sla maintenance data op."""
        try:
            with open(self.maintenance_file, 'w') as f:
                json.dump(self.maintenance_data, f, indent=2)
        except Exception as e:
            print(f"Fout bij opslaan maintenance data: {e}")
            
    def _default_maintenance_data(self):
        """Default maintenance data structuur."""
        return {
            'current_nozzle': {
                'type': 'Hardened Steel',
                'install_date': datetime.now().isoformat(),
                'accumulated_hours': 0,
                'material_history': {}
            },
            'history': []
        }
        
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "⚠️ Nozzle Maintenance Waarschuwingen"
        
    def create_analysis_widgets(self) -> None:
        """Creëer de maintenance waarschuwing interface."""
        # Hoofdcontainer
        container = tk.Frame(self.main_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)
        
        # Bovenste rij: Status en waarschuwingen
        top_row = tk.Frame(container, bg=self.colors['bg'])
        top_row.pack(fill='x', padx=5, pady=5)
        
        # Linker paneel: Huidige status
        self._create_status_panel(top_row)
        
        # Rechter paneel: Active waarschuwingen
        self._create_warnings_panel(top_row)
        
        # Middelste sectie: Recommendations
        self._create_recommendations_panel(container)
        
        # Onderste sectie: History en acties
        self._create_history_panel(container)
        
        # Initial update
        self.update_analysis()
        
    def _create_status_panel(self, parent):
        """Maak status panel voor huidige nozzle."""
        # Frame voor LabelFrame met info knop
        status_container = tk.Frame(parent, bg=self.colors['bg'])
        status_container.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Custom header met info knop
        header_frame = tk.Frame(status_container, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text="🔧 Huidige Nozzle Status",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(side='left', padx=10, pady=5)
        
        # Info knop
        info_btn = tk.Button(
            header_frame,
            text="ℹ️",
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            bd=1,
            relief=tk.FLAT,
            cursor='hand2',
            command=self._show_info_dialog
        )
        info_btn.pack(side='right', padx=10)
        self._create_tooltip(info_btn, "Uitleg over deze module")
        
        # Diagram knop
        diagram_btn = tk.Button(
            header_frame,
            text="📊",
            font=("Arial", 10),
            bg=self.colors['white'],
            fg=self.colors['secondary'],
            bd=1,
            relief=tk.FLAT,
            cursor='hand2',
            command=self._show_relationship_diagram
        )
        diagram_btn.pack(side='right', padx=(0, 5))
        self._create_tooltip(diagram_btn, "Visueel diagram van de relatie")
        
        # Status frame content
        status_frame = tk.Frame(status_container, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        status_frame.pack(fill='both', expand=True, side='bottom')
        
        # Nozzle type
        tk.Label(
            status_frame,
            text="Type:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        self.nozzle_type_label = tk.Label(
            status_frame,
            text=self.maintenance_data['current_nozzle']['type'],
            font=("Arial", 10, "bold"),
            bg=self.colors['white'],
            fg=self.colors['primary']
        )
        self.nozzle_type_label.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        # Installatie datum
        tk.Label(
            status_frame,
            text="Geïnstalleerd:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        install_date = datetime.fromisoformat(
            self.maintenance_data['current_nozzle']['install_date']
        )
        self.install_date_label = tk.Label(
            status_frame,
            text=install_date.strftime("%d-%m-%Y"),
            font=("Arial", 10),
            bg=self.colors['white']
        )
        self.install_date_label.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        # Levensduur progress
        tk.Label(
            status_frame,
            text="Levensduur:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        
        progress_frame = tk.Frame(status_frame, bg=self.colors['white'])
        progress_frame.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        self.lifetime_progress = ttk.Progressbar(
            progress_frame,
            length=150,
            mode='determinate'
        )
        self.lifetime_progress.pack(side='left', padx=(0, 10))
        
        self.lifetime_label = tk.Label(
            progress_frame,
            text="0%",
            font=("Arial", 9),
            bg=self.colors['white']
        )
        self.lifetime_label.pack(side='left')
        
        # Geschatte resterende tijd
        tk.Label(
            status_frame,
            text="Resterend:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        
        self.remaining_label = tk.Label(
            status_frame,
            text="Berekenen...",
            font=("Arial", 10, "bold"),
            bg=self.colors['white'],
            fg='green'
        )
        self.remaining_label.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        
        # Separator
        separator = tk.Frame(status_frame, height=2, bg=self.colors['light_gray'])
        separator.grid(row=4, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        
        # Relatie uitleg
        relatie_frame = tk.Frame(status_frame, bg='#F0F8FF')
        relatie_frame.grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=(0, 10))
        
        tk.Label(
            relatie_frame,
            text="ℹ️ Deze tab toont alleen de HUIDIGE nozzle.\nDe 'Abrasieve Uren' tab toont het TOTAAL.",
            font=("Arial", 8, "italic"),
            bg='#F0F8FF',
            fg='#4169E1',
            wraplength=200,
            justify='left'
        ).pack(padx=10, pady=5)
        
        status_frame.columnconfigure(1, weight=1)
        
    def _create_warnings_panel(self, parent):
        """Maak waarschuwingen panel."""
        warnings_frame = tk.LabelFrame(
            parent,
            text="🚨 Actieve Waarschuwingen",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        warnings_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Scrollable frame voor waarschuwingen
        self.warnings_container = tk.Frame(warnings_frame, bg=self.colors['white'])
        self.warnings_container.pack(fill='both', expand=True, padx=10, pady=10)
        
    def _create_recommendations_panel(self, parent):
        """Maak recommendations panel."""
        rec_frame = tk.LabelFrame(
            parent,
            text="💡 Aanbevelingen",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        rec_frame.pack(fill='x', padx=5, pady=5)
        
        self.recommendations_text = tk.Text(
            rec_frame,
            height=4,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg=self.colors['light_gray'],
            relief=tk.FLAT
        )
        self.recommendations_text.pack(fill='x', padx=10, pady=10)
        
    def _create_history_panel(self, parent):
        """Maak maintenance history panel."""
        history_frame = tk.LabelFrame(
            parent,
            text="📜 Maintenance Historie",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        history_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview voor history
        columns = ('Datum', 'Type', 'Levensduur', 'Reden')
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show='headings',
            height=6
        )
        
        # Kolom configuratie
        self.history_tree.heading('Datum', text='Vervangen op')
        self.history_tree.heading('Type', text='Nozzle Type')
        self.history_tree.heading('Levensduur', text='Uren Gebruikt')
        self.history_tree.heading('Reden', text='Vervangreden')
        
        self.history_tree.column('Datum', width=100)
        self.history_tree.column('Type', width=120)
        self.history_tree.column('Levensduur', width=100)
        self.history_tree.column('Reden', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            history_frame,
            orient='vertical',
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10, padx=(0, 10))
        
        # Actie knoppen
        button_frame = tk.Frame(history_frame, bg=self.colors['white'])
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.replace_btn = tk.Button(
            button_frame,
            text="🔄 Nozzle Vervangen",
            command=self.replace_nozzle,
            font=("Arial", 10, "bold"),
            bg=self.colors['primary'],
            fg='white',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.replace_btn.pack(side='left', padx=(0, 10))
        
        self.reset_btn = tk.Button(
            button_frame,
            text="📊 Toon Statistieken",
            command=self.show_statistics,
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.reset_btn.pack(side='left')
        
    def analyze(self) -> Dict[str, Any]:
        """Analyseer nozzle status en genereer waarschuwingen."""
        df = self.load_data()
        
        # Update accumulated hours sinds laatste reset
        if not df.empty:
            # Filter data sinds installatie
            install_date = datetime.fromisoformat(
                self.maintenance_data['current_nozzle']['install_date']
            )
            
            recent_df = df[df['timestamp'] >= install_date]
            
            # Bereken nieuwe abrasieve uren
            if 'abrasive' in recent_df.columns:
                abrasive_df = recent_df[recent_df['abrasive'] == True]
                if 'print_hours' in abrasive_df.columns:
                    new_hours = abrasive_df['print_hours'].sum()
                else:
                    new_hours = abrasive_df['weight'].sum() / 20.0  # Estimate
                    
                # Update material history
                for material in abrasive_df['material'].unique():
                    if material not in self.maintenance_data['current_nozzle']['material_history']:
                        self.maintenance_data['current_nozzle']['material_history'][material] = 0
                    
                    # Bepaal uren voor dit materiaal
                    material_df = abrasive_df[abrasive_df['material'] == material]
                    if 'print_hours' in material_df.columns:
                        material_hours = material_df['print_hours'].sum()
                    else:
                        material_hours = material_df['weight'].sum() / 20.0
                        
                    self.maintenance_data['current_nozzle']['material_history'][material] = material_hours
            else:
                new_hours = 0
                
            self.maintenance_data['current_nozzle']['accumulated_hours'] = new_hours
            self.save_maintenance_data()
        
        # Bereken wear percentage
        nozzle_type = self.maintenance_data['current_nozzle']['type']
        max_lifetime = self.NOZZLE_LIFETIMES.get(nozzle_type, 250)
        accumulated = self.maintenance_data['current_nozzle']['accumulated_hours']
        wear_percentage = (accumulated / max_lifetime) * 100
        
        # Genereer waarschuwingen
        warnings = []
        for level, config in self.WARNING_LEVELS.items():
            if wear_percentage >= config['threshold']:
                warnings.append({
                    'level': level,
                    'threshold': config['threshold'],
                    'color': config['color'],
                    'icon': config['icon'],
                    'message': self._generate_warning_message(level, wear_percentage)
                })
                
        # Genereer recommendations
        recommendations = self._generate_recommendations(
            wear_percentage, 
            nozzle_type,
            self.maintenance_data['current_nozzle']['material_history']
        )
        
        return {
            'wear_percentage': wear_percentage,
            'accumulated_hours': accumulated,
            'max_lifetime': max_lifetime,
            'remaining_hours': max(0, max_lifetime - accumulated),
            'warnings': warnings,
            'recommendations': recommendations,
            'nozzle_type': nozzle_type
        }
        
    def _generate_warning_message(self, level: str, percentage: float) -> str:
        """Genereer waarschuwing bericht op basis van level."""
        messages = {
            'low': f"Nozzle is {percentage:.0f}% versleten - Plan vervanging in",
            'medium': f"Nozzle nadert einde levensduur ({percentage:.0f}%) - Bestel nieuwe",
            'high': f"Dringende vervanging nodig! {percentage:.0f}% versleten",
            'critical': f"KRITIEK: Nozzle over limiet ({percentage:.0f}%) - Vervang NU!"
        }
        return messages.get(level, f"Nozzle {percentage:.0f}% versleten")
        
    def _generate_recommendations(self, wear_pct: float, current_type: str, 
                                 material_history: Dict[str, float]) -> List[str]:
        """Genereer slimme aanbevelingen."""
        recommendations = []
        
        # Basis aanbeveling op wear percentage
        if wear_pct >= 80:
            recommendations.append(
                f"⚡ Bestel nieuwe {current_type} nozzle - levertijd 2-3 dagen"
            )
        elif wear_pct >= 60:
            recommendations.append(
                f"📅 Plan nozzle vervanging binnen 2 weken"
            )
            
        # Analyse meest gebruikte materialen
        if material_history:
            top_material = max(material_history.items(), key=lambda x: x[1])
            material_name, hours = top_material
            
            # Kijk of huidige nozzle optimaal is
            props = get_material_properties(material_name)
            if props:
                recommended = props.recommended_nozzle
                if recommended != current_type:
                    recommendations.append(
                        f"💡 Overweeg upgrade naar {recommended} "
                        f"(optimaal voor {material_name})"
                    )
                    
        # Cost-benefit voor premium nozzles
        if current_type in ['Brass 0.4mm', 'Hardened Steel'] and wear_pct >= 50:
            total_cf_hours = sum(
                hours for mat, hours in material_history.items() 
                if '-CF' in mat or '-GF' in mat
            )
            if total_cf_hours > 50:
                recommendations.append(
                    "💰 Ruby nozzle kan kosteneffectief zijn bij "
                    "regelmatig CF/GF gebruik (6x langere levensduur)"
                )
                
        return recommendations
        
    def update_analysis(self) -> None:
        """Update de waarschuwing displays."""
        results = self.analyze()
        
        # Update status panel
        self.lifetime_progress['value'] = min(results['wear_percentage'], 100)
        self.lifetime_label.configure(text=f"{results['wear_percentage']:.0f}%")
        
        # Kleur codering voor percentage
        if results['wear_percentage'] >= 90:
            color = 'red'
        elif results['wear_percentage'] >= 80:
            color = 'orange'
        elif results['wear_percentage'] >= 60:
            color = '#FFA500'
        else:
            color = 'green'
        self.lifetime_label.configure(fg=color)
        
        # Update remaining time
        remaining_hours = results['remaining_hours']
        if remaining_hours > 100:
            remaining_text = f"{remaining_hours:.0f} uur"
        elif remaining_hours > 0:
            remaining_text = f"{remaining_hours:.1f} uur"
        else:
            remaining_text = "Vervangen nodig!"
        self.remaining_label.configure(text=remaining_text, fg=color)
        
        # Update waarschuwingen
        self._update_warnings_display(results['warnings'])
        
        # Update recommendations
        self.recommendations_text.configure(state='normal')
        self.recommendations_text.delete(1.0, tk.END)
        for rec in results['recommendations']:
            self.recommendations_text.insert(tk.END, f"{rec}\n\n")
        self.recommendations_text.configure(state='disabled')
        
        # Update history
        self._update_history_display()
        
    def _update_warnings_display(self, warnings: List[Dict]):
        """Update waarschuwingen display."""
        # Clear bestaande
        for widget in self.warnings_container.winfo_children():
            widget.destroy()
            
        if not warnings:
            tk.Label(
                self.warnings_container,
                text="✅ Geen actieve waarschuwingen",
                font=("Arial", 11),
                bg=self.colors['white'],
                fg='green'
            ).pack(pady=20)
        else:
            # Sorteer op severity
            warnings.sort(key=lambda x: x['threshold'], reverse=True)
            
            for warning in warnings:
                warning_frame = tk.Frame(
                    self.warnings_container,
                    bg=self.colors['white'],
                    relief=tk.RIDGE,
                    bd=1
                )
                warning_frame.pack(fill='x', pady=5)
                
                tk.Label(
                    warning_frame,
                    text=f"{warning['icon']} {warning['message']}",
                    font=("Arial", 10, "bold"),
                    bg=self.colors['white'],
                    fg=warning['color'],
                    wraplength=250,
                    justify='left'
                ).pack(padx=10, pady=5)
                
    def _update_history_display(self):
        """Update maintenance history display."""
        # Clear bestaande items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Voeg history items toe
        for entry in self.maintenance_data.get('history', [])[-10:]:  # Laatste 10
            self.history_tree.insert('', 'end', values=(
                entry.get('date', 'Unknown'),
                entry.get('type', 'Unknown'),
                f"{entry.get('hours_used', 0):.1f}",
                entry.get('reason', 'Manual')
            ))
            
    def replace_nozzle(self):
        """Handle nozzle vervanging."""
        # Vraag om bevestiging en nieuwe nozzle type
        dialog = NozzleReplacementDialog(self.main_frame, self.maintenance_data)
        if dialog.result:
            # Sla huidige nozzle op in history
            current = self.maintenance_data['current_nozzle']
            self.maintenance_data['history'].append({
                'date': datetime.now().strftime("%d-%m-%Y"),
                'type': current['type'],
                'hours_used': current['accumulated_hours'],
                'reason': dialog.result['reason'],
                'material_history': current['material_history']
            })
            
            # Reset voor nieuwe nozzle
            self.maintenance_data['current_nozzle'] = {
                'type': dialog.result['new_type'],
                'install_date': datetime.now().isoformat(),
                'accumulated_hours': 0,
                'material_history': {}
            }
            
            self.save_maintenance_data()
            self.update_analysis()
            
            messagebox.showinfo(
                "Nozzle Vervangen",
                f"✅ Nieuwe {dialog.result['new_type']} nozzle geregistreerd!\n\n"
                f"De teller is gereset en nieuwe tracking is gestart."
            )
            
    def show_statistics(self):
        """Toon gedetailleerde statistieken."""
        stats_window = tk.Toplevel(self.main_frame)
        stats_window.title("Nozzle Statistieken")
        stats_window.geometry("600x400")
        
        # Bereken statistieken
        total_replacements = len(self.maintenance_data.get('history', []))
        total_hours = sum(entry.get('hours_used', 0) for entry in self.maintenance_data.get('history', []))
        
        if total_replacements > 0:
            avg_lifetime = total_hours / total_replacements
        else:
            avg_lifetime = 0
            
        # Toon statistieken
        stats_text = tk.Text(stats_window, wrap=tk.WORD, font=("Arial", 10))
        stats_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        stats_text.insert(tk.END, "📊 NOZZLE ONDERHOUD STATISTIEKEN\n\n", 'title')
        stats_text.insert(tk.END, f"Totaal vervangingen: {total_replacements}\n")
        stats_text.insert(tk.END, f"Totale abrasieve uren: {total_hours:.1f}\n")
        stats_text.insert(tk.END, f"Gemiddelde levensduur: {avg_lifetime:.1f} uur\n\n")
        
        # Kosten analyse
        stats_text.insert(tk.END, "💰 KOSTEN ANALYSE\n\n", 'title')
        for entry in self.maintenance_data.get('history', [])[-5:]:
            nozzle_cost = self._get_nozzle_cost(entry.get('type', 'Unknown'))
            stats_text.insert(tk.END, 
                f"{entry.get('date', 'Unknown')}: {entry.get('type', 'Unknown')} "
                f"- €{nozzle_cost:.2f} ({entry.get('hours_used', 0):.1f} uur)\n"
            )
            
        stats_text.tag_configure('title', font=("Arial", 12, "bold"))
        stats_text.configure(state='disabled')
        
    def _get_nozzle_cost(self, nozzle_type: str) -> float:
        """Krijg geschatte kosten voor nozzle type."""
        costs = {
            'Brass 0.4mm': 8.0,
            'Brass 0.6mm': 8.0,
            'Hardened 0.4mm': 25.0,
            'Hardened 0.6mm': 25.0,
            'Hardened Steel': 30.0,
            'Ruby Nozzle': 90.0,
            'Tungsten Carbide': 60.0
        }
        return costs.get(nozzle_type, 25.0)
        
    def _show_info_dialog(self):
        """Toon uitleg over de Maintenance Waarschuwingen."""
        info_window = tk.Toplevel(self.main_frame)
        info_window.title("Info - Maintenance Waarschuwingen")
        info_window.geometry("650x600")
        info_window.configure(bg='white')
        
        # Center het venster
        info_window.update_idletasks()
        x = (info_window.winfo_screenwidth() // 2) - (650 // 2)
        y = (info_window.winfo_screenheight() // 2) - (600 // 2)
        info_window.geometry(f"+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(info_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📚 Uitleg: Maintenance Waarschuwingen",
            font=("Arial", 16, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(expand=True)
        
        # Content
        content_frame = tk.Frame(info_window, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        info_text = """
⚠️ WAT DOET DEZE MODULE?

Deze module houdt de status van je HUIDIGE nozzle bij en waarschuwt je 
wanneer vervanging nodig is. Het werkt als een kilometerstand voor je nozzle.

📊 WAT BETEKENEN DE GETALLEN?

• Type: Het type nozzle dat nu geïnstalleerd is
• Levensduur %: Hoeveel van de nozzle al versleten is
• Resterend: Geschatte resterende print uren

⚡ VERSCHIL MET ABRASIEVE UREN TAB:

• Abrasieve Uren tab: Toont TOTALE HISTORIE (alle CF/GF ooit)
• Deze tab: Toont alleen HUIDIGE NOZZLE (sinds laatste reset)

Voorbeeld uit jouw screenshot:
- Je hebt TOTAAL 506 uren abrasief geprint
- Je HUIDIGE nozzle is 76% versleten (±190 uur gebruikt)
- Dit betekent dat je al ~2x een nozzle vervangen hebt

🔄 HOE WERKT HET?

1. Bij elke print met CF/GF materiaal telt het systeem de uren
2. Als je de nozzle vervangt, klik je op "Nozzle Vervangen"
3. Het systeem reset dan naar 0% voor de nieuwe nozzle
4. De historie wordt bewaard voor analyse

💡 WAARSCHUWING NIVEAUS:

• 🟢 0-60%: Alles OK
• 🟡 60-80%: Plan vervanging
• 🟠 80-90%: Bestel nieuwe nozzle
• 🔴 90-100%: Dringend vervangen!

📝 AANBEVELINGEN:

Het systeem geeft slimme tips op basis van:
- Je meest gebruikte materialen
- Cost-benefit van verschillende nozzle types
- Je print frequentie
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
            text="📊 Visuele Uitleg: Relatie tussen Maintenance & Abrasieve Uren",
            font=("Arial", 16, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(expand=True)
        
        # Canvas voor diagram
        canvas = tk.Canvas(diagram_window, width=760, height=500, bg='white', highlightthickness=0)
        canvas.pack(pady=20)
        
        # Haal huidige data op voor actuele getallen
        results = self.analyze()
        total_hours = results['accumulated_hours'] + (results['max_lifetime'] * len(self.maintenance_data.get('history', [])))
        current_percent = results['wear_percentage']
        current_hours = results['accumulated_hours']
        
        # Teken het diagram met actuele data
        self._draw_relationship_diagram(canvas, total_hours, current_percent, current_hours)
        
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
        
    def _draw_relationship_diagram(self, canvas, total_hours, current_percent, current_hours):
        """Teken het relatie diagram op de canvas met actuele data."""
        # Kleuren
        color_current = '#FFF3E0'  # Licht oranje
        color_total = '#E8F5E9'  # Licht groen
        color_relation = '#E3F2FD'  # Licht blauw
        
        # Titel
        canvas.create_text(380, 20, text="Hoe verhouden de twee modules zich tot elkaar?", 
                          font=("Arial", 14, "bold"), fill='#212121')
        
        # Box 1: Maintenance (Boven, prominent)
        canvas.create_rectangle(230, 60, 530, 190, fill=color_current, outline='#FF9800', width=3)
        canvas.create_text(380, 80, text="⚠️ DEZE TAB: MAINTENANCE", font=("Arial", 14, "bold"), fill='#E65100')
        canvas.create_text(380, 105, text="Huidige Nozzle Status", font=("Arial", 11, "italic"), fill='#F57C00')
        canvas.create_text(380, 140, text=f"{current_percent:.0f}% versleten", font=("Arial", 20, "bold"), fill='#E65100')
        canvas.create_text(380, 165, text=f"({current_hours:.0f} van 250 uur)", font=("Arial", 10), fill='#F57C00')
        
        # Pijl naar beneden
        canvas.create_line(380, 190, 380, 230, arrow=tk.LAST, width=3, fill='#FF9800')
        canvas.create_text(395, 210, text="reset bij vervanging", font=("Arial", 8, "italic"), fill='#666666')
        
        # Box 2: Abrasieve Uren (Onder)
        canvas.create_rectangle(30, 240, 330, 340, fill=color_total, outline='#4CAF50', width=2)
        canvas.create_text(180, 260, text="🔧 ABRASIEVE UREN TAB", font=("Arial", 12, "bold"), fill='#2E7D32')
        canvas.create_text(180, 285, text="Historisch Totaal", font=("Arial", 10, "italic"), fill='#388E3C')
        canvas.create_text(180, 310, text=f"{total_hours:.0f} totale uren", font=("Arial", 16, "bold"), fill='#1B5E20')
        canvas.create_text(180, 325, text="(blijft optellen)", font=("Arial", 9), fill='#2E7D32')
        
        # History Box
        canvas.create_rectangle(430, 240, 730, 340, fill='#F5F5F5', outline='#9E9E9E', width=1)
        canvas.create_text(580, 260, text="📜 VERVANGINGS HISTORIE", font=("Arial", 12, "bold"), fill='#424242')
        history_count = len(self.maintenance_data.get('history', []))
        canvas.create_text(580, 290, text=f"{history_count} keer vervangen", font=("Arial", 14), fill='#212121')
        canvas.create_text(580, 310, text=f"= {history_count * 250} uur afgeschreven", font=("Arial", 10), fill='#616161')
        canvas.create_text(580, 325, text=f"+ {current_hours:.0f} uur huidige nozzle", font=("Arial", 10), fill='#616161')
        
        # Verbinding lijnen
        canvas.create_line(330, 290, 430, 290, width=2, fill='#757575', dash=(5, 5))
        
        # Relatie box (Onderaan)
        canvas.create_rectangle(150, 360, 610, 440, fill=color_relation, outline='#2196F3', width=3)
        canvas.create_text(380, 380, text="🔗 DE RELATIE", font=("Arial", 14, "bold"), fill='#0D47A1')
        canvas.create_text(380, 405, text=f"Totaal ({total_hours:.0f}u) = Vervangen ({history_count}×250u) + Huidig ({current_hours:.0f}u)", 
                          font=("Arial", 11), fill='#1565C0')
        canvas.create_text(380, 425, text="Deze tab reset bij elke vervanging, de andere telt door", 
                          font=("Arial", 10, "italic"), fill='#1976D2')
        
        # Educatieve tip
        canvas.create_text(380, 470, text="💡 TIP: Bij 80% krijg je een waarschuwing. Bij 100% is vervanging echt nodig!", 
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


class NozzleReplacementDialog:
    """Dialog voor nozzle vervanging."""
    
    def __init__(self, parent, maintenance_data):
        self.result = None
        
        # Maak dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nozzle Vervangen")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Content
        tk.Label(
            self.dialog,
            text="🔧 Nozzle Vervanging Registreren",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Nieuwe nozzle type
        tk.Label(
            self.dialog,
            text="Nieuwe nozzle type:",
            font=("Arial", 10)
        ).pack(pady=(10, 5))
        
        self.type_var = tk.StringVar(value=maintenance_data['current_nozzle']['type'])
        type_combo = ttk.Combobox(
            self.dialog,
            textvariable=self.type_var,
            values=list(MaintenanceWarningSystem.NOZZLE_LIFETIMES.keys()),
            state='readonly',
            width=25
        )
        type_combo.pack()
        
        # Reden voor vervanging
        tk.Label(
            self.dialog,
            text="Reden voor vervanging:",
            font=("Arial", 10)
        ).pack(pady=(20, 5))
        
        self.reason_var = tk.StringVar(value="Preventief onderhoud")
        reasons = [
            "Preventief onderhoud",
            "Verstopping",
            "Slijtage",
            "Beschadiging",
            "Upgrade",
            "Anders"
        ]
        
        reason_combo = ttk.Combobox(
            self.dialog,
            textvariable=self.reason_var,
            values=reasons,
            width=25
        )
        reason_combo.pack()
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=30)
        
        tk.Button(
            button_frame,
            text="✅ Bevestigen",
            command=self.confirm,
            bg='#00A86B',
            fg='white',
            padx=20,
            pady=5
        ).pack(side='left', padx=10)
        
        tk.Button(
            button_frame,
            text="❌ Annuleren",
            command=self.cancel,
            bg='#DC143C',
            fg='white',
            padx=20,
            pady=5
        ).pack(side='left')
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f'+{x}+{y}')
        
    def confirm(self):
        """Bevestig vervanging."""
        self.result = {
            'new_type': self.type_var.get(),
            'reason': self.reason_var.get()
        }
        self.dialog.destroy()
        
    def cancel(self):
        """Annuleer vervanging."""
        self.dialog.destroy() 