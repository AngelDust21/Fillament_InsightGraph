"""
Basis Statistieken Analytics Module
===================================

Deze module bevat basis statistische analyses voor de H2D calculator:
- Dagelijkse Activiteit
- Materiaal Gebruik
- Print Waardes
"""

# Lazy imports om circulaire dependencies te voorkomen
def get_dagelijkse_activiteit():
    """Lazy import van DagelijkseActiviteit."""
    from .dagelijkse_activiteit import DagelijkseActiviteit
    return DagelijkseActiviteit

def get_materiaal_gebruik():
    """Lazy import van MateriaalGebruik."""
    from .materiaal_gebruik import MateriaalGebruik
    return MateriaalGebruik

def get_print_waardes():
    """Lazy import van PrintWaardes."""
    from .print_waardes import PrintWaardes
    return PrintWaardes

__all__ = ['get_dagelijkse_activiteit', 'get_materiaal_gebruik', 'get_print_waardes'] 