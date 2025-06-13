"""
Pricing Engine Module - H2D Price Calculator  
===========================================

Dit module implementeert de intelligente prijsstellingslogica voor 3D printing services.
Het combineert kostprijsberekeningen met strategische markup en toeslagen voor 
winstgevende maar competitieve prijsstelling.

Pricing Strategie:
-----------------
- Gedifferentieerde markup: Materiaal (200%) vs Variabel (150%)
- Toeslagen voor complexiteit: Multicolor setup fees
- Urgentie premiums: Spoedtoeslag percentage
- Transparantie: Volledige marge berekening

Workflow:
--------
1. Kostprijs berekenen via cost_engine
2. Markup toepassen per categorie  
3. Toeslagen additioneel berekenen
4. Winstmarge percentage vaststellen

Gebruik:
-------
    >>> result = calculate_sell_price(
    ...     weight_g=100.0,
    ...     material="PLA Basic", 
    ...     multicolor=True,
    ...     spoed=True
    ... )
    >>> print(f"Verkoopprijs: €{result.sell_price:.2f}")
    >>> print(f"Winstmarge: {result.margin_pct:.1f}%")

Auteur: H2D Systems
Versie: 1.0
"""

from dataclasses import dataclass
from typing import Dict, Optional

from ..config import (
    MARKUP_MATERIAL,
    MARKUP_VARIABLE,
    COLOR_SETUP_FEE_MIN,
    COLOR_SETUP_FEE_MAX,
    SPOED_SURCHARGE_RATE,
)
from .cost_engine import calculate_costs, CostBreakdown


@dataclass
class PriceResult:
    """Compleet prijsresultaat met kostopbouw en verkoopprijs.
    
    Deze dataclass combineert de gedetailleerde kostenverdeling van
    cost_engine met de finale verkoop pricing en winstmarge analyse.
    
    Attributes:
    ----------
    breakdown : CostBreakdown
        Gedetailleerde kostprijsstructuur van de onderliggende print
    sell_price : float
        Finale adviesverkoopprijs in euro (inclusief markup en toeslagen)
    margin_pct : float
        Winstmarge percentage ((verkoop - kosten) / kosten * 100)
        
    Example:
    -------
        >>> costs = CostBreakdown(1.40, 24.28, 0.0, 25.68)
        >>> result = PriceResult(costs, 39.22, 52.7)
        >>> print(f"Winst: €{result.sell_price - result.breakdown.total_cost:.2f}")
        Winst: €13.54
        
    Note:
    ----
    De marge percentage geeft direct inzicht in de winstgevendheid
    van de opdracht en helpt bij strategische prijsstelling.
    """

    breakdown: CostBreakdown
    sell_price: float
    margin_pct: float

    def to_dict(self) -> Dict[str, float]:
        """Converteer volledige pricing naar dictionary format.
        
        Combineert kostenverdeling met verkoop data voor complete export.
        Handig voor rapportage, API responses en data analyse.
        
        Returns:
        -------
        Dict[str, float]
            Dictionary met alle kosten- en pricing componenten
            
        Example:
        -------
            >>> result = PriceResult(breakdown, 39.22, 52.7)
            >>> data = result.to_dict()
            >>> print(f"ROI: {data['margin_pct']:.1f}%")
            ROI: 52.7%
        """
        d = self.breakdown.to_dict()
        d.update({
            "sell_price": round(self.sell_price, 2),
            "margin_pct": round(self.margin_pct, 1),
        })
        return d

    @property
    def profit_amount(self) -> float:
        """Absolute winst in euro.
        
        Returns:
        -------
        float
            Winst bedrag (verkoopprijs - kostprijs)
        """
        return self.sell_price - self.breakdown.total_cost

    @property  
    def markup_factor(self) -> float:
        """Totale markup factor (verkoopprijs / kostprijs).
        
        Returns:
        -------
        float
            Multiplicatieve factor, bijv. 1.53 = 53% markup
        """
        if self.breakdown.total_cost == 0:
            return 0.0
        return self.sell_price / self.breakdown.total_cost


def calculate_sell_price(
    *,
    weight_g: float,
    material: str,
    print_hours: Optional[float] = None,
    abrasive: bool = False,
    multicolor: bool = False,
    spoed: bool = False,
) -> PriceResult:
    """Bereken intelligente adviesverkoopprijs voor 3D print.
    
    Dit is de hoofdfunctie van de pricing engine. Het combineert kostprijs
    berekening met strategische markup en toeslagen voor optimale pricing.
    
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
        True indien het materiaal abrasief is (CF/GF). Verhoogt slijtagekosten
    multicolor : bool, default=False
        True voor multi-kleur prints. Voegt vaste setup fee toe
        (gemiddeld van min/max color fee)
    spoed : bool, default=False
        True voor spoedopdrachten. Voegt percentage toeslag toe
        op finale prijs (standaard 25%)
        
    Returns:
    -------
    PriceResult
        Compleet pricing resultaat met kostenverdeling, verkoopprijs
        en winstmarge percentage
        
    Raises:
    ------
    KeyError
        Als het opgegeven materiaal niet bestaat in de database
    ValueError
        Als gewicht negatief is of andere ongeldige parameters
        
    Examples:
    --------
    Basis pricing voor standaard print:
    
        >>> result = calculate_sell_price(weight_g=100.0, material="PLA Basic")
        >>> print(f"Prijs: €{result.sell_price:.2f}")
        >>> print(f"Marge: {result.margin_pct:.1f}%")
        Prijs: €39.22
        Marge: 52.7%
        
    Premium print met alle toeslagen:
    
        >>> result = calculate_sell_price(
        ...     weight_g=50.0,
        ...     material="PETG-CF", 
        ...     print_hours=3.0,
        ...     abrasive=True,
        ...     multicolor=True,
        ...     spoed=True
        ... )
        >>> print(f"Basis kosten: €{result.breakdown.total_cost:.2f}")
        >>> print(f"Verkoop: €{result.sell_price:.2f}")
        >>> print(f"Winst: €{result.profit_amount:.2f}")
        
    Batch pricing voor offertes:
    
        >>> prints = [
        ...     {"weight_g": 75, "material": "PLA Basic"},
        ...     {"weight_g": 150, "material": "PETG Basic", "spoed": True},
        ...     {"weight_g": 200, "material": "ABS", "multicolor": True}
        ... ]
        >>> results = [calculate_sell_price(**p) for p in prints]
        >>> total = sum(r.sell_price for r in results)
        
    Sensitivity analyse:
    
        >>> base = calculate_sell_price(weight_g=100, material="PLA Basic")
        >>> rush = calculate_sell_price(weight_g=100, material="PLA Basic", spoed=True)
        >>> premium = rush.sell_price - base.sell_price
        >>> print(f"Spoedtoeslag: €{premium:.2f}")
        
    Note:
    ----
    - Markup strategie: Materiaal 200%, Variabel 150% 
    - Multicolor fee: Gemiddelde van €15-€30 (€22.50)
    - Spoedtoeslag: 25% op finale prijs
    - Marge berekening: (verkoop - kosten) / kosten * 100
    
    Tips:
    ----
    - Gebruik spoed=True spaarzaam voor echte urgentie
    - Multicolor verhoogt setup tijd en faalrisico  
    - Abrasieve materialen vereisen extra onderhoud
    - Monitor marges: <20% te laag, >60% mogelijk te hoog
    """
    # Input validatie via cost_engine (delegatie)
    breakdown = calculate_costs(
        weight_g=weight_g,
        material=material,
        print_hours=print_hours,
        abrasive=abrasive,
    )

    # Gesegmenteerde markup strategie
    cost_material = breakdown.material_cost
    cost_variable = breakdown.variable_cost + breakdown.surcharge_abrasive

    # Basis verkoopprijs met gedifferentieerde markup
    sell_price = (cost_material * MARKUP_MATERIAL) + (cost_variable * MARKUP_VARIABLE)

    # Complexiteits toeslagen
    if multicolor:
        # Vaste setup fee voor multi-kleur complexiteit
        setup_fee = (COLOR_SETUP_FEE_MIN + COLOR_SETUP_FEE_MAX) / 2
        sell_price += setup_fee
        
    if spoed:
        # Percentage toeslag voor urgentie (schaalt met order grootte)
        sell_price *= (1 + SPOED_SURCHARGE_RATE)

    # Winstmarge berekening
    if breakdown.total_cost > 0:
        margin_percentage = (sell_price - breakdown.total_cost) / breakdown.total_cost * 100
    else:
        margin_percentage = 0.0  # Edge case: zero cost

    return PriceResult(
        breakdown=breakdown, 
        sell_price=sell_price, 
        margin_pct=margin_percentage
    ) 