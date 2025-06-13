"""
Materials Database Module - H2D Price Calculator
===============================================

Dit module beheert de materiaal database voor 3D printing services.
Het bevat een curated selectie van populaire filament types met 
actuele bulk prijzen en eigenschappen.

Database Design:
---------------
- In-memory dictionary voor snelle lookups (O(1))
- Immutable Material dataclass voor data integrity
- Bulk pricing (≥6 rollen) voor professionele marges
- Type-safe interfaces met Optional returns

Materiaal Categorieën:
---------------------
- Basis materialen: PLA, PETG, ABS (€13.99-€19.99/kg)
- Specialty materialen: ASA, PC (€24.99-€49.99/kg)  
- Composiet materialen: CF, GF variants (€29.99-€79.99/kg)

Gebruik:
-------
    >>> material = get_material("PLA Basic")
    >>> if material:
    ...     cost = material.price_per_gram * 100  # 100g print
    ...     print(f"Materiaalkosten: €{cost:.2f}")
    
    >>> try:
    ...     price = get_price("PETG-CF")
    ...     print(f"PETG-CF: €{price:.3f}/gram")
    ... except KeyError as e:
    ...     print(f"Materiaal niet gevonden: {e}")

Database Updates:
----------------
Nieuwe materialen toevoegen in _MATERIALS dictionary:
    "TPU Flex": Material("TPU Flex", 34.99),

Auteur: H2D Systems  
Versie: 1.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Material:
    """Immutable model voor 3D printing filament materiaal.
    
    Deze dataclass representeert een specifiek filament type met
    alle relevante eigenschappen voor kostprijsberekening.
    
    Attributes:
    ----------
    name : str
        Volledige materiaalnaam zoals bekend bij leveranciers
    price_per_kg : float
        Bulkprijs per kilogram in euro (≥6 rollen basis)
        
    Properties:
    ----------
    price_per_gram : float
        Automatisch berekende prijs per gram voor precisie
        
    Example:
    -------
        >>> pla = Material("PLA Basic", 13.99)
        >>> print(f"{pla.name}: €{pla.price_per_kg}/kg")
        PLA Basic: €13.99/kg
        >>> cost_100g = pla.price_per_gram * 100
        >>> print(f"100g kost: €{cost_100g:.2f}")
        100g kost: €1.40
        
    Note:
    ----
    frozen=True maakt deze class immutable, wat thread-safety
    garandeert en accidentele modificaties voorkomt.
    """

    name: str
    price_per_kg: float  # € per kilogram

    @property
    def price_per_gram(self) -> float:
        """Prijs per gram (automatisch berekend van kg prijs).
        
        Returns:
        -------
        float
            Prijs per gram in euro (price_per_kg / 1000)
            
        Example:
        -------
            >>> material = Material("PLA Basic", 13.99)
            >>> print(f"Per gram: €{material.price_per_gram:.3f}")
            Per gram: €0.014
        """
        return self.price_per_kg / 1000

    def calculate_cost(self, weight_grams: float) -> float:
        """Bereken materiaalkosten voor gegeven gewicht.
        
        Parameters:
        ----------
        weight_grams : float
            Gewicht in gram
            
        Returns:
        -------
        float
            Totale materiaalkosten in euro
            
        Example:
        -------
            >>> pla = Material("PLA Basic", 13.99)
            >>> cost = pla.calculate_cost(250.0)
            >>> print(f"250g PLA: €{cost:.2f}")
            250g PLA: €3.50
        """
        return self.price_per_gram * weight_grams

    def __str__(self) -> str:
        """String representatie voor logging en debugging."""
        return f"{self.name} – €{self.price_per_kg}/kg (€{self.price_per_gram:.3f}/g)"

    def __repr__(self) -> str:
        """Unambiguous representatie voor development."""
        return f"Material('{self.name}', {self.price_per_kg})"


# === MATERIAAL DATABASE ===
# Curated selectie van populaire 3D printing materialen
# Prijzen gebaseerd op bulk inkoop (≥6 rollen) van december 2024
# Dekking: ~90% van typische 3D printing behoeften

_MATERIALS: Dict[str, Material] = {
    # BASIS MATERIALEN - Entry level, meest gebruikt
    "PLA Basic": Material("PLA Basic", 13.99),       # Beginner friendly, goede oppervlaktekwaliteit
    "PETG Basic": Material("PETG Basic", 19.99),     # Sterker dan PLA, chemisch bestendig
    "ABS": Material("ABS", 19.99),                   # Traditioneel engineering plastic, hittebestendig
    
    # SPECIALTY MATERIALEN - Specifieke eigenschappen  
    "PLA Matte": Material("PLA Matte", 19.99),       # Esthetisch upgrade, geen layer lines
    "ASA": Material("ASA", 24.99),                   # UV-bestendig ABS alternatief voor buiten
    "PC": Material("PC", 49.99),                     # High-temp engineering (130°C+), transparant
    
    # COMPOSIET MATERIALEN - Versterkte eigenschappen
    "PLA-CF": Material("PLA-CF", 29.99),             # Carbon fiber versterkt PLA, stijf en licht
    "PETG-CF": Material("PETG-CF", 36.29),           # Carbon fiber PETG, balans stijfheid/taaiheid  
    "PETG-GF": Material("PETG-GF", 39.99),           # Glass fiber PETG, hoge stijfheid
    "PA-CF": Material("PA-CF", 79.99),               # Premium nylon composite, ultimate strength
}


def list_materials() -> Dict[str, Material]:
    """Geef volledige materiaal database als dictionary.
    
    Retourneert een kopie om externe modificaties te voorkomen.
    Geschikt voor iteratie, GUI populatie en export functies.
    
    Returns:
    -------
    Dict[str, Material]
        Dictionary met materiaalnaam als key, Material object als value
        
    Example:
    -------
        >>> materials = list_materials()
        >>> for name, material in materials.items():
        ...     print(f"{name}: €{material.price_per_kg}/kg")
        PLA Basic: €13.99/kg
        PETG Basic: €19.99/kg
        ...
        
        >>> sorted_by_price = sorted(materials.items(), 
        ...                         key=lambda x: x[1].price_per_kg)
        >>> cheapest = sorted_by_price[0]
        >>> print(f"Goedkoopste: {cheapest[0]} (€{cheapest[1].price_per_kg}/kg)")
        
    Note:
    ----
    Dit retourneert een shallow copy van de database dictionary.
    De Material objecten zelf zijn immutable, dus modificaties 
    aan de dictionary raken de originele database niet.
    """
    return _MATERIALS.copy()


def get_material(material_name: str) -> Optional[Material]:
    """Veilige lookup van materiaal object met null-safety.
    
    Deze functie biedt een null-safe manier om materialen op te zoeken
    zonder exceptions. Automatische whitespace trimming voorkomt
    typische input fouten.
    
    Parameters:
    ----------
    material_name : str
        Naam van het materiaal (case-sensitive, whitespace wordt getrimd)
        
    Returns:
    -------
    Optional[Material]
        Material object indien gevonden, None indien onbekend materiaal
        
    Examples:
    --------
    Safe pattern met None checking:
    
        >>> material = get_material("PLA Basic")
        >>> if material:
        ...     cost = material.calculate_cost(100.0)
        ...     print(f"100g kost: €{cost:.2f}")
        ... else:
        ...     print("Materiaal niet gevonden")
        100g kost: €1.40
        
    Walrus operator (Python 3.8+):
    
        >>> if material := get_material("PETG-CF"):
        ...     print(f"Gevonden: {material.name}")
        Gevonden: PETG-CF
        
    Batch validation:
    
        >>> requested = ["PLA Basic", "Unknown", "ABS"]
        >>> available = [name for name in requested if get_material(name)]
        >>> print(f"Beschikbaar: {available}")
        Beschikbaar: ['PLA Basic', 'ABS']
        
    Note:
    ----
    Gebruik deze functie wanneer je wilt omgaan met potentieel 
    ongeldige material namen zonder exceptions te vangen.
    Voor performance-critical code waar je zeker bent van de
    materiaalnaam, gebruik direct get_price().
    """
    return _MATERIALS.get(material_name.strip())


def get_price(material: str) -> float:
    """Directe prijs lookup met exception bij onbekend materiaal.
    
    Snelle prijs lookup voor bekende materialen. Gooit descriptive
    KeyError met alle beschikbare opties bij ongeldige input.
    
    Parameters:
    ----------
    material : str
        Naam van het materiaal (whitespace wordt automatisch getrimd)
        
    Returns:
    -------
    float
        Prijs per gram in euro

    Raises:
    ------
    KeyError
        Als het materiaal niet bestaat in de database.
        Error message bevat lijst van alle beschikbare materialen.
        
    Examples:
    --------
    Normale usage met bekende materialen:
    
        >>> price = get_price("PLA Basic")
        >>> print(f"PLA Basic: €{price:.3f}/gram")
        PLA Basic: €0.014/gram
        
    Error handling voor onbekende materialen:
    
        >>> try:
        ...     price = get_price("Unknown Material")
        ... except KeyError as e:
        ...     print(f"Fout: {e}")
        Fout: Onbekend materiaal: Unknown Material. Beschikbaar: PLA Basic, PETG Basic, ...
        
    Batch processing met error handling:
    
        >>> materials = ["PLA Basic", "Invalid", "PETG-CF"]
        >>> prices = {}
        >>> for mat in materials:
        ...     try:
        ...         prices[mat] = get_price(mat)
        ...     except KeyError:
        ...         print(f"Ongeldig materiaal: {mat}")
        
    Performance tip voor loops:
    
        >>> # Cache voor herhaalde lookups
        >>> material_cache = {name: get_price(name) for name in ["PLA Basic", "PETG Basic"]}
        >>> # Gebruik cache[name] in plaats van get_price(name) in loop
        
    Note:
    ----
    Deze functie is geoptimaliseerd voor performance (directe dictionary lookup).
    Het levert meer gedetailleerde error messages dan standaard KeyError.
    Ideaal voor cost calculation loops waar materiaal bestand verondersteld wordt.
    """
    key = material.strip()
    if key not in _MATERIALS:
        available = ', '.join(sorted(_MATERIALS.keys()))
        raise KeyError(
            f"Onbekend materiaal: {material}. "
            f"Beschikbaar: {available}"
        )
    return _MATERIALS[key].price_per_gram 


def get_materials_by_price_range(min_price: float, max_price: float) -> Dict[str, Material]:
    """Filter materialen op prijsbereik per kilogram.
    
    Parameters:
    ----------
    min_price : float
        Minimum prijs per kg (inclusief)
    max_price : float  
        Maximum prijs per kg (inclusief)
        
    Returns:
    -------
    Dict[str, Material]
        Dictionary met materialen binnen het prijsbereik
        
    Example:
    -------
        >>> budget_materials = get_materials_by_price_range(10.0, 25.0)
        >>> for name, mat in budget_materials.items():
        ...     print(f"{name}: €{mat.price_per_kg}/kg")
    """
    return {
        name: material 
        for name, material in _MATERIALS.items()
        if min_price <= material.price_per_kg <= max_price
    }


def get_cheapest_material() -> Material:
    """Vind het goedkoopste materiaal in de database.
    
    Returns:
    -------
    Material
        Het materiaal met de laagste prijs per kg
        
    Example:
    -------
        >>> cheapest = get_cheapest_material()
        >>> print(f"Goedkoopste optie: {cheapest.name} (€{cheapest.price_per_kg}/kg)")
    """
    return min(_MATERIALS.values(), key=lambda m: m.price_per_kg)


def get_material_count() -> int:
    """Aantal materialen in database.
    
    Returns:
    -------
    int
        Totaal aantal beschikbare materialen
    """
    return len(_MATERIALS) 