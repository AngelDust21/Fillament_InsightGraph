"""
Product Model - H2D Price Calculator
===================================

Dit module definieert het Product datamodel voor de H2D Price Calculator.
Het Product model bevat alle informatie voor een 3D print product inclusief
calculatie parameters, resultaten en analytics tracking.

Design Filosofie:
----------------
- Immutable waar mogelijk (frozen=True) voor data integriteit
- Type hints voor betere IDE support en type safety
- Validatie in __post_init__ voor robuuste data
- Auto-generated IDs voor unieke identificatie
- Analytics tracking voor toekomstige analyses

Gebruik:
-------
    >>> product = Product(
    ...     name="Telefoon Houder",
    ...     description="Universele smartphone houder",
    ...     weight_g=45.5,
    ...     material="PLA Basic",
    ...     print_hours=2.5
    ... )
    >>> print(product.product_id)
    202501280001

Auteur: H2D Systems
Versie: 1.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import json


@dataclass
class Product:
    """3D Print Product met volledige calculatie en tracking informatie.
    
    Deze dataclass representeert een compleet 3D print product met alle
    parameters, berekende waarden en analytics tracking voor populariteit.
    
    Attributes:
    ----------
    # Identificatie
    product_id : str
        Uniek ID in formaat YYYYMMDDXXXX (auto-generated, puur numeriek)
    name : str
        Product naam (verplicht, max 100 karakters)
    description : str
        Product beschrijving (optioneel, max 500 karakters)
    
    # Calculatie Parameters
    weight_g : float
        Gewicht in gram (moet positief zijn)
    material : str
        Materiaal naam uit materials database
    print_hours : float
        Print tijd in uren (auto of manueel)
    
    # Print Opties
    multicolor : bool
        Multi-kleur print (AMS gebruik)
    abrasive : bool
        Abrasief materiaal (CF/GF)
    rush : bool
        Spoedopdracht (<48u)
    
    # Berekende Waarden
    material_cost : float
        Materiaalkosten in euro
    variable_cost : float
        Variabele kosten in euro
    total_cost : float
        Totale kostprijs in euro
    sell_price : float
        Verkoopprijs in euro
    margin_pct : float
        Winstmarge percentage
    
    # Analytics Tracking
    times_loaded : int
        Aantal keer bekeken/geladen
    times_calculated : int
        Aantal keer herberekend
    times_exported : int
        Aantal keer geëxporteerd
    actual_orders : int
        Aantal daadwerkelijke bestellingen
    
    # Timestamps
    created_at : datetime
        Aanmaakdatum (auto)
    updated_at : datetime
        Laatste wijziging (auto)
    last_accessed : datetime
        Laatste keer gebruikt (auto)
    
    # Metadata
    version : int
        Versienummer voor wijzigingen tracking
    tags : list[str]
        Tags voor categorisatie
    custom_fields : Dict[str, Any]
        Flexibele extra velden
    
    Methods:
    -------
    calculate_popularity() -> float
        Bereken populariteit score
    to_dict() -> Dict[str, Any]
        Converteer naar dictionary
    from_dict(data: Dict) -> Product
        Laad vanuit dictionary
    validate() -> bool
        Valideer alle velden
    """
    
    # === IDENTIFICATIE ===
    name: str
    description: str = ""
    product_id: str = field(default="", init=False)
    
    # === CALCULATIE PARAMETERS ===
    weight_g: float = 0.0
    material: str = "PLA Basic"
    print_hours: float = 0.0
    
    # === PRINT OPTIES ===
    multicolor: bool = False
    abrasive: bool = False
    rush: bool = False
    
    # === BEREKENDE WAARDEN ===
    material_cost: float = 0.0
    variable_cost: float = 0.0
    total_cost: float = 0.0
    sell_price: float = 0.0
    margin_pct: float = 0.0
    
    # === ANALYTICS TRACKING ===
    times_loaded: int = 0
    times_calculated: int = 0
    times_exported: int = 0
    actual_orders: int = 0
    
    # === TIMESTAMPS ===
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    
    # === METADATA ===
    version: int = 1
    tags: list[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    # Klasse variabele voor ID generatie
    _id_counter: int = field(default=0, init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Validatie en auto-generatie na initialisatie.
        
        - Genereert uniek product ID
        - Valideert input waarden
        - Zet default timestamps
        """
        # Generate product ID als nog niet gezet
        if not self.product_id:
            self.product_id = self._generate_product_id()
        
        # Valideer inputs
        self._validate_inputs()
        
        # Bereken automatisch print tijd als niet opgegeven
        if self.print_hours == 0.0 and self.weight_g > 0:
            self.print_hours = self.weight_g * 0.04  # Default 0.04u/g
    
    def _generate_product_id(self) -> str:
        """Genereer uniek product ID.
        
        Format: YYYYMMDDXXXX (puur numeriek)
        Bijvoorbeeld: 202501280001
        """
        date_part = datetime.now().strftime("%Y%m%d")
        # In productie: haal counter uit database/file
        Product._id_counter += 1
        counter_part = f"{Product._id_counter:04d}"
        return f"{date_part}{counter_part}"
    
    def _validate_inputs(self) -> None:
        """Valideer alle input waarden.
        
        Raises:
        ------
        ValueError
            Bij ongeldige input waarden
        """
        # Naam validatie
        if not self.name or not self.name.strip():
            raise ValueError("Product naam is verplicht")
        if len(self.name) > 100:
            raise ValueError("Product naam mag max 100 karakters zijn")
        
        # Beschrijving validatie
        if len(self.description) > 500:
            raise ValueError("Beschrijving mag max 500 karakters zijn")
        
        # Gewicht validatie
        if self.weight_g < 0:
            raise ValueError(f"Gewicht moet positief zijn, kreeg: {self.weight_g}")
        
        # Print tijd validatie
        if self.print_hours < 0:
            raise ValueError(f"Print tijd moet positief zijn, kreeg: {self.print_hours}")
        
        # Kosten validatie
        if self.total_cost < 0:
            raise ValueError("Totale kosten kunnen niet negatief zijn")
        if self.sell_price < 0:
            raise ValueError("Verkoopprijs kan niet negatief zijn")
    
    def calculate_popularity(self) -> float:
        """Bereken populariteit score gebaseerd op analytics.
        
        Formule:
        score = (views × 1 + calculations × 2 + exports × 3 + orders × 10) / dagen
        
        Returns:
        -------
        float
            Populariteit score (hoger = populairder)
        """
        # Bereken dagen sinds aanmaak
        days_old = max(1, (datetime.now() - self.created_at).days)
        
        # Gewogen score berekening
        weighted_score = (
            self.times_loaded * 1 +
            self.times_calculated * 2 +
            self.times_exported * 3 +
            self.actual_orders * 10
        )
        
        # Normaliseer voor leeftijd
        return weighted_score / days_old
    
    def update_accessed(self) -> None:
        """Update last_accessed timestamp en increment load counter."""
        self.last_accessed = datetime.now()
        self.times_loaded += 1
    
    def update_calculated(self) -> None:
        """Update voor nieuwe berekening."""
        self.times_calculated += 1
        self.updated_at = datetime.now()
        self.last_accessed = datetime.now()
    
    def update_exported(self) -> None:
        """Update voor export actie."""
        self.times_exported += 1
        self.last_accessed = datetime.now()
    
    def add_order(self, quantity: int = 1) -> None:
        """Registreer een bestelling."""
        self.actual_orders += quantity
        self.last_accessed = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converteer Product naar dictionary voor opslag.
        
        Returns:
        -------
        Dict[str, Any]
            Dictionary representatie van product
        """
        return {
            # Identificatie
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            
            # Parameters
            'weight_g': self.weight_g,
            'material': self.material,
            'print_hours': self.print_hours,
            
            # Opties
            'multicolor': self.multicolor,
            'abrasive': self.abrasive,
            'rush': self.rush,
            
            # Berekende waarden
            'material_cost': self.material_cost,
            'variable_cost': self.variable_cost,
            'total_cost': self.total_cost,
            'sell_price': self.sell_price,
            'margin_pct': self.margin_pct,
            
            # Analytics
            'times_loaded': self.times_loaded,
            'times_calculated': self.times_calculated,
            'times_exported': self.times_exported,
            'actual_orders': self.actual_orders,
            'popularity_score': self.calculate_popularity(),
            
            # Timestamps (ISO format voor compatibiliteit)
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            
            # Metadata
            'version': self.version,
            'tags': self.tags,
            'custom_fields': self.custom_fields
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Maak Product instance vanuit dictionary.
        
        Parameters:
        ----------
        data : Dict[str, Any]
            Dictionary met product data
            
        Returns:
        -------
        Product
            Nieuwe product instance
        """
        # Maak een kopie om originele data niet te wijzigen
        data = data.copy()
        
        # Parse timestamps
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if isinstance(data.get('updated_at'), str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if isinstance(data.get('last_accessed'), str):
            data['last_accessed'] = datetime.fromisoformat(data['last_accessed'])
        
        # Verwijder velden die niet in constructor kunnen
        product_id = data.pop('product_id', None)
        data.pop('popularity_score', None)
        data.pop('_id_counter', None)  # Private field
        
        # Maak instance
        product = cls(**data)
        
        # Zet product_id expliciet na creatie
        if product_id:
            product.product_id = product_id
        
        return product
    
    def __str__(self) -> str:
        """String representatie voor gebruiker."""
        return f"{self.product_id}: {self.name} ({self.material}, {self.weight_g}g)"
    
    def __repr__(self) -> str:
        """Developer representatie."""
        return (f"Product(id='{self.product_id}', name='{self.name}', "
                f"material='{self.material}', weight={self.weight_g}g, "
                f"price=€{self.sell_price:.2f})")


# Voor backwards compatibility en makkelijkere imports
__all__ = ['Product'] 