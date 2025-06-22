"""
Analytics GUI Module - H2D Price Calculator
==========================================

Deze module beheert de analytics interface en laadt
alle analyse modules dynamisch.

REDESIGNED: Professionele dashboard layout met sidebar navigatie
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys


class AnalyticsGUI(tk.Frame):
    """Hoofd analytics GUI controller met moderne dashboard layout."""
    
    def __init__(self, parent, data_manager, colors):
        """Initialiseer Analytics GUI."""
        super().__init__(parent, bg=colors['bg'])
        self.data_manager = data_manager
        self.colors = colors
        self.analyses = {}
        self.current_frame = None
        self.sidebar_buttons = {}
        
        # Update kleuren voor professionele look
        self.dashboard_colors = {
            'sidebar_bg': '#2C3E50',  # Donker blauw-grijs
            'sidebar_hover': '#34495E',  # Iets lichter voor hover
            'sidebar_active': '#3498DB',  # Helder blauw voor actief
            'header_bg': '#ECF0F1',  # Licht grijs
            'content_bg': '#FFFFFF',  # Wit
            'text_light': '#FFFFFF',  # Witte tekst voor sidebar
            'text_dark': '#2C3E50',  # Donkere tekst voor content
        }
        
        # Check modules
        self._check_analytics_module()
        
        # Creëer professionele layout
        self.create_professional_layout()
        
    def _check_analytics_module(self):
        """Check of analytics module correct is geïnstalleerd."""
        try:
            import pandas
            import matplotlib
            import numpy
        except ImportError as e:
            missing = str(e).split("'")[1]
            messagebox.showwarning(
                "Module Vereist",
                f"De analytics module vereist {missing}.\n\n"
                f"Installeer met: pip install {missing}"
            )
    
    def create_professional_layout(self):
        """Creëer moderne dashboard layout met sidebar."""
        # Main container met grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar (Links)
        self.create_sidebar()
        
        # Main content area (Rechts)
        self.content_area = tk.Frame(self, bg=self.dashboard_colors['content_bg'])
        self.content_area.grid(row=0, column=1, sticky='nsew')
        
        # Header in content area
        self.create_header()
        
        # Content frame waar analyses geladen worden
        self.content_frame = tk.Frame(self.content_area, bg=self.dashboard_colors['content_bg'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Laad eerste analyse standaard
        self.show_basis_stats()
    
    def create_sidebar(self):
        """Creëer professionele sidebar navigatie."""
        # Sidebar frame
        sidebar = tk.Frame(self, bg=self.dashboard_colors['sidebar_bg'], width=250)
        sidebar.grid(row=0, column=0, sticky='nsew')
        sidebar.grid_propagate(False)
        
        # Logo/Titel sectie
        logo_frame = tk.Frame(sidebar, bg=self.dashboard_colors['sidebar_bg'], height=80)
        logo_frame.pack(fill='x', padx=20, pady=20)
        logo_frame.pack_propagate(False)
        
        tk.Label(
            logo_frame,
            text="📊 Analytics",
            font=("Arial", 24, "bold"),
            bg=self.dashboard_colors['sidebar_bg'],
            fg=self.dashboard_colors['text_light']
        ).pack(expand=True)
        
        # Separator
        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', padx=20)
        
        # Menu items
        menu_items = [
            ("📈 Basis Statistieken", self.show_basis_stats),
            ("🔧 Slijtage & Onderhoud", self.show_slijtage),
            ("💰 Kosten Analyse", self.show_kosten),
            ("🎯 Business Insights", self.show_business)
        ]
        
        # Creëer menu buttons
        for text, command in menu_items:
            btn = self.create_sidebar_button(sidebar, text, command)
            self.sidebar_buttons[text] = btn
        
        # Info sectie onderaan
        info_frame = tk.Frame(sidebar, bg=self.dashboard_colors['sidebar_bg'])
        info_frame.pack(side='bottom', fill='x', padx=20, pady=20)
        
        tk.Label(
            info_frame,
            text="Data bron:",
            font=("Arial", 9),
            bg=self.dashboard_colors['sidebar_bg'],
            fg='#95A5A6'
        ).pack(anchor='w')
        
        tk.Label(
            info_frame,
                            text="producten/master_calculations.csv",
            font=("Arial", 10, "bold"),
            bg=self.dashboard_colors['sidebar_bg'],
            fg=self.dashboard_colors['text_light'],
            wraplength=200
        ).pack(anchor='w')
        
        # Extra info
        tk.Label(
            info_frame,
            text="✓ Correcte data bron",
            font=("Arial", 8),
            bg=self.dashboard_colors['sidebar_bg'],
            fg='#27AE60'
        ).pack(anchor='w', pady=(5, 0))
        
    def create_sidebar_button(self, parent, text, command):
        """Creëer een sidebar menu button met hover effect."""
        btn_frame = tk.Frame(parent, bg=self.dashboard_colors['sidebar_bg'])
        btn_frame.pack(fill='x', padx=10, pady=2)
        
        btn = tk.Label(
            btn_frame,
            text=text,
            font=("Arial", 12),
            bg=self.dashboard_colors['sidebar_bg'],
            fg=self.dashboard_colors['text_light'],
            padx=20,
            pady=15,
            anchor='w',
            cursor='hand2'
        )
        btn.pack(fill='x')
        
        # Bind events voor hover en click
        btn.bind("<Enter>", lambda e: self.on_btn_hover(btn, True))
        btn.bind("<Leave>", lambda e: self.on_btn_hover(btn, False))
        btn.bind("<Button-1>", lambda e: command())
        
        return btn
    
    def on_btn_hover(self, btn, hovering):
        """Handle button hover effect."""
        if btn['bg'] != self.dashboard_colors['sidebar_active']:  # Als niet actief
            btn['bg'] = self.dashboard_colors['sidebar_hover'] if hovering else self.dashboard_colors['sidebar_bg']
    
    def set_active_button(self, active_text):
        """Markeer actieve button in sidebar."""
        for text, btn in self.sidebar_buttons.items():
            if text == active_text:
                btn['bg'] = self.dashboard_colors['sidebar_active']
                btn['fg'] = self.dashboard_colors['text_light']
            else:
                btn['bg'] = self.dashboard_colors['sidebar_bg']
                btn['fg'] = self.dashboard_colors['text_light']
    
    def create_header(self):
        """Creëer professionele header in content area."""
        header_frame = tk.Frame(
            self.content_area, 
            bg=self.dashboard_colors['header_bg'],
            height=70
        )
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content container
        header_content = tk.Frame(header_frame, bg=self.dashboard_colors['header_bg'])
        header_content.pack(expand=True, fill='both', padx=30, pady=15)
        
        # Titel
        self.header_title = tk.Label(
            header_content,
            text="H2D Price Calculator - Analytics Dashboard",
            font=("Arial", 18, "bold"),
            bg=self.dashboard_colors['header_bg'],
            fg=self.dashboard_colors['text_dark']
        )
        self.header_title.pack(side='left')
        
        # Refresh button
        refresh_btn = tk.Button(
            header_content,
            text="🔄 Vernieuw Data",
            font=("Arial", 11),
            bg='#3498DB',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.refresh_current_view
        )
        refresh_btn.pack(side='right')
        
        # Separator
        separator = tk.Frame(self.content_area, bg='#BDC3C7', height=1)
        separator.pack(fill='x')
    
    def clear_content(self):
        """Clear huidige content frame."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.content_frame, bg=self.dashboard_colors['content_bg'])
        self.current_frame.pack(fill='both', expand=True)
    
    def show_basis_stats(self):
        """Toon basis statistieken."""
        self.clear_content()
        self.set_active_button("📈 Basis Statistieken")
        self.header_title.config(text="Basis Statistieken - Overzicht")
        
        try:
            # Laad basis modules
            from src.analytics.basis.dagelijkse_activiteit import DagelijkseActiviteit
            from src.analytics.basis.materiaal_gebruik import MateriaalGebruik
            from src.analytics.basis.print_waardes import PrintWaardes
            
            # Creëer sub-tabs
            self._create_analysis_tabs(self.current_frame, [
                ("📅 Dagelijkse Activiteit", DagelijkseActiviteit),
                ("🎨 Materiaal Gebruik", MateriaalGebruik),
                ("📊 Print Waardes", PrintWaardes)
            ])
        except ImportError as e:
            self._show_module_error(self.current_frame, "Basis Statistieken", str(e))
    
    def show_slijtage(self):
        """Toon slijtage analyses."""
        self.clear_content()
        self.set_active_button("🔧 Slijtage & Onderhoud")
        self.header_title.config(text="Slijtage & Onderhoud - Tracking")
        
        try:
            # Import alle slijtage modules
            from ..analytics.slijtage import (
                AbrasiveTeller,
                MaintenanceWarningSystem,
                SlijtageGrafiek
            )
            
            # Als productie_teller bestaat, voeg die ook toe
            modules_list = []
            try:
                from ..analytics.slijtage.productie_teller import ProductieSlijtageTeller
                modules_list.append(("📈 Productie Teller", ProductieSlijtageTeller))
            except ImportError:
                pass
            
            # Voeg onze nieuwe modules toe
            modules_list.extend([
                ("🔧 Abrasieve Uren", AbrasiveTeller),
                ("⚠️ Maintenance", MaintenanceWarningSystem),
                ("📊 Grafieken", SlijtageGrafiek)
            ])
            
            # Creëer tabs voor alle modules
            self._create_analysis_tabs(self.current_frame, modules_list)
            
        except Exception as e:
            self._show_module_error(self.current_frame, "Slijtage Module", str(e))
    
    def show_kosten(self):
        """Toon kosten analyses."""
        self.clear_content()
        self.set_active_button("💰 Kosten Analyse")
        self.header_title.config(text="Kosten Analyse - Winstgevendheid")
        
        self._show_coming_soon(self.current_frame, "Kosten Analyse", [
            "📈 Marge trends over tijd",
            "💸 Kosten breakdown per product",
            "🏷️ Pricing optimalisatie"
        ])
    
    def show_business(self):
        """Toon business insights."""
        self.clear_content()
        self.set_active_button("🎯 Business Insights")
        self.header_title.config(text="Business Insights - Strategisch Overzicht")
        
        self._show_coming_soon(self.current_frame, "Business Insights", [
            "🔥 Populaire product configuraties",
            "⚡ Rush vs normale orders",
            "📏 Size impact analyse"
        ])
    
    def _create_analysis_tabs(self, parent, modules):
        """Creëer tabs voor analyse modules met moderne styling."""
        # Tab styling
        style = ttk.Style()
        style.configure('Modern.TNotebook', background=self.dashboard_colors['content_bg'])
        style.configure('Modern.TNotebook.Tab', 
                       padding=[30, 15], 
                       font=('Arial', 11),
                       background='#ECF0F1')
        
        notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        notebook.pack(fill='both', expand=True)
        
        for name, module_class in modules:
            tab_frame = tk.Frame(notebook, bg=self.dashboard_colors['content_bg'])
            notebook.add(tab_frame, text=name)
            
            try:
                module = module_class(
                    data_manager=self.data_manager,
                    parent_frame=tab_frame,
                    colors=self.colors
                )
                module.create_widgets(tab_frame)
            except Exception as e:
                self._show_module_error(tab_frame, name, str(e))
    
    def _show_coming_soon(self, parent, title, features):
        """Toon coming soon bericht met moderne styling."""
        # Container
        container = tk.Frame(parent, bg='#F8F9FA', relief=tk.FLAT, bd=0)
        container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Icon en titel
        tk.Label(
            container,
            text="🚧",
            font=("Arial", 48),
            bg='#F8F9FA'
        ).pack(pady=(20, 10))
        
        tk.Label(
            container,
            text=f"{title} - Binnenkort Beschikbaar",
            font=("Arial", 20, "bold"),
            bg='#F8F9FA',
            fg='#2C3E50'
        ).pack(pady=(0, 20))
        
        # Features
        features_frame = tk.Frame(container, bg='#FFFFFF', relief=tk.RIDGE, bd=1)
        features_frame.pack(pady=20)
        
        for feature in features:
            tk.Label(
                features_frame,
                text=f"  • {feature}",
                font=("Arial", 12),
                bg='#FFFFFF',
                fg='#34495E',
                anchor='w'
            ).pack(fill='x', padx=30, pady=10)
    
    def _show_module_error(self, parent, module_name, error):
        """Toon error met moderne styling."""
        error_frame = tk.Frame(parent, bg='#FFE5E5', relief=tk.FLAT, bd=0)
        error_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        tk.Label(
            error_frame,
            text="⚠️",
            font=("Arial", 48),
            bg='#FFE5E5',
            fg='#E74C3C'
        ).pack(pady=20)
        
        tk.Label(
            error_frame,
            text=f"Fout bij laden {module_name}",
            font=("Arial", 16, "bold"),
            bg='#FFE5E5',
            fg='#C0392B'
        ).pack()
        
        tk.Label(
            error_frame,
            text=str(error),
            font=("Arial", 11),
            bg='#FFE5E5',
            fg='#7F1E1E',
            wraplength=400
        ).pack(pady=10)
    
    def refresh_current_view(self):
        """Vernieuw huidige weergave."""
        # Simpele implementatie - herlaad huidige view
        # Dit kan uitgebreid worden per module
        pass 