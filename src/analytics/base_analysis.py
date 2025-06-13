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
        
    def load_data(self, force_reload: bool = False) -> pd.DataFrame:
        """Laad data uit master_calculations.csv met caching.
        
        Parameters:
        ----------
        force_reload : bool
            Force nieuwe data load, negeer cache
            
        Returns:
        -------
        pd.DataFrame
            DataFrame met berekeningen
        """
        if self._data_cache is None or force_reload:
            try:
                # Laad master calculations uit exports folder
                # Check of base_dir al 'exports' eindigt
                if hasattr(self.data_manager, 'base_dir'):
                    if isinstance(self.data_manager.base_dir, str):
                        base_dir = self.data_manager.base_dir
                    else:
                        base_dir = str(self.data_manager.base_dir)
                    
                    if base_dir.endswith('exports'):
                        log_path = os.path.join(base_dir, 'master_calculations.csv')
                    else:
                        log_path = os.path.join(base_dir, 'exports', 'master_calculations.csv')
                else:
                    # Fallback
                    log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'exports', 'master_calculations.csv')
                
                if os.path.exists(log_path):
                    self._data_cache = pd.read_csv(log_path)
                    # Converteer timestamp naar datetime met flexibele parsing
                    if 'timestamp' in self._data_cache.columns:
                        try:
                            # Gebruik 'mixed' format voor verschillende timestamp formaten
                            self._data_cache['timestamp'] = pd.to_datetime(
                                self._data_cache['timestamp'], 
                                format='mixed',
                                utc=False
                            )
                        except Exception as e:
                            print(f"DEBUG: Timestamp parsing error: {e}")
                            # Fallback: probeer te parsen zonder format
                            self._data_cache['timestamp'] = pd.to_datetime(
                                self._data_cache['timestamp']
                            )
                else:
                    # Leeg DataFrame met juiste kolommen
                    self._data_cache = pd.DataFrame()
                    
            except Exception as e:
                print(f"Fout bij laden data: {e}")
                self._data_cache = pd.DataFrame()
                
        return self._data_cache
        
    def load_complete_data(self, force_reload: bool = False) -> pd.DataFrame:
        """Laad complete data uit calculation_log.csv.
        
        Deze methode laadt de volledige calculation_log.csv die alle 31 kolommen bevat,
        in tegenstelling tot master_calculations.csv die een subset is.
        
        Parameters:
        ----------
        force_reload : bool
            Force nieuwe data load, negeer cache
            
        Returns:
        -------
        pd.DataFrame
            DataFrame met complete berekeningen inclusief print_hours etc.
        """
        cache_key = '_complete_data_cache'
        
        if not hasattr(self, cache_key) or getattr(self, cache_key) is None or force_reload:
            try:
                # Bepaal pad naar calculation_log.csv
                if hasattr(self.data_manager, 'base_dir'):
                    if isinstance(self.data_manager.base_dir, str):
                        base_dir = self.data_manager.base_dir
                    else:
                        base_dir = str(self.data_manager.base_dir)
                    
                    if base_dir.endswith('exports'):
                        log_path = os.path.join(base_dir, 'calculation_log.csv')
                    else:
                        log_path = os.path.join(base_dir, 'exports', 'calculation_log.csv')
                else:
                    # Fallback
                    log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'exports', 'calculation_log.csv')
                
                if os.path.exists(log_path):
                    setattr(self, cache_key, pd.read_csv(log_path))
                    df = getattr(self, cache_key)
                    
                    # Converteer timestamp naar datetime
                    if 'timestamp' in df.columns:
                        try:
                            df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', utc=False)
                        except:
                            df['timestamp'] = pd.to_datetime(df['timestamp'])
                    
                    # Parse date kolom ook
                    if 'date' in df.columns:
                        try:
                            df['date'] = pd.to_datetime(df['date'])
                        except:
                            pass
                            
                    print(f"Loaded {len(df)} rows from calculation_log.csv with {len(df.columns)} columns")
                else:
                    print(f"calculation_log.csv not found at: {log_path}")
                    setattr(self, cache_key, pd.DataFrame())
                    
            except Exception as e:
                print(f"Fout bij laden complete data: {e}")
                setattr(self, cache_key, pd.DataFrame())
                
        return getattr(self, cache_key)
        
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
            self.load_data(force_reload=True)
            
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