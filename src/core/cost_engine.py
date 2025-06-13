"""
Cost Engine Module - H2D Price Calculator
=========================================

Dit module bevat de core kostenberekening logica voor 3D printing services.
Het implementeert een gedetailleerde kostprijsstructuur die alle aspecten
van 3D printing productie meeneemt.

Componenten:
-----------
- Materiaalkosten: Gebaseerd op gewicht en materiaalprijs per gram
- Variabele kosten: Energie, onderhoud, arbeid en overhead per uur
- Toeslagen: Extra kosten voor abrasieve materialen
- Slijtage: Realistische nozzle slijtage per materiaal

UPDATE v1.1:
-----------
- Gebruik material_properties voor realistische printtijden
- Aparte slijtage berekening per materiaal type
- Betere schatting op basis van printsnelheid

Gebruik:
-------
    >>> costs = calculate_costs(100.0, "PLA Basic", print_hours=4.0)
    >>> print(f"Totale kosten: €{costs.total_cost:.2f}")
    Totale kosten: €25.68

Auteur: H2D Systems
Versie: 1.1
"""

from dataclasses import dataclass
from typing import Dict, Optional

from ..config import (
    VARIABLE_COST_PER_HOUR_EXCL_MATERIAL, 
    AUTO_TIME_PER_GRAM_H, 
    ABRASIVE_SURCHARGE_PER_HOUR
)
from ..materials.materials import get_price

# Probeer material properties te importeren
try:
    from ..materials.material_properties import (
        calculate_print_time as calc_print_time_realistic,
        calculate_wear_cost,
        get_material_properties
    )
    HAS_MATERIAL_PROPERTIES = True
except ImportError:
    HAS_MATERIAL_PROPERTIES = False


@dataclass
class CostBreakdown:
    """Gedetailleerde kostprijsstructuur voor een 3D print.
    
    Deze dataclass bevat alle kostencomponenten van een print opdracht,
    opgesplitst in traceerbare categorieën voor transparante prijsstelling.
    
    Attributes:
    ----------
    material_cost : float
        Kosten van het verbruikte filament in euro (gewicht × prijs/gram)
    variable_cost : float
        Variabele productiekosten in euro (energie + onderhoud + arbeid + overhead)
    surcharge_abrasive : float
        Extra toeslag voor abrasieve materialen in euro (CF/GF slijtage)
    total_cost : float
        Totale kostprijs in euro (som van alle componenten)
        
    Example:
    -------
        >>> breakdown = CostBreakdown(1.40, 24.28, 0.0, 25.68)
        >>> print(f"Materiaal: €{breakdown.material_cost:.2f}")
        Materiaal: €1.40
        
    Note:
    ----
    Deze class is immutable (frozen) om accidentele wijzigingen te voorkomen.
    Alle bedragen worden intern opgeslagen met volledige precisie.
    """

    material_cost: float
    variable_cost: float  # energie + onderhoud + arbeid + overhead
    surcharge_abrasive: float
    total_cost: float

    def to_dict(self) -> Dict[str, float]:
        """Converteer kostenverdeling naar dictionary format.
        
        Handig voor JSON serialisatie, CSV export en API responses.
        Alle bedragen worden afgerond naar 2 decimalen (centen).
        
        Returns:
        -------
        Dict[str, float]
            Dictionary met alle kostencomponenten, afgerond naar centen
            
        Example:
        -------
            >>> costs = CostBreakdown(1.399, 24.283, 0.0, 25.682)
            >>> data = costs.to_dict()
            >>> print(data["material_cost"])
            1.40
        """
        return {
            "material_cost": round(self.material_cost, 2),
            "variable_cost": round(self.variable_cost, 2),
            "surcharge_abrasive": round(self.surcharge_abrasive, 2),
            "total_cost": round(self.total_cost, 2),
        }


def _calc_print_hours_auto(weight_g: float, material: Optional[str] = None) -> float:
    """Bepaal automatische printduur gebaseerd op gewicht en materiaal.
    
    Gebruikt material properties indien beschikbaar voor realistische
    printsnelheden per materiaal type. Valt terug op standaard ratio
    als material properties niet gevonden worden.
    
    Parameters:
    ----------
    weight_g : float
        Gewicht van de print in gram
    material : Optional[str]
        Materiaal naam voor specifieke printsnelheid lookup
        
    Returns:
    -------
    float
        Geschatte printduur in uren
        
    Example:
    -------
        >>> uren = _calc_print_hours_auto(100.0, "PLA Basic")
        >>> print(f"{uren:.1f} uur")
        3.3 uur
        
        >>> uren = _calc_print_hours_auto(100.0, "TPU 95A")
        >>> print(f"{uren:.1f} uur")
        6.7 uur
        
    Note:
    ----
    TPU print veel langzamer (15g/uur) dan PLA (30g/uur).
    Dit heeft grote impact op de totale kosten!
    """
    if HAS_MATERIAL_PROPERTIES and material:
        # Gebruik realistische snelheid per materiaal
        return calc_print_time_realistic(material, weight_g)
    else:
        # Fallback naar standaard ratio
        return weight_g * AUTO_TIME_PER_GRAM_H


def calculate_costs(
    weight_g: float,
    material: str,
    *,
    print_hours: Optional[float] = None,
    abrasive: bool = False,
) -> CostBreakdown:
    """Bereken de volledige kostprijs voor een 3D print.
    
    Dit is de hoofdfunctie van de cost engine. Het combineert alle
    kostencomponenten tot een transparante kostprijsstructuur.
    
    Parameters:
    ----------
    weight_g : float
        Gewicht van de print in gram (moet positief zijn)
    material : str
        Naam van het materiaal (moet bestaan in materials database)
    print_hours : Optional[float], default=None
        Handmatige printduur in uren. Indien None wordt automatisch
        berekend op basis van gewicht (0.04 uur/gram)
    abrasive : bool, default=False
        True indien het materiaal abrasief is (CF/GF). Voegt extra
        slijtagekosten toe voor nozzle en extruder onderhoud
        
    Returns:
    -------
    CostBreakdown
        Gedetailleerde kostenverdeling met alle componenten
        
    Raises:
    ------
    KeyError
        Als het opgegeven materiaal niet bestaat in de database
    ValueError
        Als gewicht negatief is of andere ongeldige parameters
        
    Examples:
    --------
    Basis gebruik met automatische tijdsberekening:
    
        >>> costs = calculate_costs(100.0, "PLA Basic")
        >>> print(f"Totaal: €{costs.total_cost:.2f}")
        Totaal: €25.68
        
    Met handmatige printduur:
    
        >>> costs = calculate_costs(50.0, "PETG-CF", print_hours=2.5, abrasive=True)
        >>> print(f"Materiaal: €{costs.material_cost:.2f}")
        >>> print(f"Variabel: €{costs.variable_cost:.2f}")
        >>> print(f"Abrasief: €{costs.surcharge_abrasive:.2f}")
        
    Voor batch berekeningen:
    
        >>> materials = ["PLA Basic", "PETG Basic", "ABS"]
        >>> weights = [75, 125, 200]
        >>> costs_list = [calculate_costs(w, m) for w, m in zip(weights, materials)]
        
    Note:
    ----
    - Alle bedragen zijn in euro
    - Materiaalkosten zijn gebaseerd op bulk prijzen (≥6 rollen)
    - Variabele kosten dekken alle operationele uitgaven per uur
    - Abrasieve toeslag compenseert extra slijtage aan printer onderdelen
    """
    # Input validatie
    if weight_g <= 0:
        raise ValueError(f"Gewicht moet positief zijn, kreeg: {weight_g}")
    
    # Bepaal printduur (auto of handmatig)
    if print_hours is None:
        print_hours = _calc_print_hours_auto(weight_g, material)
    elif print_hours < 0:
        raise ValueError(f"Print uren moeten positief zijn, kreeg: {print_hours}")

    # Materiaalkost berekening
    price_per_gram = get_price(material)  # Kan KeyError gooien
    material_cost = price_per_gram * weight_g

    # Variabele kosten (energie, onderhoud, arbeid, overhead)
    variable_cost = VARIABLE_COST_PER_HOUR_EXCL_MATERIAL * print_hours

    # Slijtage kosten berekening
    if HAS_MATERIAL_PROPERTIES:
        # Gebruik material-specifieke slijtage berekening
        surcharge_abrasive = calculate_wear_cost(material, print_hours)
    else:
        # Fallback naar oude abrasive flag methode
        surcharge_abrasive = ABRASIVE_SURCHARGE_PER_HOUR * print_hours if abrasive else 0.0

    # Totaal kostprijs
    total = material_cost + variable_cost + surcharge_abrasive

    return CostBreakdown(
        material_cost=material_cost,
        variable_cost=variable_cost,
        surcharge_abrasive=surcharge_abrasive,
        total_cost=total,
    ) 