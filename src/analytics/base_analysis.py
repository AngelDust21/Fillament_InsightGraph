"""
Base Analysis Class - H2D Price Calculator
=========================================

Basis klasse voor alle analyse modules.
Biedt gemeenschappelijke functionaliteit voor:
- Data loading uit CSV
- GUI widget creatie
- Error handling
- Data caching
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
import time


class BaseAnalysis(ABC):
    """Abstract basis klasse voor alle analyses.
    
    Elke analyse module moet deze klasse extenden en de
    abstracte methoden implementeren.
    """
    
    def __init__(self, data_manager, parent_frame=None, colors=None):
        """Initialiseer basis analyse.
        
        Parameters:
        ----------
        data_manager : DataManager
            Instance voor data toegang
        parent_frame : tk.Frame, optional
            Parent frame voor GUI widgets
        colors : dict, optional
            Kleurenschema van hoofdGUI
        """
        self.data_manager = data_manager
        self.parent_frame = parent_frame
        self.colors = colors or self._default_colors()
        self._data_cache = None
        self._complete_data_cache = None
        self.cache_duration = 300  # 5 minuten cache
        self.widgets = {}
        
    def _default_colors(self) -> Dict[str, str]:
        """Default kleurenschema als geen colors zijn meegegeven."""
        return {
            'bg': '#f8f8f8',
            'primary': '#00A86B',
            'secondary': '#2E8B57',
            'accent': '#32CD32',
            'text': '#333333',
            'light_gray': '#e8e8e8',
            'white': '#ffffff'
        }
    
    def _is_cache_valid(self) -> bool:
        """Check of de data cache nog geldig is."""
        if self._data_cache is None:
            return False
        return (time.time() - self._data_cache['timestamp']) < self.cache_duration
    
    def _is_complete_cache_valid(self) -> bool:
        """Check of de complete data cache nog geldig is."""
        if self._complete_data_cache is None:
            return False
        return (time.time() - self._complete_data_cache['timestamp']) < self.cache_duration
    
    def _get_cache_age(self) -> float:
        """Krijg leeftijd van de cache in seconden."""
        if self._data_cache is None:
            return float('inf')
        return time.time() - self._data_cache['timestamp']
    
    def _get_complete_cache_age(self) -> float:
        """Krijg leeftijd van de complete cache in seconden."""
        if self._complete_data_cache is None:
            return float('inf')
        return time.time() - self._complete_data_cache['timestamp']
        
    def load_data(self) -> Optional[pd.DataFrame]:
        """Laad data uit master_calculations.csv met caching.
        
        Dit is de primaire methode voor de meeste analyses. Laadt een subset van kolommen
        die relevant zijn voor visualisaties.
        
        Returns:
        -------
        Optional[pd.DataFrame]
            DataFrame met data of None als laden mislukt
        """
        # Check cache eerst
        if self._is_cache_valid():
            print(f"Using cached data (age: {self._get_cache_age():.1f} seconds)")
            return self._data_cache['data'].copy()
        
        # Bepaal pad naar master_calculations.csv
        # Start vanaf de huidige file locatie
        current_file = os.path.abspath(__file__)
        
        # Ga naar de root van het project (waar exports folder is)
        # Van src/analytics/base_analysis.py naar root is 2 niveau's omhoog
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        
        # Pad naar master_calculations.csv
        log_path = os.path.join(project_root, 'exports', 'producten', 'master_calculations.csv')
        
        print(f"DEBUG: Project root: {project_root}")
        print(f"DEBUG: Looking for master_calculations.csv at: {log_path}")
        print(f"DEBUG: File exists: {os.path.exists(log_path)}")
        
        if os.path.exists(log_path):
            try:
                df = pd.read_csv(log_path)
                print(f"Loaded {len(df)} rows from master_calculations.csv")
                
                # Converteer timestamp naar datetime als die bestaat
                if 'timestamp' in df.columns:
                    # Gebruik format='mixed' om verschillende timestamp formaten te ondersteunen
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
                
                # Update cache
                self._data_cache = {
                    'data': df,
                    'timestamp': time.time()
                }
                
                return df.copy()
            except Exception as e:
                print(f"Error loading master_calculations.csv: {e}")
                return pd.DataFrame()  # Return lege DataFrame in plaats van None
        else:
            print(f"master_calculations.csv not found at: {log_path}")
            # Probeer het bestand te creëren als het niet bestaat
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            # Maak een lege CSV met de juiste headers
            empty_df = pd.DataFrame(columns=[
                'timestamp', 'weight', 'material', 'material_cost', 
                'variable_cost', 'total_cost', 'sell_price', 'margin_pct',
                'profit_amount', 'multicolor', 'abrasive', 'rush',
                'day_of_week', 'hour_of_day', 'month', 'year', 
                'product_name', 'product_id', 'is_product'
            ])
            empty_df.to_csv(log_path, index=False)
            print(f"Created empty master_calculations.csv at: {log_path}")
            return pd.DataFrame()  # Return lege DataFrame
        
    def load_complete_data(self) -> Optional[pd.DataFrame]:
        """Laad complete data uit calculation_log.csv.
        
        Deze methode laadt de volledige calculation_log.csv die alle 31 kolommen bevat,
        in tegenstelling tot master_calculations.csv die een subset is.
        
        Returns:
        -------
        Optional[pd.DataFrame]
            DataFrame met complete data of None als laden mislukt
        """
        # Check cache eerst
        if self._is_complete_cache_valid():
            print(f"Using cached complete data (age: {self._get_complete_cache_age():.1f} seconds)")
            return self._complete_data_cache['data'].copy()
        
        # Bepaal pad naar calculation_log.csv
        # Start vanaf de huidige file locatie
        current_file = os.path.abspath(__file__)
        
        # Ga naar de root van het project (waar exports folder is)
        # Van src/analytics/base_analysis.py naar root is 2 niveau's omhoog
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        
        # Pad naar calculation_log.csv
        log_path = os.path.join(project_root, 'exports', 'berekeningen', 'calculation_log.csv')
        
        print(f"DEBUG: Project root: {project_root}")
        print(f"DEBUG: Looking for calculation_log.csv at: {log_path}")
        print(f"DEBUG: File exists: {os.path.exists(log_path)}")
        
        if os.path.exists(log_path):
            try:
                df = pd.read_csv(log_path)
                
                # Converteer timestamp naar datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed')
                
                print(f"Loaded {len(df)} rows from calculation_log.csv with {len(df.columns)} columns")
                
                # Update cache
                self._complete_data_cache = {
                    'data': df,
                    'timestamp': time.time()
                }
                
                return df.copy()
            except Exception as e:
                print(f"Error loading calculation_log.csv: {e}")
                return pd.DataFrame()  # Return lege DataFrame in plaats van None
        else:
            print(f"calculation_log.csv not found at: {log_path}")
            return pd.DataFrame()  # Return lege DataFrame in plaats van None
        
    def create_widgets(self, parent: tk.Frame) -> None:
        """Creëer GUI widgets voor deze analyse.
        
        Parameters:
        ----------
        parent : tk.Frame
            Parent frame voor widgets
        """
        self.parent_frame = parent
        
        # Container frame
        self.main_frame = tk.Frame(parent, bg=self.colors['bg'])
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Titel
        self.create_title()
        
        # Analyse specifieke widgets
        self.create_analysis_widgets()
        
        # Refresh knop
        self.create_refresh_button()
        
    def create_title(self) -> None:
        """Creëer titel widget."""
        title_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        title_frame.pack(fill='x', pady=(0, 10))
        
        title = tk.Label(
            title_frame,
            text=self.get_title(),
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title.pack(side='left')
        
    def create_refresh_button(self) -> None:
        """Creëer refresh knop."""
        btn_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(10, 0))
        
        refresh_btn = tk.Button(
            btn_frame,
            text="🔄 Vernieuw Data",
            command=self.refresh_analysis,
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        refresh_btn.pack(side='right')
        
    def refresh_analysis(self) -> None:
        """Vernieuw de analyse met nieuwe data."""
        try:
            # Force reload data
            self.load_data()
            
            # Update visualisaties
            self.update_analysis()
            
            # Feedback
            if hasattr(self, 'status_label'):
                self.status_label.configure(text="✅ Data vernieuwd")
                
        except Exception as e:
            messagebox.showerror("Fout", f"Kon analyse niet vernieuwen:\n{str(e)}")
            
    def show_no_data_message(self) -> None:
        """Toon bericht als er geen data is."""
        msg_label = tk.Label(
            self.main_frame,
            text="📊 Geen data beschikbaar\n\nVoer eerst enkele berekeningen uit.",
            font=("Arial", 12),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='center'
        )
        msg_label.pack(pady=50)
        
    @abstractmethod
    def get_title(self) -> str:
        """Return titel voor deze analyse.
        
        Returns:
        -------
        str
            Titel string
        """
        pass
        
    @abstractmethod
    def create_analysis_widgets(self) -> None:
        """Creëer analyse-specifieke widgets.
        
        Moet geïmplementeerd worden door subklassen.
        """
        pass
        
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Voer de analyse uit.
        
        Returns:
        -------
        Dict[str, Any]
            Analyse resultaten
        """
        pass
        
    @abstractmethod
    def update_analysis(self) -> None:
        """Update de analyse visualisaties.
        
        Wordt aangeroepen bij refresh.
        """
        pass
        
    def open_fullscreen_dialog(self, title: str, create_content_func):
        """Open een fullscreen dialog voor grafieken.
        
        Parameters:
        ----------
        title : str
            Titel voor het fullscreen venster
        create_content_func : function
            Functie die de content creëert, krijgt parent frame als argument
        """
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
        
        # Header frame met moderne styling
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
        
        # Export knop
        export_btn = tk.Button(
            header_content,
            text="💾 Exporteer",
            font=("Arial", 11),
            bg='#27AE60',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2',
            command=lambda: self._export_fullscreen_chart(title)
        )
        export_btn.pack(side='right', padx=(0, 10))
        
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
        
        # Content frame
        content_frame = tk.Frame(fullscreen_window, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Roep de content creatie functie aan
        create_content_func(content_frame)
        
        # Focus op het venster
        fullscreen_window.focus_set()
        fullscreen_window.grab_set()
        
    def _export_fullscreen_chart(self, title: str):
        """Export de huidige grafiek (placeholder voor toekomstige implementatie)."""
        messagebox.showinfo(
            "Export Functie",
            f"Export van '{title}' komt in een toekomstige versie.\n\n"
            "De grafiek zal opgeslagen worden als PNG/PDF."
        )
        
    def create_chart_header(self, parent: tk.Frame, title: str, fullscreen_callback=None) -> tk.Frame:
        """Creëer een standaard header voor charts met optionele fullscreen knop.
        
        Parameters:
        ----------
        parent : tk.Frame
            Parent frame voor de header
        title : str
            Titel van de chart
        fullscreen_callback : function, optional
            Callback functie voor fullscreen knop
            
        Returns:
        -------
        tk.Frame
            Header frame
        """
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        # Titel
        tk.Label(
            header_frame,
            text=title,
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#2C3E50'
        ).pack(side='left')
        
        # Fullscreen knop indien callback gegeven
        if fullscreen_callback:
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
                command=fullscreen_callback
            )
            fullscreen_btn.pack(side='right')
            
        return header_frame 