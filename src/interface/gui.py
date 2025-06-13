"""
GUI Module - H2D Price Calculator
================================

Deze module implementeert de grafische gebruikersinterface voor de H2D Price Calculator
using modern tkinter met professionele UX patterns en real-time calculatie feedback.

GUI Architectuur & Design Filosofie:
-----------------------------------
De GUI volgt een hybride MVC (Model-View-Controller) architectuur:

**Model Layer**: Business logic modules (cost_engine, pricing_engine, materials)
- Zuivere business logica zonder GUI dependencies
- Type-safe data transfer via dataclasses (CostBreakdown, PriceResult)
- Configureerbare parameters via config system

**View Layer**: tkinter widget hiërarchie met professionele styling
- Tabbed interface voor functionaliteit scheiding (Calculator vs Config)
- Responsive layout met proper grid/pack management
- Consistent Bambu Lab branding en kleurenschema
- Accessibility overwegingen (keyboard navigation, clear labels)

**Controller Layer**: Event handling en data binding in H2DCalculatorGUI
- Real-time input validatie met gebruiksvriendelijke error messages
- Automatic calculation triggers op input wijzigingen
- Configuration persistence voor user preferences
- Professional export functies (CSV, clipboard)

User Experience Design Patterns:
-------------------------------
1. **Progressive Disclosure**: Basis calculator → Advanced configuratie
2. **Immediate Feedback**: Real-time berekeningen en statusbar updates  
3. **Error Prevention**: Input validatie met constructive error messages
4. **Consistency**: Uniforme button styling, spacing en interaction patterns
5. **Forgiveness**: Reset functies en auto-save configuratie
6. **Professional Workflow**: Export, copy-paste, en batch processing support

Widget Hiërarchie & Layout Strategie:
------------------------------------
```
Root Window (900x600)
├── Header Frame (Brand styling)
├── Notebook (Tabbed interface)
│   ├── Calculator Tab
│   │   ├── Input Frame (Left panel)
│   │   │   ├── Parameter inputs (weight, material, time)
│   │   │   ├── Options checkboxes (multicolor, abrasive, rush)
│   │   │   └── Action buttons (calculate, reset)
│   │   └── Results Frame (Right panel)  
│   │       ├── TreeView (Cost breakdown display)
│   │       └── Export buttons (CSV, clipboard)
│   └── Configuration Tab
│       └── Scrollable Frame (Parameter categories)
│           ├── Basic Costs (Energy, labor, overhead)
│           ├── Markups (Material, variable pricing)
│           ├── Surcharges (Rush, abrasive, multicolor)
│           └── Save/Reset actions
└── Status Bar (Feedback en berekening status)
```

Data Flow & State Management:
---------------------------
1. **Input Capture**: tkinter StringVar/BooleanVar voor reactive programming
2. **Validation Pipeline**: Type checking → Business rule validation → User feedback
3. **Calculation Pipeline**: Input normalization → Business logic calls → Result formatting
4. **State Persistence**: Configuration auto-save met graceful degradation
5. **Export Pipeline**: Data serialization → Format selection → File/clipboard output

Modern GUI Best Practices Implemented:
-------------------------------------
- **Separation of Concerns**: GUI logic apart van business logic
- **Event-Driven Architecture**: Loose coupling via callback patterns  
- **Defensive Programming**: Input sanitization en exception handling
- **Responsive Design**: Proper widget scaling en minimum sizes
- **Accessibility**: Tab order, keyboard shortcuts, clear labeling
- **Professional Polish**: Consistent spacing, fonts, en visual hierarchy

Integration met Business Logic:
------------------------------
De GUI werkt als thin client die business logic modules orkestreert:
- **cost_engine**: Voor kostprijsberekeningen met runtime configuratie
- **pricing_engine**: Voor verkoopprijzen en winstmarge analyse  
- **materials**: Voor materiaal database lookups en pricing
- **config**: Voor parameter management en user preferences
- **utils**: Voor data formatting, export en validation utilities

Performance Considerations:
--------------------------
- **Lazy Loading**: Widgets worden on-demand gecreëerd
- **Efficient Updates**: Minimale redraws door selective widget updates
- **Memory Management**: Proper cleanup van tkinter resources
- **Responsive UI**: Non-blocking operations met proper error handling

Gebruik:
-------
    >>> # Programmatische start
    >>> app = H2DCalculatorGUI()
    >>> app.run()
    
    >>> # CLI integration
    >>> from interface.gui import main
    >>> main()  # Start GUI vanuit command line

Testing & Development:
---------------------
GUI module ondersteunt development workflow:
- Configuratie persistence voor consistent testing
- Export functies voor result verification  
- Real-time calculation voor immediate feedback
- Error handling met descriptive messages

Extensibility Design:
--------------------
Module is ontworpen voor toekomstige uitbreidingen:
- Plugin architecture via tab system
- Configurable business rules via settings
- Modular widget creation voor neue functionaliteit
- Themable UI via centralized color management

Auteur: H2D Systems
Versie: 1.0
Platform: Windows/macOS/Linux (cross-platform tkinter)
"""

# Standard library imports
from datetime import datetime
from typing import Dict, Any, List, Optional

# Third-party imports
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
import sys
import os
import subprocess

# Local application imports
from ..config.user_config import save_user_config, load_user_config
from ..core.cost_engine import CostBreakdown
from ..core.pricing_engine import PriceResult
from ..materials.materials import list_materials, get_material, get_price
from ..materials.material_properties import is_abrasive_material
from ..utils.utils import format_euro, export_calculation_csv
from ..utils.data_manager import DataManager
from ..products import Product, ProductManager


class H2DCalculatorGUI:
    """Hoofdklasse voor de H2D Price Calculator grafische interface.
    
    Deze klasse implementeert een moderne, professionele tkinter GUI voor
    3D printing kostprijsberekeningen. De interface volgt UX best practices
    met real-time feedback, input validatie en intuïtieve workflow.
    
    Architectuur:
    ------------
    - **MVC Pattern**: Scheiding tussen business logic en presentation
    - **Event-Driven**: Reactive UI updates via tkinter variable bindings
    - **Modular Design**: Gescheiden tab interfaces voor verschillende functionaliteiten
    - **State Management**: Persistent configuration met graceful degradation
    
    Features:
    --------
    - Real-time kostprijsberekeningen met live updates
    - Configureerbare business parameters via Settings tab
    - Professional data export (CSV, clipboard) 
    - Input validatie met gebruiksvriendelijke error handling
    - Responsive layout met professional Bambu Lab branding
    - Cross-platform compatibility (Windows/macOS/Linux)
    
    Workflow:
    --------
    1. **Input**: Gebruiker voert parameters in (gewicht, materiaal, opties)
    2. **Validation**: Real-time input checks met immediate feedback
    3. **Calculation**: Automatic business logic calls bij input wijzigingen
    4. **Display**: Structured result presentation in TreeView format
    5. **Export**: Professional output via multiple formats
    
    UI Components:
    -------------
    - **Calculator Tab**: Primaire interface voor kostenberekeningen
    - **Configuration Tab**: Advanced parameter tuning voor power users
    - **Products Tab**: Product management en database functionaliteit
    - **Status Bar**: Real-time feedback over berekening status
    - **Export Panel**: Professional data output functies
    
    Example:
    -------
        >>> # Basic usage
        >>> app = H2DCalculatorGUI()
        >>> app.run()  # Start interactive GUI
        
        >>> # Programmatic integration
        >>> calculator = H2DCalculatorGUI()
        >>> calculator.weight_var.set("100")
        >>> calculator.material_var.set("PLA Basic") 
        >>> calculator.calculate_price()
        >>> result = calculator.result_data
        
    Note:
    ----
    Deze klasse is thread-safe voor GUI operations maar business logic
    calls moeten vanuit de main thread gebeuren (tkinter limitation).
    """
    
    def __init__(self) -> None:
        """Initialiseer de H2D Calculator GUI met alle componenten.
        
        Creëert de complete GUI hiërarchie inclusief:
        - Root window met professional styling
        - All tkinter variables voor reactive data binding
        - Widget hiërarchie (tabs, frames, controls)
        - Event bindings voor real-time updates
        - Configuration loading met fallback defaults
        
        De initialisatie volgt een gestructureerde workflow:
        1. Setup root window en styling theme
        2. Create reactive variables (StringVar, BooleanVar)
        3. Build widget hierarchy (header, tabs, statusbar)
        4. Configure layout management (grid weights, pack options)
        5. Bind events voor interactive behavior
        
        Raises:
        ------
        ImportError
            Als verplichte GUI dependencies ontbreken
        tk.TclError
            Bij GUI initialisatie problemen (display issues)
            
        Example:
        -------
            >>> try:
            ...     app = H2DCalculatorGUI()
            ...     print("GUI succesvol geïnitialiseerd")
            ... except tk.TclError as e:
            ...     print(f"Display probleem: {e}")
        """
        # Initialize tkinter root window
        self.root = tk.Tk()
        
        # Initialize ProductManager voor product opslag functionaliteit
        # Dit moet VOOR create_widgets() omdat de products tab deze nodig heeft
        self.product_manager = ProductManager("data/h2d_products.json")
        
        # Initialize DataManager voor export/import en analyse functionaliteit
        # Gebruik absoluut pad relatief aan bedrijfsleider directory
        bedrijfsleider_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        exports_path = os.path.join(bedrijfsleider_dir, "exports")
        self.data_manager = DataManager(exports_path)
        
        # Build GUI components in logical order
        self.setup_window()        # Configure main window properties
        self.create_variables()    # Initialize reactive variables
        self.create_widgets()      # Build widget hierarchy
        self.setup_layout()        # Configure layout management  
        self.bind_events()         # Connect event handlers
        
    def setup_window(self) -> None:
        """Configureer het hoofdvenster met professional styling en branding.
        
        Stelt alle window-level eigenschappen in:
        - Window title, size en resizing behavior
        - Background colors en visual theme
        - Window positioning en visibility management
        - Professional Bambu Lab color scheme
        
        Design Rationale:
        ----------------
        - **900x600 default**: Optimaal voor laptop screens (1366x768+)
        - **Resizable**: Flexibiliteit voor verschillende screen sizes  
        - **Professional colors**: Bambu Lab branding consistency
        - **Topmost handling**: Zichtbaarheid zonder permanent-on-top irritatie
        
        Color Scheme:
        ------------
        - Primary (#00A86B): Bambu Lab signature green voor accent elements
        - Secondary (#2E8B57): Darker green for hover states
        - Background (#f8f8f8): Light gray voor clean, minimal appearance
        - Text (#333333): Dark gray voor optimal readability
        """
        # Window configuration
        self.root.title("H2D Prijs Calculator - Bambu Lab Edition")
        self.root.geometry("900x600")  # Optimal size for laptop screens
        self.root.configure(bg="#f8f8f8")
        self.root.resizable(True, True)  # Allow user to resize for different workflows
        
        # Visibility management: Show window prominently but don't stay on top
        self.root.lift()  # Bring to front
        self.root.attributes('-topmost', True)  # Temporary topmost
        self.root.after_idle(lambda: self.root.attributes('-topmost', False))  # Release after idle
        
        # Professional Bambu Lab color scheme
        self.colors: Dict[str, str] = {
            'bg': '#f8f8f8',           # Light background for clean appearance
            'primary': '#00A86B',       # Bambu Lab signature green
            'secondary': '#2E8B57',     # Darker green for hover states
            'accent': '#32CD32',        # Bright green for success indicators
            'text': '#333333',          # Dark gray for optimal readability
            'light_gray': '#e8e8e8',    # Light borders and separators
            'white': '#ffffff'          # Pure white for input backgrounds
        }
        
    def create_variables(self) -> None:
        """Initialiseer alle tkinter variables voor reactive data binding.
        
        Creëert StringVar en BooleanVar objecten die de GUI state managen
        via tkinter's reactive programming model. Deze variables zorgen voor
        automatic UI updates wanneer data wijzigt.
        
        Variable Categories:
        -------------------
        **Input Variables**: Direct user input voor calculatie parameters
        - weight_var: Print gewicht in gram (StringVar voor flexible input)
        - material_var: Geselecteerd materiaal naam 
        - hours_var: Print tijd in uren (manual override van auto calculation)
        - auto_hours_var: Boolean voor automatic time calculation (default: True)
        
        **Option Variables**: Boolean flags voor print complexiteit
        - multicolor_var: Multi-kleur print (AMS usage)
        - abrasive_var: Abrasief materiaal (CF/GF)
        - rush_var: Spoedopdracht (urgency surcharge)
        
        **Configuration Variables**: Advanced business parameters
        - config_vars: Dictionary van StringVar voor alle config parameters
        - Loaded vanuit persistent storage met graceful fallbacks
        
        **Result Variables**: Calculation output storage
        - result_data: Dictionary voor export en clipboard functionality
        
        Reactive Programming Pattern:
        ---------------------------
        Deze variables ondersteunen tkinter's trace() mechanism voor:
        - Real-time input validation
        - Automatic calculation triggering
        - UI state synchronization
        - Event-driven updates zonder manual polling
        
        Configuration Persistence:
        -------------------------
        Config variables worden geïnitialiseerd vanuit opgeslagen user preferences
        met intelligent fallbacks naar business defaults. Dit zorgt voor:
        - Consistent user experience tussen sessies
        - Graceful degradation bij corrupt config files
        - Professional workflow continuity
        
        Example:
        -------
            >>> gui = H2DCalculatorGUI()
            >>> gui.weight_var.set("150")  # Triggers automatic calculation
            >>> print(gui.auto_hours_var.get())  # True (default)
            >>> gui.multicolor_var.set(True)  # Enables multicolor surcharge
        """
        # === PRIMARY INPUT VARIABLES ===
        # Core calculation parameters - StringVar for flexible user input
        self.weight_var = tk.StringVar()      # Print weight in grams
        self.material_var = tk.StringVar()    # Selected material name
        self.hours_var = tk.StringVar()       # Manual print time override
        
        # === CALCULATION CONTROL ===
        # Boolean flag for automatic vs manual time calculation
        self.auto_hours_var = tk.BooleanVar(value=True)  # Default to auto mode
        
        # === PRINT OPTION FLAGS ===
        # Boolean variables voor print complexity options
        self.multicolor_var = tk.BooleanVar()  # Multi-color print (AMS)
        self.abrasive_var = tk.BooleanVar()    # Abrasive material (CF/GF)
        self.rush_var = tk.BooleanVar()        # Rush order surcharge
        
        # === RESULT STORAGE ===
        # Dictionary voor calculation results en export functionality
        self.result_data: Dict[str, Any] = {}
        
        # === CONFIGURATION PERSISTENCE ===
        # Load saved user configuration met graceful degradation
        saved_config: Dict[str, str] = load_user_config()
        
        # Configuration variables met intelligent defaults
        # Each parameter heeft business rationale en fallback waarde
        self.config_vars: Dict[str, tk.StringVar] = {
            # Basic operational costs
            'printer_power': tk.StringVar(value=saved_config.get('printer_power', "1.05")),     # kW
            'energy_price': tk.StringVar(value=saved_config.get('energy_price', "0.30")),       # €/kWh
            'labour_cost': tk.StringVar(value=saved_config.get('labour_cost', "23.50")),        # €/hour
            'monitoring_pct': tk.StringVar(value=saved_config.get('monitoring_pct', "10")),     # % of labor
            'maintenance_cost': tk.StringVar(value=saved_config.get('maintenance_cost', "0.0765")), # €/hour
            
            # Overhead distribution
            'overhead_year': tk.StringVar(value=saved_config.get('overhead_year', "6669")),     # € annually
            'annual_hours': tk.StringVar(value=saved_config.get('annual_hours', "2000")),       # Hours/year
            
            # Pricing strategy
            'markup_material': tk.StringVar(value=saved_config.get('markup_material', "200")),  # % markup
            'markup_variable': tk.StringVar(value=saved_config.get('markup_variable', "150")),  # % markup
            
            # Surcharges
            'spoed_surcharge': tk.StringVar(value=saved_config.get('spoed_surcharge', "25")),   # % surcharge
            'abrasive_surcharge': tk.StringVar(value=saved_config.get('abrasive_surcharge', "0.50")), # €/hour
            'color_fee_min': tk.StringVar(value=saved_config.get('color_fee_min', "15")),       # € minimum
            'color_fee_max': tk.StringVar(value=saved_config.get('color_fee_max', "30")),       # € maximum
            
            # Automation parameters
            'auto_time_per_gram': tk.StringVar(value=saved_config.get('auto_time_per_gram', "0.04"))  # hours/gram
        }
        
    def create_widgets(self) -> None:
        """Construeer de complete widget hiërarchie met professional layout.
        
        Bouwt alle GUI componenten in een gestructureerde volgorde:
        1. Header met branding en applicatie titel
        2. Tabbed interface voor functionaliteit scheiding
        3. Calculator tab met input/output panels
        4. Configuration tab met scrollable parameter grid
        5. Products tab: Product management en database functionaliteit
        6. Status bar voor user feedback
        7. Export panel
        
        Design Patterns Used:
        --------------------
        - **Progressive Disclosure**: Basis features → Advanced configuration
        - **Spatial Grouping**: Gerelateerde controls bij elkaar
        - **Visual Hierarchy**: Consistent typography en spacing
        - **Professional Polish**: Bambu Lab branding en kleuren
        
        Widget Architecture:
        ------------------
        ```
        create_header()          → Brand header met titel
        ttk.Notebook            → Tab container voor functionaliteit
        ├── create_calculator_tab() → Primary calculation interface  
        ├── create_config_tab()     → Advanced parameter tuning
        ├── create_products_tab()   → Product management interface
        ├── create_analysis_tab()   → Data analyse interface
        └── create_statusbar()      → Status feedback panel
        ```
        
        Accessibility Features:
        ----------------------
        - Logical tab order voor keyboard navigation
        - Clear labels en descriptions
        - Consistent interaction patterns
        - Error prevention via validation
        """
        # === HEADER SECTION ===
        # Professional branding en applicatie titel
        self.create_header()
        
        # === TABBED INTERFACE CONTAINER ===
        # Progressive disclosure pattern: basis functionaliteit → advanced config → products → results
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # === TAB CREATION ===
        # Calculator tab: Primary user interface voor kostprijsberekeningen
        self.calc_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.calc_frame, text="🧮 Calculator")
        
        # Configuration tab: Advanced parameter tuning voor power users
        self.config_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.config_frame, text="⚙️ Configuratie")
        
        # Products tab: Product management en database functionaliteit
        self.products_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.products_frame, text="📦 Producten")
        
        # Analysis tab: Data analyse en rapportage functionaliteit
        self.analysis_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.analysis_frame, text="📊 Analyse")
        
        # === STATUS BAR ===
        # Real-time feedback over applicatie staat
        # MOET VOOR tab creation omdat sommige tabs de status_label gebruiken
        self.create_statusbar()
        
        # === TAB CONTENT CREATION ===
        # Build specialized content voor elke tab
        self.create_calculator_tab()  # Primary calculation interface
        self.create_config_tab()      # Advanced business parameter tuning
        self.create_products_tab()    # Product management interface
        self.create_analysis_tab()    # Data analyse interface
        
    def create_header(self) -> None:
        """Creëer professional header met Bambu Lab branding.
        
        Design Elements:
        ---------------
        - Signature Bambu Lab green background (#00A86B)
        - Professional typography (Arial 18pt bold)
        - Centered layout met emoji accent (🖨️)
        - Fixed height (60px) voor consistent visual hierarchy
        - White text voor optimal contrast tegen groene achtergrond
        
        Branding Strategy:
        -----------------
        Header establishes immediate brand recognition en product identity.
        De groene kleur connecteert direct met Bambu Lab ecosystem while
        emoji adds friendly, approachable touch to professional interface.
        """
        # Create header container met fixed height voor consistent layout
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)  # Maintain fixed height
        
        # Professional title label met brand styling
        title_label = tk.Label(
            header_frame,
            text="🖨️ H2D Prijs Calculator",  # Emoji voor friendly touch
            font=("Arial", 18, "bold"),
            bg=self.colors['primary'],
            fg='white'  # High contrast voor readability
        )
        title_label.pack(pady=15)  # Centered vertical positioning
        
    def create_calculator_tab(self):
        """Maak calculator tab"""
        # Main container voor calculator tab
        self.main_container = tk.Frame(self.calc_frame, bg=self.colors['bg'])
        self.main_container.pack(fill='both', expand=True)
        
        # Input frame (links)
        self.input_frame = tk.LabelFrame(
            self.main_container,
            text="📝 Invoer Parameters",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        self.input_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Gewicht input
        tk.Label(
            self.input_frame,
            text="Gewicht (gram):",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        weight_frame = tk.Frame(self.input_frame, bg=self.colors['white'])
        weight_frame.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        self.weight_entry = tk.Entry(
            weight_frame,
            textvariable=self.weight_var,
            font=("Arial", 10),
            width=15
        )
        self.weight_entry.pack(side='left')
        
        self.weight_spinbox = tk.Spinbox(
            weight_frame,
            from_=1,
            to=1000,
            textvariable=self.weight_var,
            font=("Arial", 10),
            width=5
        )
        self.weight_spinbox.pack(side='left', padx=(5, 0))
        
        # Materiaal selectie
        tk.Label(
            self.input_frame,
            text="Materiaal:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.material_combo = ttk.Combobox(
            self.input_frame,
            textvariable=self.material_var,
            values=list(list_materials().keys()),
            state='readonly',
            font=("Arial", 10),
            width=20
        )
        self.material_combo.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        self.material_combo.set("PLA Basic")  # Default waarde
        
        # Printtijd
        tk.Label(
            self.input_frame,
            text="Printtijd (uren):",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=2, column=0, sticky='w', pady=5)
        
        hours_frame = tk.Frame(self.input_frame, bg=self.colors['white'])
        hours_frame.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        self.hours_entry = tk.Entry(
            hours_frame,
            textvariable=self.hours_var,
            font=("Arial", 10),
            width=10
        )
        self.hours_entry.pack(side='left')
        
        self.auto_hours_check = tk.Checkbutton(
            hours_frame,
            text="Auto (0.04 u/g)",
            variable=self.auto_hours_var,
            font=("Arial", 9),
            bg=self.colors['white'],
            command=self.toggle_hours_entry
        )
        self.auto_hours_check.pack(side='left', padx=(10, 0))
        
        # Opties checkboxes
        options_frame = tk.LabelFrame(
            self.input_frame,
            text="🔧 Extra Opties",
            font=("Arial", 10, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text']
        )
        options_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=15)
        
        self.multicolor_check = tk.Checkbutton(
            options_frame,
            text="🎨 Meerkleurige print (AMS)",
            variable=self.multicolor_var,
            font=("Arial", 10),
            bg=self.colors['white'],
            command=self.calculate_price
        )
        self.multicolor_check.pack(anchor='w', pady=2)
        
        self.abrasive_check = tk.Checkbutton(
            options_frame,
            text="⚙️ Abrasief materiaal (CF/GF)",
            variable=self.abrasive_var,
            font=("Arial", 10),
            bg=self.colors['white'],
            command=self.calculate_price
        )
        self.abrasive_check.pack(anchor='w', pady=2)
        
        self.rush_check = tk.Checkbutton(
            options_frame,
            text="⚡ Spoedopdracht (<48u)",
            variable=self.rush_var,
            font=("Arial", 10),
            bg=self.colors['white'],
            command=self.calculate_price
        )
        self.rush_check.pack(anchor='w', pady=2)
        
        # Actie knoppen
        button_frame = tk.Frame(self.input_frame, bg=self.colors['white'])
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.calculate_btn = tk.Button(
            button_frame,
            text="💰 Bereken Prijs",
            command=self.calculate_price,
            font=("Arial", 12, "bold"),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.calculate_btn.pack(side='left', padx=(0, 10))
        
        self.reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset_form,
            font=("Arial", 10),
            bg=self.colors['light_gray'],
            fg=self.colors['text'],
            padx=15,
            pady=10,
            cursor='hand2'
        )
        self.reset_btn.pack(side='left')
        
        # Grid configuratie
        self.input_frame.columnconfigure(1, weight=1)
        
        # Result frame (rechts)
        self.result_frame = tk.LabelFrame(
            self.main_container,
            text="📊 Resultaten",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        self.result_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Resultaten treeview
        columns = ('Item', 'Waarde')
        self.result_tree = ttk.Treeview(
            self.result_frame,
            columns=columns,
            show='headings',
            height=12
        )
        
        # Column headers
        self.result_tree.heading('Item', text='Kostenpost')
        self.result_tree.heading('Waarde', text='Bedrag (€)')
        
        # Column widths
        self.result_tree.column('Item', width=200)
        self.result_tree.column('Waarde', width=120, anchor='e')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.result_frame,
            orient='vertical',
            command=self.result_tree.yview
        )
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview en scrollbar
        self.result_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Export knoppen
        export_frame = tk.Frame(self.result_frame, bg=self.colors['white'])
        export_frame.pack(fill='x', pady=(10, 0))
        
        self.export_csv_btn = tk.Button(
            export_frame,
            text="📄 Export CSV",
            command=self.export_csv,
            font=("Arial", 9),
            bg=self.colors['secondary'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        self.export_csv_btn.pack(side='left', padx=(0, 5))
        
        self.copy_btn = tk.Button(
            export_frame,
            text="📋 Kopieer",
            command=self.copy_to_clipboard,
            font=("Arial", 9),
            bg=self.colors['accent'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        self.copy_btn.pack(side='left')
        
    def create_config_tab(self):
        """Maak configuratie tab"""
        # Scrollable frame
        canvas = tk.Canvas(self.config_frame, bg=self.colors['bg'])
        scrollbar = ttk.Scrollbar(self.config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Basis kosten
        basic_frame = tk.LabelFrame(
            scrollable_frame,
            text="💰 Basis Kosten",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        basic_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        self._add_config_field(basic_frame, "Printer vermogen (kW):", 'printer_power', 0)
        self._add_config_field(basic_frame, "Energie prijs (€/kWh):", 'energy_price', 1)
        self._add_config_field(basic_frame, "Arbeidskosten (€/uur):", 'labour_cost', 2)
        self._add_config_field(basic_frame, "Monitoring percentage (%):", 'monitoring_pct', 3)
        self._add_config_field(basic_frame, "Onderhoudskosten (€/uur):", 'maintenance_cost', 4)
        self._add_config_field(basic_frame, "Overhead per jaar (€):", 'overhead_year', 5)
        self._add_config_field(basic_frame, "Jaarlijkse printuren:", 'annual_hours', 6)
        
        # Marges
        margin_frame = tk.LabelFrame(
            scrollable_frame,
            text="📈 Marges & Mark-ups",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        margin_frame.pack(fill='x', padx=10, pady=5)
        
        self._add_config_field(margin_frame, "Materiaal mark-up (%):", 'markup_material', 0)
        self._add_config_field(margin_frame, "Variabele mark-up (%):", 'markup_variable', 1)
        
        # Toeslagen
        surcharge_frame = tk.LabelFrame(
            scrollable_frame,
            text="➕ Toeslagen",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        surcharge_frame.pack(fill='x', padx=10, pady=5)
        
        self._add_config_field(surcharge_frame, "Spoedtoeslag (%):", 'spoed_surcharge', 0)
        self._add_config_field(surcharge_frame, "Abrasief toeslag (€/uur):", 'abrasive_surcharge', 1)
        self._add_config_field(surcharge_frame, "Kleur setup min (€):", 'color_fee_min', 2)
        self._add_config_field(surcharge_frame, "Kleur setup max (€):", 'color_fee_max', 3)
        
        # Overige
        other_frame = tk.LabelFrame(
            scrollable_frame,
            text="🔧 Overige Instellingen",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        other_frame.pack(fill='x', padx=10, pady=5)
        
        self._add_config_field(other_frame, "Auto tijd per gram (u/g):", 'auto_time_per_gram', 0)
        
        # Actie knoppen
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        button_frame.pack(fill='x', padx=10, pady=20)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 Opslaan",
            command=self.save_config,
            font=("Arial", 11, "bold"),
            bg=self.colors['primary'],
            fg='white',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        save_btn.pack(side='left', padx=(0, 10))
        
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset naar standaard",
            command=self.reset_config,
            font=("Arial", 11),
            bg=self.colors['secondary'],
            fg='white',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        reset_btn.pack(side='left')
        
        # Pack canvas en scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def create_products_tab(self):
        """Maak products tab voor product management.
        
        Deze tab biedt complete CRUD functionaliteit voor producten:
        - Opslaan van huidige berekeningen als product
        - Laden van bestaande producten
        - Lijst weergave van alle producten
        - Zoeken en filteren
        - Product statistieken
        """
        # Main container met twee panelen
        main_container = tk.Frame(self.products_frame, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True)
        
        # === LINKER PANEEL: Product acties ===
        left_panel = tk.Frame(main_container, bg=self.colors['bg'])
        left_panel.pack(side='left', fill='both', expand=True, padx=(10, 5))
        
        # Huidige berekening frame
        current_frame = tk.LabelFrame(
            left_panel,
            text="💾 Huidige Berekening",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        current_frame.pack(fill='x', pady=(10, 5))
        
        # Product naam input
        tk.Label(
            current_frame,
            text="Product naam:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.product_name_var = tk.StringVar()
        self.product_name_entry = tk.Entry(
            current_frame,
            textvariable=self.product_name_var,
            font=("Arial", 10),
            width=30
        )
        self.product_name_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Product beschrijving
        tk.Label(
            current_frame,
            text="Beschrijving:",
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=1, column=0, sticky='nw', pady=5)
        
        self.product_desc_text = tk.Text(
            current_frame,
            font=("Arial", 10),
            width=30,
            height=3
        )
        self.product_desc_text.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Opslaan knop
        save_product_btn = tk.Button(
            current_frame,
            text="💾 Opslaan als Product",
            command=self.save_as_product,
            font=("Arial", 11, "bold"),
            bg=self.colors['primary'],
            fg='white',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        save_product_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        current_frame.columnconfigure(1, weight=1)
        
        # Zoek frame
        search_frame = tk.LabelFrame(
            left_panel,
            text="🔍 Zoeken",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        search_frame.pack(fill='x', pady=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=25
        )
        self.search_entry.pack(side='left', padx=(0, 10))
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Zoek",
            command=self.search_products,
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        search_btn.pack(side='left')
        
        # Filter frame
        filter_frame = tk.LabelFrame(
            left_panel,
            text="🏷️ Filter op Materiaal",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        filter_frame.pack(fill='x', pady=5)
        
        self.filter_material_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_material_var,
            values=['Alle'] + list(list_materials().keys()),
            state='readonly',
            font=("Arial", 10),
            width=20
        )
        self.filter_combo.pack(side='left', padx=(0, 10))
        self.filter_combo.set("Alle")
        
        filter_btn = tk.Button(
            filter_frame,
            text="🏷️ Filter",
            command=self.filter_products,
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        filter_btn.pack(side='left')
        
        # Statistieken frame
        stats_frame = tk.LabelFrame(
            left_panel,
            text="📊 Statistieken",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        stats_frame.pack(fill='x', pady=5)
        
        self.stats_text = tk.Text(
            stats_frame,
            font=("Arial", 10),
            width=35,
            height=6,
            state='disabled',
            bg=self.colors['light_gray']
        )
        self.stats_text.pack()
        
        # === RECHTER PANEEL: Product lijst ===
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 10))
        
        # Product lijst frame
        list_frame = tk.LabelFrame(
            right_panel,
            text="📦 Product Database",
            font=("Arial", 12, "bold"),
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=10
        )
        list_frame.pack(fill='both', expand=True, pady=(10, 5))
        
        # Treeview voor producten
        columns = ('ID', 'Naam', 'Materiaal', 'Gewicht', 'Prijs', 'Marge', 'Orders')
        self.product_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='tree headings',
            height=15
        )
        
        # Column configuratie
        self.product_tree.heading('#0', text='')
        self.product_tree.heading('ID', text='Product ID')
        self.product_tree.heading('Naam', text='Naam')
        self.product_tree.heading('Materiaal', text='Materiaal')
        self.product_tree.heading('Gewicht', text='Gewicht (g)')
        self.product_tree.heading('Prijs', text='Prijs (€)')
        self.product_tree.heading('Marge', text='Marge (%)')
        self.product_tree.heading('Orders', text='Bestellingen')
        
        # Column widths
        self.product_tree.column('#0', width=0, stretch=False)
        self.product_tree.column('ID', width=120)
        self.product_tree.column('Naam', width=200)
        self.product_tree.column('Materiaal', width=100)
        self.product_tree.column('Gewicht', width=80, anchor='e')
        self.product_tree.column('Prijs', width=80, anchor='e')
        self.product_tree.column('Marge', width=80, anchor='e')
        self.product_tree.column('Orders', width=80, anchor='e')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview
        self.product_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click voor laden
        self.product_tree.bind('<Double-Button-1>', self.load_selected_product)
        
        # Actie knoppen frame
        action_frame = tk.Frame(list_frame, bg=self.colors['white'])
        action_frame.pack(fill='x', pady=(10, 0))
        
        load_btn = tk.Button(
            action_frame,
            text="📂 Laad Product",
            command=self.load_selected_product,
            font=("Arial", 10),
            bg=self.colors['primary'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        load_btn.pack(side='left', padx=(0, 5))
        
        delete_btn = tk.Button(
            action_frame,
            text="🗑️ Verwijder",
            command=self.delete_selected_product,
            font=("Arial", 10),
            bg='#DC3545',
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        delete_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(
            action_frame,
            text="🔄 Vernieuwen",
            command=self.refresh_product_list,
            font=("Arial", 10),
            bg=self.colors['secondary'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        refresh_btn.pack(side='left', padx=5)
        
        export_all_btn = tk.Button(
            action_frame,
            text="📊 Export Alles",
            command=self.export_all_products,
            font=("Arial", 10),
            bg=self.colors['accent'],
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        export_all_btn.pack(side='left', padx=5)
        
        # Grafiek knop - opent visualisaties in nieuw venster
        charts_btn = tk.Button(
            action_frame,
            text="📈 Toon Grafieken",
            command=self.show_product_charts,
            font=("Arial", 10),
            bg='#6C757D',
            fg='white',
            padx=10,
            pady=5,
            cursor='hand2'
        )
        charts_btn.pack(side='left', padx=5)
        
        # Initial load van producten
        self.refresh_product_list()
        self.update_product_stats()

    def create_analysis_tab(self):
        """Maak analysis tab met nieuwe modulaire analytics GUI.
        
        Deze tab laadt de aparte AnalyticsGUI klasse die alle
        analyse modules beheert. Dit houdt de hoofdGUI clean!
        """
        # Main container
        main_container = tk.Frame(self.analysis_frame, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True)
        
        try:
            # Lazy import van analytics GUI
            from .gui_analytics import AnalyticsGUI
            
            # Maak analytics GUI instance
            self.analytics_gui = AnalyticsGUI(
                parent=main_container,
                data_manager=self.data_manager,
                colors=self.colors
            )
            
            # Pack de analytics GUI
            self.analytics_gui.pack(fill='both', expand=True)
            
            # Update status
            self.status_label.configure(text="📊 Analytics module geladen")
            
        except ImportError as e:
            # Fallback als analytics module problemen heeft
            self._show_analytics_error(main_container, e)
            
    def _show_analytics_error(self, parent, error):
        """Toon error als analytics module niet kan laden."""
        error_frame = tk.Frame(parent, bg=self.colors['bg'])
        error_frame.pack(fill='both', expand=True)
        
        # Error icon en titel
        title = tk.Label(
            error_frame,
            text="⚠️ Analytics Module Fout",
            font=("Arial", 16, "bold"),
            bg=self.colors['bg'],
            fg='red'
        )
        title.pack(pady=(50, 20))
        
        # Error details
        details = tk.Label(
            error_frame,
            text=f"De analytics module kon niet worden geladen:\n\n{str(error)}",
            font=("Arial", 11),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='center'
        )
        details.pack(pady=(0, 20))
        
        # Instructies
        instructions = tk.Label(
            error_frame,
            text="Mogelijke oplossingen:\n"
                 "1. Controleer of alle analytics bestanden aanwezig zijn\n"
                 "2. Installeer vereiste packages: pip install pandas matplotlib\n"
                 "3. Check de console voor meer details",
            font=("Arial", 10),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='left'
        )
        instructions.pack()
        
    def import_csv_data(self):
        """Import CSV data voor analyse."""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                # Placeholder voor import logica
                messagebox.showinfo("Import", f"Import functie komt binnenkort!\n\nGeselecteerd bestand: {filename}")
            except Exception as e:
                messagebox.showerror("Import Fout", f"Kon bestand niet importeren:\n{str(e)}")
                
    def export_all_data(self):
        """Export alle data voor analyse."""
        try:
            # Gebruik DataManager voor export
            summary = self.data_manager.get_export_statistics()
            messagebox.showinfo(
                "Export Info", 
                f"Data wordt automatisch geëxporteerd naar:\n{self.data_manager.base_dir}\n\n"
                f"Totaal exports: {summary['total_calculations']}\n"
                f"Export grootte: {summary['total_size_mb']:.1f} MB"
            )
        except Exception as e:
            messagebox.showerror("Export Fout", f"Kon data niet exporteren:\n{str(e)}")
            
    def clean_old_data(self):
        """Schoon oude export data op."""
        if messagebox.askyesno("Bevestiging", "Wilt u exports ouder dan 30 dagen verwijderen?"):
            try:
                removed = self.data_manager.cleanup_old_exports(days_to_keep=30)
                messagebox.showinfo("Opgeschoond", f"{removed} oude export bestanden verwijderd.")
            except Exception as e:
                messagebox.showerror("Opschoon Fout", f"Kon data niet opschonen:\n{str(e)}")

    def _add_config_field(self, parent, label_text, var_key, row):
        """Helper functie om config velden toe te voegen"""
        tk.Label(
            parent,
            text=label_text,
            font=("Arial", 10),
            bg=self.colors['white']
        ).grid(row=row, column=0, sticky='w', pady=5, padx=(0, 20))
        
        entry = tk.Entry(
            parent,
            textvariable=self.config_vars[var_key],
            font=("Arial", 10),
            width=15
        )
        entry.grid(row=row, column=1, sticky='w', pady=5)
        
        # Configureer grid
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=0)
        
    def create_statusbar(self):
        """Maak statusbar onderaan"""
        self.statusbar = tk.Frame(self.root, bg=self.colors['light_gray'], height=30)
        self.statusbar.pack(fill='x', side='bottom')
        self.statusbar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.statusbar,
            text="Klaar voor berekening...",
            font=("Arial", 9),
            bg=self.colors['light_gray'],
            fg=self.colors['text']
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
    def setup_layout(self):
        """Configureer layout en grid weights"""
        self.toggle_hours_entry()  # Initial state
        
    def bind_events(self) -> None:
        """Bind event handlers voor reactive UI behavior.
        
        Configureert tkinter variable tracing voor real-time updates:
        - Input field changes triggeren automatic validation
        - Parameter wijzigingen starten immediate recalculation  
        - Auto-calculation mode changes updaten UI state
        
        Event-Driven Architecture:
        -------------------------
        Deze binding approach implementeert reactive programming patterns
        waarbij UI automatisch reageert op data changes zonder manual
        polling of explicit update calls.
        
        Trace Callbacks:
        ---------------
        - 'w' (write): Fires wanneer variable value wijzigt
        - self.on_input_change: Handles automatic calculation triggering
        - Real-time user feedback zonder performance impact
        """
        # Bind input variables voor automatic calculation triggering
        self.weight_var.trace('w', self.on_input_change)      # Weight input changes
        self.material_var.trace('w', self.on_input_change)    # Material selection changes  
        self.hours_var.trace('w', self.on_input_change)       # Manual time input changes
        self.auto_hours_var.trace('w', self.on_input_change)  # Auto-calculation mode toggle
        
        # Bind material variable voor automatic abrasive detection
        self.material_var.trace('w', self.update_abrasive_checkbox)  # Auto-detect abrasive materials

    def toggle_hours_entry(self) -> None:
        """Schakel hours entry field enabled/disabled gebaseerd op auto checkbox.
        
        UI State Management:
        -------------------
        - Auto mode (default): Hours entry disabled, automatic calculation
        - Manual mode: Hours entry enabled voor custom print time input
        - Immediate recalculation bij mode wijziging
        
        User Experience:
        ---------------
        Prevents input confusion door clear visual indicators van active mode.
        Gray-out effect voor disabled state provides immediate feedback.
        """
        if self.auto_hours_var.get():
            self.hours_entry.configure(state='disabled')  # Visual indication van auto mode
            self.calculate_auto_hours()  # Direct auto calculation
        else:
            self.hours_entry.configure(state='normal')  # Enable voor manual input
            
    def calculate_auto_hours(self) -> None:
        """Bereken automatische print tijd gebaseerd op gewicht (0.04 u/g).
        
        Auto Calculation Logic:
        ----------------------
        Gebruikt configurable ratio (default 0.04 hours/gram) voor time estimation.
        Deze ratio is gebaseerd op gemiddelde print speeds voor standard quality.
        
        Error Handling:
        --------------
        Graceful degradation bij invalid input - defaults naar "0.00" 
        in plaats van exception throwing voor smooth user experience.
        
        Business Rule:
        -------------
        Formula: print_hours = weight_grams × time_per_gram_ratio
        Default ratio represents 25g/hour average print speed.
        """
        try:
            weight = float(self.weight_var.get() or 0)
            auto_time_per_gram = float(self.config_vars['auto_time_per_gram'].get())
            auto_hours = weight * auto_time_per_gram
            self.hours_var.set(f"{auto_hours:.2f}")  # Format to 2 decimals voor precision
        except ValueError:
            self.hours_var.set("0.00")  # Graceful fallback bij invalid input
            
    def on_input_change(self, *args) -> None:
        """Callback voor input field wijzigingen - triggert automatic updates.
        
        Real-Time Calculation Strategy:
        ------------------------------
        Only triggers full calculation when alle required fields zijn ingevuld.
        Dit voorkomt partial calculations en error states tijdens typing.
        
        Performance Optimization:
        ------------------------
        Checks voor data completeness before expensive business logic calls.
        Automatic hour calculation alleen bij auto mode activatie.
        
        Parameters:
        ----------
        *args : tuple
            Tkinter trace callback arguments (ignored)
        """
        # Update auto hours alleen in auto mode
        if self.auto_hours_var.get():
            self.calculate_auto_hours()
            
        # Trigger full calculation alleen bij complete input
        if self.weight_var.get() and self.material_var.get():
            self.calculate_price()
            
    def update_abrasive_checkbox(self, *args) -> None:
        """Update abrasive checkbox automatisch op basis van materiaal naam.
        
        Detecteert carbon fiber (CF) en glass fiber (GF) materialen
        en zet automatisch de abrasive checkbox aan/uit.
        
        Gebruikt de is_abrasive_material functie uit material_properties
        voor consistente detectie logica.
        """
        material = self.material_var.get()
        if material:
            # Gebruik de centrale detectie functie
            self.abrasive_var.set(is_abrasive_material(material))
            
    def validate_input(self) -> bool:
        """Valideer alle user input voor business logic compatibility.
        
        Validation Pipeline:
        -------------------
        1. **Weight Validation**: Positive number check met meaningful errors
        2. **Material Validation**: Existence check tegen materials database  
        3. **Time Validation**: Non-negative number voor print hours
        4. **User Feedback**: Descriptive error messages via messageboxes
        
        Business Rules Enforced:
        -----------------------
        - Weight moet positief zijn (geen 0g prints)
        - Materiaal moet bestaan in database (prevent calculation errors)
        - Print tijd kan niet negatief zijn (time travel prevention)
        
        Error Handling Strategy:
        -----------------------
        Immediate user feedback via messagebox.showerror() met:
        - Clear description van het probleem
        - Actionable guidance voor correction
        - Professional tone met Nederlandse tekst
        
        Returns:
        -------
        bool
            True als alle input valid is, False bij validation errors
            
        Example:
        -------
            >>> gui = H2DCalculatorGUI()
            >>> gui.weight_var.set("100")
            >>> gui.material_var.set("PLA Basic")  
            >>> gui.hours_var.set("4.0")
            >>> valid = gui.validate_input()  # Returns True
        """
        try:
            # === WEIGHT VALIDATION ===
            # Must be positive number voor realistic print calculations
            weight = float(self.weight_var.get())
            if weight <= 0:
                raise ValueError("Gewicht moet groter zijn dan 0 gram")
                
            # === MATERIAL VALIDATION ===
            # Must exist in materials database voor price lookup
            if not self.material_var.get():
                raise ValueError("Selecteer een materiaal uit de lijst")
                
            # === TIME VALIDATION ===  
            # Hours can be zero (auto-calculated) but not negative
            hours = float(self.hours_var.get() or 0)
            if hours < 0:
                raise ValueError("Print tijd kan niet negatief zijn")
                
            return True  # All validations passed
            
        except ValueError as e:
            # User-friendly error feedback met actionable guidance
            messagebox.showerror("Invoerfout", str(e))
            return False
            
    def calculate_price(self) -> None:
        """Hoofdfunctie voor kostprijs en verkoopprijs berekening.
        
        Business Logic Integration Workflow:
        -----------------------------------
        1. **Input Validation**: Comprehensive user input checks
        2. **Material Lookup**: Database verification van selected material
        3. **Cost Calculation**: Integration met cost_engine business logic
        4. **Price Calculation**: Integration met pricing_engine voor verkoop pricing
        5. **Result Display**: Professional formatting in TreeView widget
        6. **Status Update**: Real-time feedback via status bar
        
        Error Handling Strategy:
        -----------------------
        Multi-layered error handling voor robust user experience:
        - Input validation errors → User-friendly messageboxes
        - Material lookup errors → Clear material suggestion
        - Calculation errors → Generic error message met debugging info
        - Status bar updates → Visual feedback over calculation staat
        
        Configuration Integration:
        -------------------------
        Uses runtime configuration values vanuit GUI config tab in plaats van
        static config module. Dit allows real-time parameter updates zonder
        application restart.
        
        Performance Considerations:
        --------------------------
        - Early return bij validation failures (avoid expensive calculations)
        - Material existence check voorkomt downstream errors
        - Exception catching voorkomt UI freeze bij business logic errors
        
        Example:
        -------
            >>> gui = H2DCalculatorGUI()  
            >>> gui.weight_var.set("100")
            >>> gui.material_var.set("PLA Basic")
            >>> gui.calculate_price()  # Updates GUI met results
        """
        # === INPUT VALIDATION GATE ===
        # Early return prevents expensive calculations bij invalid input
        if not self.validate_input():
            return
            
        try:
            # === EXTRACT INPUT PARAMETERS ===
            # Convert GUI string input naar business logic types
            weight = float(self.weight_var.get())
            material_name = self.material_var.get()
            hours = float(self.hours_var.get() or 0)
            
            # === MATERIAL VERIFICATION ===
            # Verify material exists in database before expensive calculations
            material = get_material(material_name)
            if not material:
                # Provide actionable error message met suggestions
                available_materials = ', '.join(list(list_materials().keys()))
                messagebox.showerror(
                    "Materiaal Fout", 
                    f"Materiaal '{material_name}' niet gevonden in database.\n\n"
                    f"Beschikbare materialen:\n{available_materials}"
                )
                return
                
            # === BUSINESS LOGIC INTEGRATION ===
            # Call cost engine met GUI configuration parameters
            costs = self.calculate_costs_with_config(
                weight_g=weight,
                material_name=material_name,
                print_hours=hours,
                abrasive=self.abrasive_var.get()  # Boolean option
            )
            
            # Call pricing engine met alle GUI options
            price_result = self.calculate_sell_price_with_config(
                weight_g=weight,
                material_name=material_name,
                print_hours=hours,
                abrasive=self.abrasive_var.get(),
                multicolor=self.multicolor_var.get(),  # AMS usage
                spoed=self.rush_var.get()              # Urgency surcharge
            )
            
            # === RESULT PRESENTATION ===
            # Update GUI met professional formatted results
            self.update_results(costs, price_result, weight, material_name)
            
            # === UITGEBREID LOGBOEK ===
            # Log ALLE details naar calculation_log.csv voor debugging (behalve product info)
            try:
                # Haal huidige configuratie op
                config = self.get_config_values()
                
                # Maak uitgebreide log data
                log_data = {
                    'weight': weight,
                    'material': material_name,
                    'print_hours': hours,
                    'material_cost': costs.material_cost,
                    'variable_cost': costs.variable_cost,
                    'total_cost': costs.total_cost,
                    'sell_price': price_result.sell_price,
                    'margin_pct': price_result.margin_pct,
                    'options': {
                        'multicolor': self.multicolor_var.get(),
                        'abrasive': self.abrasive_var.get(),
                        'rush': self.rush_var.get()
                    },
                    'config': {
                        'printer_power': config['printer_power'],
                        'energy_price': config['energy_price'],
                        'labour_cost': config['labour_cost'],
                        'monitoring_pct': config['monitoring_pct'] * 100,  # Convert back to percentage
                        'maintenance_cost': config['maintenance_cost'],
                        'overhead_year': config['overhead_year'],
                        'annual_hours': config['annual_hours'],
                        'markup_material': config['markup_material'] * 100,  # Convert to percentage
                        'markup_variable': config['markup_variable'] * 100,  # Convert to percentage
                        'spoed_surcharge': config['spoed_surcharge'] * 100,  # Convert to percentage
                        'abrasive_surcharge': config['abrasive_surcharge'],
                        'color_fee_min': config['color_fee_min'],
                        'color_fee_max': config['color_fee_max'],
                        'auto_time_per_gram': config['auto_time_per_gram']
                    },
                    'auto_hours_used': self.auto_hours_var.get()
                }
                
                self.data_manager.log_calculation_simple(log_data)
                
            except Exception as e:
                # Silent fail - logboek is niet kritisch
                print(f"Waarschuwing: Kon niet naar logboek schrijven: {e}")
            
            # === STATUS FEEDBACK ===
            # Provide immediate user feedback over successful calculation
            self.status_label.configure(
                text=f"✅ Berekening voltooid - Marge: {price_result.margin_pct:.1f}% | "
                     f"Break-even: {format_euro(price_result.breakdown.total_cost)}"
            )
            
        except Exception as e:
            # === ERROR HANDLING ===
            # Catch-all voor unexpected business logic errors
            messagebox.showerror(
                "Berekeningsfout", 
                f"Er is een onverwachte fout opgetreden:\n{str(e)}\n\n"
                f"Controleer uw invoer en probeer opnieuw."
            )
            # Update status bar met error indication
            self.status_label.configure(text="❌ Fout bij berekening - controleer invoer")

    def save_config(self) -> None:
        """Persisteer huidige configuratie naar user settings bestand.
        
        Configuration Persistence Strategy:
        ----------------------------------
        1. **Input Validation**: Comprehensive validation van alle config waarden
        2. **Type Conversion**: String GUI input → Float business values  
        3. **Business Rules**: Enforcement van positive values en reasonable ranges
        4. **File Persistence**: JSON storage via config.user_config module
        5. **User Feedback**: Success/error messaging met actionable guidance
        
        Validation Pipeline:
        -------------------
        - Type checking (string → float conversion)
        - Range validation (positive values only)  
        - Business rule enforcement (reasonable parameter ranges)
        - Error aggregation (collect alle validation errors)
        
        Data Integrity:
        --------------
        Validates alle parameters voor save operation om corrupt config files
        te voorkomen. Partial saves worden prevented - either alle parameters
        zijn valid of geen save operation.
        
        User Experience:
        ---------------
        - Clear success confirmation met next steps guidance
        - Detailed error messages bij validation failures
        - Status bar updates voor immediate feedback
        - Professional messaging tone
        
        Example:
        -------
            >>> gui = H2DCalculatorGUI()
            >>> gui.config_vars['printer_power'].set("1.2")  
            >>> gui.save_config()  # Validates and saves all config
        """
        try:
            # === INPUT VALIDATION PIPELINE ===
            config_values: Dict[str, str] = {}
            validation_errors: List[str] = []
            
            # Validate alle configuration parameters
            for key, var in self.config_vars.items():
                try:
                    # Convert string input naar numeric value  
                    value = float(var.get())
                    
                    # Business rule: Alle parameters moeten positive zijn
                    if value < 0:
                        validation_errors.append(f"{key}: Waarde kan niet negatief zijn")
                        continue
                    
                    # Store als string voor consistency met config system
                    config_values[key] = str(value)
                    
                except ValueError:
                    validation_errors.append(f"{key}: Ongeldige numerieke waarde")
            
            # === VALIDATION ERROR HANDLING ===
            if validation_errors:
                error_message = "Configuratie bevat ongeldige waarden:\n\n" + "\n".join(validation_errors)
                messagebox.showerror("Configuratie Fout", error_message)
                return
                    
            # === PERSISTENCE OPERATION ===
            # Save validated configuration naar persistent storage
            save_user_config(config_values)
            
            # === SUCCESS FEEDBACK ===
            # Professional user confirmation met next steps guidance
            messagebox.showinfo(
                "Configuratie Opgeslagen", 
                "Configuratie succesvol opgeslagen!\n\n"
                "De nieuwe waarden worden gebruikt voor alle volgende berekeningen.\n"
                "Herstart niet vereist - wijzigingen zijn direct actief."
            )
            
            # Update status bar met success indication
            self.status_label.configure(
                text="✅ Configuratie opgeslagen - nieuwe waarden direct actief"
            )
            
        except Exception as e:
            # === PERSISTENCE ERROR HANDLING ===
            # Handle file system errors, permission issues, etc.
            messagebox.showerror(
                "Opslag Fout", 
                f"Kon configuratie niet opslaan:\n{str(e)}\n\n"
                f"Controleer bestand permissions en probeer opnieuw."
            )
            self.status_label.configure(text="❌ Configuratie opslag gefaald")

    def reset_form(self):
        """Reset alle invoervelden"""
        self.weight_var.set("")
        self.material_var.set("PLA Basic")
        self.hours_var.set("")
        self.auto_hours_var.set(True)
        self.multicolor_var.set(False)
        self.abrasive_var.set(False)
        self.rush_var.set(False)
        
        # Clear resultaten
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
            
        self.result_data = {}
        self.status_label.configure(text="Formulier gereset - klaar voor nieuwe berekening")
        self.toggle_hours_entry()
        
    def reset_config(self):
        """Reset configuratie naar standaard waarden"""
        if messagebox.askyesno("Bevestiging", "Weet je zeker dat je alle waarden wilt resetten naar standaard?"):
            # Reset naar standaard waarden
            self.config_vars['printer_power'].set("1.05")
            self.config_vars['energy_price'].set("0.30")
            self.config_vars['labour_cost'].set("23.50")
            self.config_vars['monitoring_pct'].set("10")
            self.config_vars['maintenance_cost'].set("0.0765")
            self.config_vars['overhead_year'].set("6669")
            self.config_vars['annual_hours'].set("2000")
            self.config_vars['markup_material'].set("200")
            self.config_vars['markup_variable'].set("150")
            self.config_vars['spoed_surcharge'].set("25")
            self.config_vars['abrasive_surcharge'].set("0.50")
            self.config_vars['color_fee_min'].set("15")
            self.config_vars['color_fee_max'].set("30")
            self.config_vars['auto_time_per_gram'].set("0.04")
            
            messagebox.showinfo("Gereset", "Alle waarden zijn gereset naar standaard")
            self.status_label.configure(text="🔄 Configuratie gereset naar standaard")
            
    def get_config_values(self):
        """Haal huidige configuratie waarden op"""
        return {
            'printer_power': float(self.config_vars['printer_power'].get()),
            'energy_price': float(self.config_vars['energy_price'].get()),
            'labour_cost': float(self.config_vars['labour_cost'].get()),
            'monitoring_pct': float(self.config_vars['monitoring_pct'].get()) / 100,  # Convert percentage
            'maintenance_cost': float(self.config_vars['maintenance_cost'].get()),
            'overhead_year': float(self.config_vars['overhead_year'].get()),
            'annual_hours': float(self.config_vars['annual_hours'].get()),
            'markup_material': float(self.config_vars['markup_material'].get()) / 100,  # Convert to factor
            'markup_variable': float(self.config_vars['markup_variable'].get()) / 100,  # Convert to factor
            'spoed_surcharge': float(self.config_vars['spoed_surcharge'].get()) / 100,  # Convert to rate
            'abrasive_surcharge': float(self.config_vars['abrasive_surcharge'].get()),
            'color_fee_min': float(self.config_vars['color_fee_min'].get()),
            'color_fee_max': float(self.config_vars['color_fee_max'].get()),
            'auto_time_per_gram': float(self.config_vars['auto_time_per_gram'].get())
        }
        
    def calculate_costs_with_config(self, weight_g: float, material_name: str, 
                                   print_hours: float, abrasive: bool) -> CostBreakdown:
        """Bereken kosten met GUI configuratie in plaats van hardcoded config.
        
        Deze methode gebruikt de configuratie waarden uit de GUI tabs in plaats
        van de static config.py waarden. Dit maakt real-time aanpassingen mogelijk.
        
        Parameters:
        ----------
        weight_g : float
            Gewicht van de print in gram
        material_name : str
            Naam van het materiaal
        print_hours : float
            Print tijd in uren
        abrasive : bool
            Of het materiaal abrasief is
            
        Returns:
        -------
        CostBreakdown
            Kostenverdeling met GUI configuratie waarden
        """
        # Haal configuratie waarden op
        config = self.get_config_values()
        
        # Bereken materiaalkosten
        price_per_gram = get_price(material_name)
        material_cost = price_per_gram * weight_g
        
        # Bereken variabele kosten per uur met GUI config
        energy_cost_per_hour = config['printer_power'] * config['energy_price']
        monitoring_cost_per_hour = config['labour_cost'] * config['monitoring_pct']  # Alleen monitoring percentage!
        overhead_cost_per_hour = config['overhead_year'] / config['annual_hours']
        
        # Variabele kosten per uur (zoals in de werkende backup)
        variable_cost_per_hour = (
            energy_cost_per_hour + 
            config['maintenance_cost'] + 
            monitoring_cost_per_hour + 
            overhead_cost_per_hour
        )
        
        variable_cost = variable_cost_per_hour * print_hours
        
        # Abrasief toeslag
        surcharge_abrasive = config['abrasive_surcharge'] * print_hours if abrasive else 0.0
        
        # Totaal
        total_cost = material_cost + variable_cost + surcharge_abrasive
        
        return CostBreakdown(
            material_cost=material_cost,
            variable_cost=variable_cost,
            surcharge_abrasive=surcharge_abrasive,
            total_cost=total_cost
        )
    
    def calculate_sell_price_with_config(self, weight_g: float, material_name: str,
                                        print_hours: float, abrasive: bool,
                                        multicolor: bool, spoed: bool) -> PriceResult:
        """Bereken verkoopprijs met GUI configuratie waarden.
        
        Deze methode past de pricing strategie toe met de configureerbare
        markup percentages en toeslagen uit de GUI settings.
        
        Parameters:
        ----------
        weight_g : float
            Gewicht van de print in gram
        material_name : str
            Naam van het materiaal
        print_hours : float
            Print tijd in uren
        abrasive : bool
            Of het materiaal abrasief is
        multicolor : bool
            Multi-kleur print
        spoed : bool
            Spoedopdracht
            
        Returns:
        -------
        PriceResult
            Pricing resultaat met marge berekening
        """
        # Bereken kosten met GUI config
        breakdown = self.calculate_costs_with_config(
            weight_g, material_name, print_hours, abrasive
        )
        
        # Haal configuratie waarden op
        config = self.get_config_values()
        
        # Basis verkoopprijs met configureerbare markup
        cost_material = breakdown.material_cost
        cost_variable = breakdown.variable_cost + breakdown.surcharge_abrasive
        
        sell_price = (
            (cost_material * (1 + config['markup_material'])) + 
            (cost_variable * (1 + config['markup_variable']))
        )
        
        # Multicolor toeslag
        if multicolor:
            setup_fee = (config['color_fee_min'] + config['color_fee_max']) / 2
            sell_price += setup_fee
        
        # Spoedtoeslag
        if spoed:
            sell_price *= (1 + config['spoed_surcharge'])
        
        # Marge berekening
        if breakdown.total_cost > 0:
            margin_pct = (sell_price - breakdown.total_cost) / breakdown.total_cost * 100
        else:
            margin_pct = 0.0
            
        return PriceResult(
            breakdown=breakdown,
            sell_price=sell_price,
            margin_pct=margin_pct
        )
    
    def update_results(self, costs: CostBreakdown, price_result: PriceResult, 
                      weight: float, material_name: str) -> None:
        """Update de resultaten treeview met berekende waarden.
        
        Formatteert alle kosten en prijzen voor professionele presentatie
        in de GUI met duidelijke categorieën en totalen.
        
        Parameters:
        ----------
        costs : CostBreakdown
            Kostenverdeling object
        price_result : PriceResult
            Pricing resultaat met verkoopprijs
        weight : float
            Gewicht voor display
        material_name : str
            Materiaal naam voor display
        """
        # Clear bestaande resultaten
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # Voeg nieuwe resultaten toe
        self.result_tree.insert('', 'end', values=('📦 Gewicht', f'{weight:.1f} gram'))
        self.result_tree.insert('', 'end', values=('🎨 Materiaal', material_name))
        self.result_tree.insert('', 'end', values=('', ''))  # Separator
        
        # Kosten breakdown
        self.result_tree.insert('', 'end', values=('Materiaalkosten', format_euro(costs.material_cost)))
        self.result_tree.insert('', 'end', values=('Variabele kosten', format_euro(costs.variable_cost)))
        
        if costs.surcharge_abrasive > 0:
            self.result_tree.insert('', 'end', values=('Abrasief toeslag', format_euro(costs.surcharge_abrasive)))
            
        self.result_tree.insert('', 'end', values=('', ''))  # Separator
        self.result_tree.insert('', 'end', values=('💰 Totale kosten', format_euro(costs.total_cost)))
        self.result_tree.insert('', 'end', values=('', ''))  # Separator
        
        # Verkoopprijs en marge
        self.result_tree.insert('', 'end', values=('📈 Verkoopprijs', format_euro(price_result.sell_price)))
        self.result_tree.insert('', 'end', values=('📊 Winstmarge', f'{price_result.margin_pct:.1f}%'))
        self.result_tree.insert('', 'end', values=('💵 Winst bedrag', format_euro(price_result.sell_price - costs.total_cost)))
        
        # Bewaar voor export
        self.result_data = {
            'weight': weight,
            'material': material_name,
            'material_cost': costs.material_cost,
            'variable_cost': costs.variable_cost,
            'surcharge_abrasive': costs.surcharge_abrasive,
            'total_cost': costs.total_cost,
            'sell_price': price_result.sell_price,
            'margin_pct': price_result.margin_pct,
            'profit_amount': price_result.sell_price - costs.total_cost
        }
    
    def export_csv(self) -> None:
        """Exporteer berekening naar CSV bestand EN master_calculations.csv.
        
        Deze functie wordt alleen aangeroepen wanneer de gebruiker bewust
        op de Export knop drukt. Exporteert naar:
        1. Een specifiek bestand gekozen door gebruiker
        2. Master_calculations.csv voor centrale database
        """
        if not self.result_data:
            messagebox.showwarning("Geen data", "Voer eerst een berekening uit voordat je exporteert.")
            return
            
        # File dialog voor save locatie
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"h2d_calculatie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                # Maak calc_data voor DataManager export (naar master)
                calc_data = {
                    'weight': self.result_data['weight'],
                    'material': self.result_data['material'],
                    'material_cost': self.result_data['material_cost'],
                    'variable_cost': self.result_data['variable_cost'],
                    'total_cost': self.result_data['total_cost'],
                    'sell_price': self.result_data['sell_price'],
                    'margin_pct': self.result_data['margin_pct'],
                    'options': {
                        'multicolor': self.multicolor_var.get(),
                        'abrasive': self.abrasive_var.get(),
                        'rush': self.rush_var.get()
                    },
                    'print_hours': float(self.hours_var.get() or 0)
                }
                
                # Export naar master_calculations.csv via DataManager
                export_path = self.data_manager.export_calculation(calc_data)
                
                # Ook exporteren naar user-selected file
                export_data = {
                    'weight': self.result_data['weight'],
                    'material': self.result_data['material'],
                    'costs': CostBreakdown(
                        material_cost=self.result_data['material_cost'],
                        variable_cost=self.result_data['variable_cost'],
                        surcharge_abrasive=self.result_data.get('surcharge_abrasive', 0),
                        total_cost=self.result_data['total_cost']
                    ),
                    'price_result': PriceResult(
                        breakdown=CostBreakdown(
                            material_cost=self.result_data['material_cost'],
                            variable_cost=self.result_data['variable_cost'],
                            surcharge_abrasive=self.result_data.get('surcharge_abrasive', 0),
                            total_cost=self.result_data['total_cost']
                        ),
                        sell_price=self.result_data['sell_price'],
                        margin_pct=self.result_data['margin_pct']
                    ),
                    'timestamp': datetime.now(),
                    'print_hours': float(self.hours_var.get() or 0)
                }
                
                # Gebruik de juiste export functie voor user file
                export_calculation_csv(export_data, filename)
                
                messagebox.showinfo(
                    "Export Succesvol", 
                    f"Berekening geëxporteerd naar:\n"
                    f"• {filename}\n"
                    f"• {export_path} (master database)"
                )
                self.status_label.configure(text="✅ CSV export succesvol (user file + master database)")
                
            except Exception as e:
                messagebox.showerror("Export Fout", f"Kon bestand niet opslaan:\n{str(e)}")
                self.status_label.configure(text="❌ CSV export mislukt")
    
    def copy_to_clipboard(self) -> None:
        """Kopieer berekening naar klembord.
        
        Formatteert alle berekende waarden als tekst en kopieert
        naar systeem klembord voor paste in andere applicaties.
        """
        if not self.result_data:
            messagebox.showwarning("Geen data", "Voer eerst een berekening uit voordat je kopieert.")
            return
            
        # Format data voor klembord
        clipboard_text = f"""H2D Prijs Calculator - Berekening
=====================================
Datum/Tijd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Gewicht: {self.result_data['weight']:.1f} gram
Materiaal: {self.result_data['material']}

Kostenverdeling:
- Materiaalkosten: {format_euro(self.result_data['material_cost'])}
- Variabele kosten: {format_euro(self.result_data['variable_cost'])}"""

        if self.result_data['surcharge_abrasive'] > 0:
            clipboard_text += f"\n- Abrasief toeslag: {format_euro(self.result_data['surcharge_abrasive'])}"
            
        clipboard_text += f"""
- Totale kosten: {format_euro(self.result_data['total_cost'])}

Verkoopprijs: {format_euro(self.result_data['sell_price'])}
Winstmarge: {self.result_data['margin_pct']:.1f}%
Winst bedrag: {format_euro(self.result_data['profit_amount'])}
====================================="""
        
        try:
            pyperclip.copy(clipboard_text)
            messagebox.showinfo("Gekopieerd", "Berekening is gekopieerd naar het klembord!")
            self.status_label.configure(text="📋 Gekopieerd naar klembord")
        except Exception as e:
            messagebox.showerror("Kopieer Fout", f"Kon niet naar klembord kopiëren:\n{str(e)}")
            self.status_label.configure(text="❌ Kopiëren mislukt")
        
    # === PRODUCT MANAGEMENT METHODS ===
    
    def save_as_product(self) -> None:
        """Sla huidige berekening op als product in database."""
        if not self.result_data:
            messagebox.showwarning("Geen berekening", "Voer eerst een berekening uit voordat je een product opslaat.")
            return
            
        name = self.product_name_var.get().strip()
        if not name:
            messagebox.showerror("Naam vereist", "Voer een productnaam in.")
            return
            
        description = self.product_desc_text.get("1.0", "end-1c").strip()
        
        try:
            # Maak Product object van huidige berekening
            product = Product(
                name=name,
                description=description,
                weight_g=self.result_data['weight'],
                material=self.result_data['material'],
                print_hours=float(self.hours_var.get() or 0),
                multicolor=self.multicolor_var.get(),
                abrasive=self.abrasive_var.get(),
                rush=self.rush_var.get(),
                material_cost=self.result_data['material_cost'],
                variable_cost=self.result_data['variable_cost'],
                total_cost=self.result_data['total_cost'],
                sell_price=self.result_data['sell_price'],
                margin_pct=self.result_data['margin_pct']
            )
            
            # Sla op via ProductManager
            saved = self.product_manager.create(product)
            
            # Export product naar master_calculations.csv
            calc_data = {
                'weight': saved.weight_g,
                'material': saved.material,
                'material_cost': saved.material_cost,
                'variable_cost': saved.variable_cost,
                'total_cost': saved.total_cost,
                'sell_price': saved.sell_price,
                'margin_pct': saved.margin_pct,
                'options': {
                    'multicolor': saved.multicolor,
                    'abrasive': saved.abrasive,
                    'rush': saved.rush
                },
                'print_hours': saved.print_hours,
                'product_name': saved.name,
                'product_id': saved.product_id,
                'is_product': True
            }
            
            # Export naar master via DataManager
            self.data_manager.export_calculation(calc_data)
            
            messagebox.showinfo("Product Opgeslagen", f"Product '{saved.name}' is opgeslagen met ID: {saved.product_id}")
            self.status_label.configure(text=f"✅ Product opgeslagen: {saved.product_id} (ook in master database)")
            
            # Clear inputs
            self.product_name_var.set("")
            self.product_desc_text.delete("1.0", "end")
            
            # Refresh lijst
            self.refresh_product_list()
            self.update_product_stats()
            
        except Exception as e:
            messagebox.showerror("Opslag Fout", f"Kon product niet opslaan:\n{str(e)}")
            
    def search_products(self) -> None:
        """Zoek producten op naam of beschrijving."""
        query = self.search_var.get().strip()
        if not query:
            self.refresh_product_list()
            return
            
        products = self.product_manager.search(query)
        self._update_product_tree(products)
        self.status_label.configure(text=f"🔍 {len(products)} producten gevonden voor '{query}'")
        
    def filter_products(self) -> None:
        """Filter producten op materiaal type."""
        material = self.filter_material_var.get()
        
        if material == "Alle":
            products = self.product_manager.list_all()
        else:
            products = self.product_manager.filter_by_material(material)
            
        self._update_product_tree(products)
        self.status_label.configure(text=f"🏷️ {len(products)} producten met materiaal '{material}'")
        
    def load_selected_product(self, event=None) -> None:
        """Laad geselecteerd product in calculator."""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Geen selectie", "Selecteer eerst een product om te laden.")
            return
            
        # Haal product ID uit treeview
        item = self.product_tree.item(selection[0])
        product_id = item['values'][0]
        
        # Laad product via manager
        product = self.product_manager.get_by_id(product_id)
        if not product:
            messagebox.showerror("Product niet gevonden", f"Product {product_id} bestaat niet meer.")
            return
            
        # Vul calculator velden met product data
        self.weight_var.set(str(product.weight_g))
        self.material_var.set(product.material)
        self.hours_var.set(str(product.print_hours))
        self.auto_hours_var.set(False)  # Manual mode voor geladen product
        self.multicolor_var.set(product.multicolor)
        self.abrasive_var.set(product.abrasive)
        self.rush_var.set(product.rush)
        
        # Trigger herberekening
        self.calculate_price()
        
        # Switch naar calculator tab
        self.notebook.select(0)
        
        self.status_label.configure(text=f"📂 Product geladen: {product.name}")
        
    def delete_selected_product(self) -> None:
        """Verwijder geselecteerd product uit database."""
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Geen selectie", "Selecteer eerst een product om te verwijderen.")
            return
            
        # Bevestiging vragen
        if not messagebox.askyesno("Bevestig verwijdering", "Weet je zeker dat je dit product wilt verwijderen?"):
            return
            
        # Haal product ID uit treeview
        item = self.product_tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        # Verwijder via manager
        if self.product_manager.delete(product_id):
            messagebox.showinfo("Product Verwijderd", f"Product '{product_name}' is verwijderd.")
            self.refresh_product_list()
            self.update_product_stats()
            self.status_label.configure(text=f"🗑️ Product verwijderd: {product_name}")
        else:
            messagebox.showerror("Verwijder Fout", "Kon product niet verwijderen.")
            
    def refresh_product_list(self) -> None:
        """Vernieuw de product lijst in treeview."""
        products = self.product_manager.list_all()
        self._update_product_tree(products)
        
    def export_all_products(self) -> None:
        """Exporteer alle producten naar CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"h2d_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                self.product_manager.export_csv(filename)
                messagebox.showinfo("Export Succesvol", f"Producten geëxporteerd naar:\n{filename}")
                self.status_label.configure(text="✅ Product export succesvol")
            except Exception as e:
                messagebox.showerror("Export Fout", f"Kon producten niet exporteren:\n{str(e)}")
                
    def update_product_stats(self) -> None:
        """Update statistieken weergave."""
        try:
            stats = self.product_manager.get_statistics()
        
            # Format statistieken tekst
            stats_text = f"""Totaal producten: {stats['total_products']}
Populairste: {stats.get('most_popular_product', 'N/A')}
Gem. gewicht: {stats['avg_weight']:.1f}g
Gem. prijs: €{stats['avg_price']:.2f}
Gem. marge: {stats['avg_margin']:.1f}%
Totale orders: {stats['total_orders']}"""
            
            # Update text widget
            self.stats_text.configure(state='normal')
            self.stats_text.delete('1.0', 'end')
            self.stats_text.insert('1.0', stats_text)
            self.stats_text.configure(state='disabled')
            
        except Exception as e:
            # Silent fail voor stats update
            print(f"Waarschuwing: Kon statistieken niet updaten: {e}")
        
    def _update_product_tree(self, products: List[Product]) -> None:
        """Helper om product treeview te updaten."""
        # Clear huidige items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        # Voeg producten toe
        for product in products:
            self.product_tree.insert('', 'end', values=(
                product.product_id,
                product.name,
                product.material,
                f"{product.weight_g:.1f}",
                format_euro(product.sell_price),
                f"{product.margin_pct:.1f}%",
                product.actual_orders
            ))
    
    def show_product_charts(self) -> None:
        """Open nieuw venster met scrollbare product grafieken.
        
        Deze functie creëert een apart venster met uitgebreide
        visualisaties voor product analyses.
        """
        try:
            # Check of ProductCharts beschikbaar is
            from ..products import ProductCharts
            
            # Maak nieuw top-level venster
            charts_window = tk.Toplevel(self.root)
            charts_window.title("📊 Product Grafieken - H2D Calculator")
            charts_window.geometry("1000x800")
            
            # Minimum grootte voor leesbaarheid
            charts_window.minsize(800, 600)
            
            # Icon als hoofdvenster
            if hasattr(self, 'icon_path') and os.path.exists(self.icon_path):
                charts_window.iconbitmap(self.icon_path)
            
            # Header frame
            header_frame = tk.Frame(charts_window, bg=self.colors['primary'], height=50)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            # Header titel
            title_label = tk.Label(
                header_frame,
                text="📊 Product Analyse Grafieken",
                font=("Arial", 16, "bold"),
                bg=self.colors['primary'],
                fg='white'
            )
            title_label.pack(pady=12)
            
            # Instructie label
            info_frame = tk.Frame(charts_window, bg=self.colors['bg'])
            info_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(
                info_frame,
                text="Scroll omlaag om alle 6 grafieken te bekijken • Gebaseerd op data uit master_calculations.csv",
                font=("Arial", 10, "italic"),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack()
            
            # Charts frame
            charts_frame = tk.Frame(charts_window, bg=self.colors['bg'])
            charts_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
            
            # Creëer ProductCharts instance
            product_charts = ProductCharts(
                parent=charts_frame,
                product_manager=self.product_manager,
                colors=self.colors
            )
            
            # Refresh knop onderaan
            button_frame = tk.Frame(charts_window, bg=self.colors['bg'])
            button_frame.pack(fill='x', pady=10)
            
            refresh_btn = tk.Button(
                button_frame,
                text="🔄 Vernieuw Grafieken",
                command=product_charts.refresh_charts,
                font=("Arial", 11, "bold"),
                bg=self.colors['primary'],
                fg='white',
                padx=20,
                pady=8,
                cursor='hand2'
            )
            refresh_btn.pack()
            
            # Status update
            self.status_label.configure(text="📊 Product grafieken geopend")
            
        except ImportError:
            messagebox.showerror(
                "Module niet gevonden",
                "De grafieken module is niet beschikbaar.\n\n"
                "Installeer matplotlib met:\n"
                "pip install matplotlib"
            )
        except Exception as e:
            messagebox.showerror(
                "Grafiek Fout",
                f"Kon grafieken niet laden:\n{str(e)}"
            )

    def run(self) -> None:
        """Start de GUI event loop.
        
        Dit is de main entry point voor de applicatie. Start tkinter's
        mainloop() voor event processing en window management.
        """
        self.root.mainloop()


def main():
    """Main entry point voor de H2D Calculator GUI applicatie.
    
    Creëert een instantie van de calculator GUI en start de event loop.
    Vangt exceptions op voor graceful error handling bij startup problemen.
    """
    try:
        # Create en start GUI
        app = H2DCalculatorGUI()
        app.run()
    except Exception as e:
        # Fallback error handling voor startup problemen
        import traceback
        error_msg = f"Fout bij opstarten van H2D Calculator:\n\n{str(e)}\n\n{traceback.format_exc()}"
        
        # Probeer tkinter messagebox, anders print naar console
        try:
            import tkinter.messagebox
            tkinter.messagebox.showerror("Startup Fout", error_msg)
        except:
            print(error_msg)
            sys.exit(1)


if __name__ == "__main__":
    """Entry point voor directe module uitvoering.
    
    Enables running GUI via: python -m interface.gui
    Professional pattern voor Python module executability.
    """
    main() 