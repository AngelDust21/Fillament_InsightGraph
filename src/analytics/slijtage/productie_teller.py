"""
Productie Slijtage Teller - H2D Price Calculator
===============================================

Deze module berekent realistische slijtage kosten op basis van:
- Aantal te produceren stuks per product
- Materiaal specifieke slijtage factoren
- Werkelijke printsnelheden per materiaal

EDUCATIEF DOEL:
--------------
Toont het verschil tussen:
- 1x 100g PETG-CF printen: €0.45 slijtage
- 100x 100g PETG-CF printen: €45.00 slijtage (!!)

Dit leert studenten om productie volumes mee te nemen
in hun prijsberekeningen.
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import os

from ..base_analysis import BaseAnalysis
from ...materials.material_properties import (
    get_material_properties,
    calculate_print_time,
    calculate_wear_cost
)


class ProductieSlijtageTeller(BaseAnalysis):
    """Berekent slijtage voor productie runs.
    
    Verschil met simpele teller:
    - Vraagt om productie aantallen
    - Berekent totale slijtage voor hele run
    - Toont impact op prijs per stuk
    """
    
    def get_title(self) -> str:
        """Return titel voor deze analyse."""
        return "🏭 Productie Slijtage Calculator"
        
    def create_analysis_widgets(self) -> None:
        """Creëer de productie interface."""
        df = self.load_data()
        if df.empty:
            self.show_no_data_message()
            return
            
        # === INVOER SECTIE ===
        self._create_input_section()
        
        # === RESULTATEN SECTIE ===
        self._create_results_section()
        
        # === PRODUCTIE TABEL ===
        self._create_production_table()
        
    def _create_input_section(self) -> None:
        """Maak invoer sectie voor productie planning."""
        input_frame = tk.LabelFrame(
            self.main_frame,
            text="📝 Productie Planning",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Product selectie
        row1 = tk.Frame(input_frame, bg=self.colors['white'])
        row1.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            row1,
            text="Product:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).pack(side='left', padx=(0, 5))
        
        # Laad unieke producten
        df = self.load_data()
        products = df[df['is_product'] == True]['product_name'].dropna().unique()
        
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(
            row1,
            textvariable=self.product_var,
            values=list(products),
            width=30,
            state='readonly'
        )
        self.product_combo.pack(side='left', padx=5)
        self.product_combo.bind('<<ComboboxSelected>>', self._on_product_select)
        
        # Aantal stuks
        tk.Label(
            row1,
            text="Aantal stuks:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).pack(side='left', padx=(20, 5))
        
        self.quantity_var = tk.StringVar(value="10")
        quantity_entry = tk.Entry(
            row1,
            textvariable=self.quantity_var,
            width=10,
            font=("Arial", 10)
        )
        quantity_entry.pack(side='left', padx=5)
        
        # Bereken knop
        calc_btn = tk.Button(
            row1,
            text="Bereken Slijtage",
            command=self._calculate_production,
            bg=self.colors['primary'],
            fg='white',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        calc_btn.pack(side='left', padx=20)
        
        # Product info
        self.info_label = tk.Label(
            input_frame,
            text="Selecteer een product om details te zien",
            font=("Arial", 9),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        self.info_label.pack(anchor='w', padx=10, pady=(0, 5))
        
    def _create_results_section(self) -> None:
        """Maak resultaten display."""
        results_frame = tk.LabelFrame(
            self.main_frame,
            text="📊 Slijtage Berekening",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        results_frame.pack(fill='x', pady=(0, 10))
        
        # Grid voor resultaten
        grid = tk.Frame(results_frame, bg=self.colors['white'])
        grid.pack(padx=20, pady=10)
        
        # Labels voor resultaten
        self.result_labels = {}
        
        rows = [
            ("per_stuk", "Slijtage per stuk:"),
            ("totaal", "Totale slijtage:"),
            ("nozzle_life", "Nozzle levensduur:"),
            ("advies", "Advies:")
        ]
        
        for i, (key, text) in enumerate(rows):
            tk.Label(
                grid,
                text=text,
                font=("Arial", 10, "bold"),
                bg=self.colors['white']
            ).grid(row=i, column=0, sticky='e', padx=(0, 10), pady=3)
            
            label = tk.Label(
                grid,
                text="-",
                font=("Arial", 10),
                bg=self.colors['white']
            )
            label.grid(row=i, column=1, sticky='w', pady=3)
            self.result_labels[key] = label
            
    def _create_production_table(self) -> None:
        """Maak tabel voor meerdere producten."""
        table_frame = tk.LabelFrame(
            self.main_frame,
            text="📋 Productie Overzicht",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        table_frame.pack(fill='both', expand=True)
        
        # Treeview voor productie lijst
        columns = ('Product', 'Materiaal', 'Aantal', 'Uren/stuk', 'Slijtage/stuk', 'Totaal')
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=8
        )
        
        # Kolom configuratie
        widths = [150, 100, 60, 80, 90, 80]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Totalen onderaan
        totals_frame = tk.Frame(table_frame, bg=self.colors['white'])
        totals_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.totals_label = tk.Label(
            totals_frame,
            text="Totale productie slijtage: € 0.00",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['secondary']
        )
        self.totals_label.pack(side='right')
        
    def _on_product_select(self, event=None) -> None:
        """Update info bij product selectie."""
        product = self.product_var.get()
        if not product:
            return
            
        df = self.load_data()
        product_data = df[df['product_name'] == product].iloc[-1]  # Laatste versie
        
        info = (f"Materiaal: {product_data['material']} | "
                f"Gewicht: {product_data['weight']:.0f}g | "
                f"Laatste prijs: €{product_data['sell_price']:.2f}")
        
        self.info_label.configure(text=info)
        
    def _calculate_production(self) -> None:
        """Bereken slijtage voor productie run."""
        product = self.product_var.get()
        if not product:
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            self.result_labels['advies'].configure(
                text="Voer een geldig aantal in",
                fg='red'
            )
            return
            
        # Haal product data op
        df = self.load_data()
        product_data = df[df['product_name'] == product].iloc[-1]
        
        material = product_data['material']
        weight = product_data['weight']
        
        # Bereken met material properties
        props = get_material_properties(material)
        if not props:
            self.result_labels['advies'].configure(
                text="Geen material properties gevonden",
                fg='red'
            )
            return
            
        # Bereken per stuk
        print_time_per = calculate_print_time(material, weight)
        wear_cost_per = calculate_wear_cost(material, print_time_per)
        
        # Bereken totaal
        total_hours = print_time_per * quantity
        total_wear = wear_cost_per * quantity
        
        # Nozzle levensduur impact
        nozzle_life_hours = 1000.0 / props.nozzle_wear_factor
        life_used_pct = (total_hours / nozzle_life_hours) * 100
        
        # Update labels
        self.result_labels['per_stuk'].configure(
            text=f"€ {wear_cost_per:.3f}",
            fg=self.colors['text']
        )
        
        self.result_labels['totaal'].configure(
            text=f"€ {total_wear:.2f}",
            fg='red' if total_wear > 50 else self.colors['text']
        )
        
        self.result_labels['nozzle_life'].configure(
            text=f"{life_used_pct:.1f}% van {props.recommended_nozzle}",
            fg='red' if life_used_pct > 80 else self.colors['text']
        )
        
        # Advies
        if life_used_pct > 100:
            vervangingen = int(life_used_pct / 100)
            advies = f"⚠️ Vervang nozzle {vervangingen}x tijdens productie!"
            kleur = 'red'
        elif life_used_pct > 80:
            advies = "⚠️ Nozzle vervanging nodig na deze run"
            kleur = 'orange'
        elif props.nozzle_wear_factor > 5:
            advies = f"💡 Overweeg {props.recommended_nozzle} voor CF/GF"
            kleur = 'blue'
        else:
            advies = "✅ Acceptabele slijtage voor deze run"
            kleur = 'green'
            
        self.result_labels['advies'].configure(text=advies, fg=kleur)
        
        # Voeg toe aan tabel
        self._add_to_table(product, material, quantity, print_time_per, wear_cost_per, total_wear)
        
    def _add_to_table(self, product: str, material: str, quantity: int,
                     hours_per: float, wear_per: float, total: float) -> None:
        """Voeg productie run toe aan tabel."""
        # Voeg nieuwe rij toe
        values = (
            product,
            material,
            quantity,
            f"{hours_per:.2f}u",
            f"€{wear_per:.3f}",
            f"€{total:.2f}"
        )
        
        self.tree.insert('', 'end', values=values)
        
        # Update totaal
        total_sum = 0.0
        for item in self.tree.get_children():
            vals = self.tree.item(item)['values']
            total_str = vals[5].replace('€', '')
            total_sum += float(total_str)
            
        self.totals_label.configure(
            text=f"Totale productie slijtage: € {total_sum:.2f}"
        )
        
    def analyze(self) -> Dict[str, Any]:
        """Analyseer productie slijtage."""
        # Voor compatibility met base class
        return {"status": "manual_mode"}
        
    def update_analysis(self) -> None:
        """Update de analyse (refresh data)."""
        # Herlaad product lijst
        df = self.load_data()
        products = df[df['is_product'] == True]['product_name'].dropna().unique()
        self.product_combo['values'] = list(products) 