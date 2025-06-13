"""
Material Properties - H2D Price Calculator
==========================================

Dit module bevat uitgebreide eigenschappen per materiaal type
voor realistische printtijd en slijtage berekeningen.

EDUCATIEF DOEL:
--------------
Laat zien hoe verschillende materialen verschillende:
- Printsnelheden hebben (PLA snel, TPU langzaam)
- Slijtage veroorzaken (CF/GF hoog, PLA laag)
- Nozzle vervangingskosten hebben

Dit maakt de calculator realistischer en leert studenten
over materiaal eigenschappen en hun impact op kosten.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class MaterialProperties:
    """Uitgebreide eigenschappen van een 3D print materiaal.
    
    Attributes:
    ----------
    print_speed_grams_per_hour : float
        Gemiddelde printsnelheid in gram/uur
    nozzle_wear_factor : float
        Slijtage factor (1.0 = normaal, 10.0 = 10x sneller)
    recommended_nozzle : str
        Aanbevolen nozzle type
    nozzle_replacement_cost : float
        Kosten voor nozzle vervanging in euro
    """
    print_speed_grams_per_hour: float
    nozzle_wear_factor: float
    recommended_nozzle: str
    nozzle_replacement_cost: float
    
    @property
    def hours_per_gram(self) -> float:
        """Bereken uren per gram (inverse van speed)."""
        return 1.0 / self.print_speed_grams_per_hour
    
    @property
    def wear_cost_per_hour(self) -> float:
        """Bereken slijtage kosten per uur.
        
        Basis: standaard nozzle duurt 1000 uur
        Met wear factor: levensduur = 1000 / wear_factor
        """
        nozzle_lifetime_hours = 1000.0 / self.nozzle_wear_factor
        return self.nozzle_replacement_cost / nozzle_lifetime_hours


# Realistische materiaal eigenschappen database
MATERIAL_PROPERTIES: Dict[str, MaterialProperties] = {
    # BASIS MATERIALEN
    "PLA Basic": MaterialProperties(
        print_speed_grams_per_hour=30.0,  # Snel en makkelijk
        nozzle_wear_factor=1.0,           # Minimale slijtage
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    "PETG Basic": MaterialProperties(
        print_speed_grams_per_hour=25.0,  # Iets langzamer
        nozzle_wear_factor=1.2,           # Licht verhoogde slijtage
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    "ABS": MaterialProperties(
        print_speed_grams_per_hour=28.0,  # Redelijk snel
        nozzle_wear_factor=1.1,           # Minimale extra slijtage
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    
    # SPECIALTY MATERIALEN
    "PLA Matte": MaterialProperties(
        print_speed_grams_per_hour=28.0,  # Bijna als normaal PLA
        nozzle_wear_factor=1.0,
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    "PLA Silk": MaterialProperties(
        print_speed_grams_per_hour=25.0,  # Langzamer voor kwaliteit
        nozzle_wear_factor=1.0,
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    "PLA Wood": MaterialProperties(
        print_speed_grams_per_hour=20.0,  # Langzaam, verstopt makkelijk
        nozzle_wear_factor=2.0,           # Hout deeltjes = slijtage
        recommended_nozzle="Hardened 0.6mm",
        nozzle_replacement_cost=25.0
    ),
    "ASA": MaterialProperties(
        print_speed_grams_per_hour=26.0,
        nozzle_wear_factor=1.2,
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    "PC": MaterialProperties(
        print_speed_grams_per_hour=20.0,  # Langzaam, hoge temp
        nozzle_wear_factor=1.5,
        recommended_nozzle="Hardened 0.4mm",
        nozzle_replacement_cost=25.0
    ),
    
    # FLEXIBELE MATERIALEN
    "TPU 95A": MaterialProperties(
        print_speed_grams_per_hour=15.0,  # Zeer langzaam!
        nozzle_wear_factor=1.0,
        recommended_nozzle="Brass 0.4mm",
        nozzle_replacement_cost=8.0
    ),
    
    # COMPOSIET MATERIALEN - HOGE SLIJTAGE
    "PLA-CF": MaterialProperties(
        print_speed_grams_per_hour=25.0,
        nozzle_wear_factor=8.0,           # Carbon fiber = hoge slijtage!
        recommended_nozzle="Hardened Steel",
        nozzle_replacement_cost=30.0
    ),
    "PETG-CF": MaterialProperties(
        print_speed_grams_per_hour=22.0,
        nozzle_wear_factor=10.0,          # Nog hoger door PETG temp
        recommended_nozzle="Hardened Steel",
        nozzle_replacement_cost=30.0
    ),
    "PETG-GF": MaterialProperties(
        print_speed_grams_per_hour=20.0,
        nozzle_wear_factor=12.0,          # Glass fiber = extreme slijtage
        recommended_nozzle="Ruby Nozzle",
        nozzle_replacement_cost=90.0
    ),
    "PA-CF": MaterialProperties(
        print_speed_grams_per_hour=18.0,  # Langzaam, moeilijk materiaal
        nozzle_wear_factor=15.0,          # Nylon + CF = worst case
        recommended_nozzle="Ruby Nozzle",
        nozzle_replacement_cost=90.0
    ),
    "PA12-CF": MaterialProperties(
        print_speed_grams_per_hour=16.0,
        nozzle_wear_factor=15.0,
        recommended_nozzle="Ruby Nozzle", 
        nozzle_replacement_cost=90.0
    ),
}


def get_material_properties(material_name: str) -> Optional[MaterialProperties]:
    """Haal eigenschappen op voor een materiaal.
    
    Parameters:
    ----------
    material_name : str
        Naam van het materiaal
        
    Returns:
    -------
    Optional[MaterialProperties]
        Properties object of None als niet gevonden
    """
    return MATERIAL_PROPERTIES.get(material_name)


def calculate_print_time(material_name: str, weight_grams: float) -> float:
    """Bereken realistische printtijd voor materiaal en gewicht.
    
    Parameters:
    ----------
    material_name : str
        Naam van het materiaal
    weight_grams : float
        Gewicht in gram
        
    Returns:
    -------
    float
        Geschatte printtijd in uren
    """
    props = get_material_properties(material_name)
    if not props:
        # Fallback naar standaard snelheid
        return weight_grams / 25.0
    
    return weight_grams / props.print_speed_grams_per_hour


def calculate_wear_cost(material_name: str, print_hours: float) -> float:
    """Bereken nozzle slijtage kosten.
    
    Parameters:
    ----------
    material_name : str
        Naam van het materiaal
    print_hours : float
        Aantal print uren
        
    Returns:
    -------
    float
        Slijtage kosten in euro
    """
    props = get_material_properties(material_name)
    if not props:
        # Fallback: minimale slijtage
        return print_hours * 0.01
    
    return print_hours * props.wear_cost_per_hour


def get_nozzle_recommendation(material_name: str) -> str:
    """Krijg nozzle aanbeveling voor materiaal.
    
    Parameters:
    ----------
    material_name : str
        Naam van het materiaal
        
    Returns:
    -------
    str
        Aanbevolen nozzle type
    """
    props = get_material_properties(material_name)
    if not props:
        return "Brass 0.4mm (standaard)"
    
    return props.recommended_nozzle


def is_abrasive_material(material_name: str) -> bool:
    """Check of materiaal abrasief is (bevat carbon/glass fibers).
    
    Detecteert automatisch abrasieve materialen op basis van:
    - '-CF' suffix (Carbon Fiber)
    - '-GF' suffix (Glass Fiber)
    - 'Carbon' in de naam
    - 'Glass' in de naam
    
    Parameters:
    ----------
    material_name : str
        Naam van het materiaal
        
    Returns:
    -------
    bool
        True als materiaal abrasief is, False anders
        
    Examples:
    --------
    >>> is_abrasive_material("PETG-CF")
    True
    >>> is_abrasive_material("PLA Basic")
    False
    >>> is_abrasive_material("PC Carbon")
    True
    """
    # Check op bekende abrasieve markers
    abrasive_markers = ['-CF', '-GF', 'Carbon', 'Glass', 'Fiber']
    material_upper = material_name.upper()
    
    return any(marker.upper() in material_upper for marker in abrasive_markers)


# Test functies voor validatie
if __name__ == "__main__":
    print("=== Material Properties Test ===\n")
    
    # Test verschillende materialen
    test_weight = 100.0  # 100 gram
    
    for material in ["PLA Basic", "PETG-CF", "TPU 95A"]:
        props = get_material_properties(material)
        if props:
            time = calculate_print_time(material, test_weight)
            wear = calculate_wear_cost(material, time)
            
            print(f"{material}:")
            print(f"  - Print snelheid: {props.print_speed_grams_per_hour}g/uur")
            print(f"  - Tijd voor 100g: {time:.1f} uur")
            print(f"  - Slijtage factor: {props.nozzle_wear_factor}x")
            print(f"  - Slijtage kosten: €{wear:.3f}")
            print(f"  - Aanbevolen nozzle: {props.recommended_nozzle}")
            print() 