"""
Configuration Module - H2D Price Calculator
===========================================

Dit module beheert alle configureerbare parameters voor kostenberekeningen
en prijsstelling. Het implementeert een hiërarchisch configuratiesysteem 
met standaard waarden en optionele gebruiker overrides.

Configuratie Hiërarchie:
-----------------------
1. Standaard waarden (in dit bestand)
2. Gebruiker configuratie (user_settings.json)
3. Runtime overrides (via GUI)

Alle waarden zijn gebaseerd op H2D_PriceBlueprint.md en representeren
realistische kosten voor een professionele 3D printing service.

Gebruik:
-------
    >>> from config import VARIABLE_COST_PER_HOUR_EXCL_MATERIAL
    >>> print(f"Variabele kosten: €{VARIABLE_COST_PER_HOUR_EXCL_MATERIAL:.2f}/uur")
    
    >>> settings = get_settings()
    >>> print(f"Materiaal markup: {settings.markup_material:.0%}")

Configuratie Updates:
--------------------
Gebruik de GUI configuratie tab of bewerk user_settings.json handmatig.
Wijzigingen worden automatisch toegepast bij herstart.

Auteur: H2D Systems
Versie: 1.0
"""

from dataclasses import dataclass
from typing import Final, Dict, Any, Callable
from pathlib import Path


# === CONFIGURATIE LADEN SYSTEEM ===

def _load_user_configuration() -> Dict[str, Any]:
    """Laad gebruiker configuratie met graceful degradation.
    
    Returns:
    -------
    Dict[str, Any]
        User configuration dictionary, leeg bij problemen
    """
    try:
        from .user_config import load_user_config, config_exists
        if config_exists():
            return load_user_config()
    except ImportError:
        # user_config module bestaat niet (eerste run)
        pass
    except Exception:
        # Configuratie bestand corrupt of andere fout
        pass
    
    return {}


def _create_value_getters() -> tuple[Callable[[str, float], float], Callable[[str, int], int]]:
    """Maak type-safe value getter functies.
    
    Returns:
    -------
    tuple[Callable, Callable]
        (get_float_func, get_int_func) met fallback naar defaults
    """
    user_config = _load_user_configuration()
    
    def get_float(key: str, default: float) -> float:
        """Haal float waarde op met fallback naar default."""
        try:
            val = user_config.get(key, str(default))
            return float(val)
        except (ValueError, TypeError):
            return default
    
    def get_int(key: str, default: int) -> int:
        """Haal int waarde op met fallback naar default."""
        try:
            val = user_config.get(key, str(default))
            return int(float(val))  # float() first om "25.0" -> 25 te parsen
        except (ValueError, TypeError):
            return default
    
    return get_float, get_int


# Initialiseer value getters
_get_float, _get_int = _create_value_getters()


# === BASIS OPERATIONELE KOSTEN ===
# Deze waarden representeren de werkelijke kosten van printer operatie

# Energie verbruik en kosten
PRINTER_POWER_KW: Final[float] = _get_float('printer_power', 1.05)
"""Gemiddeld stroomverbruik van Bambu Lab X1C in kilowatt.
Gebaseerd op: verwarmde bed (120W) + hotend (40W) + motors/fans (300W) + electronica (90W).
Totaal ~550W actief printen + 500W idle warming = 1.05kW gemiddeld."""

ENERGY_PRICE_PER_KWH: Final[float] = _get_float('energy_price', 0.35)  
"""Energieprijs per kilowattuur in euro.
Belgische gemiddelde 2024: €0.35/kWh inclusief belastingen en distributiekosten.
Update deze waarde bij significante energieprijswijzigingen."""

# Arbeid en monitoring kosten  
LABOUR_COST_PER_HOUR: Final[float] = _get_float('labour_cost', 27.80)
"""Arbeidskosten per uur voor 3D printing operator.
Gebaseerd op: €16/uur bruto + 73% werkgeverslasten RSZ = €27.80 totaal.
Omvat: lonen, RSZ bijdragen, vakantiegeld, eindejaarspremie, verzekeringen."""

MONITORING_PERCENTAGE: Final[float] = _get_float('monitoring_pct', 10) / 100
"""Percentage van arbeidskosten voor print monitoring.
10% betekent: 6 minuten actieve monitoring per print uur.
Omvat: start setup, progress checks, problem solving, finish handling."""

# Onderhoud en slijtage
MAINTENANCE_COST_PER_HOUR: Final[float] = _get_float('maintenance_cost', 0.0765)
"""Onderhoud en slijtagekosten per print uur.
Berekening: €153 per 2000 uur = €0.0765/uur.
Omvat: nozzles, belts, sensors, lubricants, preventief onderhoud."""

# Overhead en vaste kosten
OVERHEAD_PER_YEAR: Final[int] = _get_int('overhead_year', 7200)
"""Jaarlijkse overhead kosten voor 3D printing operatie.
Omvat: ruimte huur, verzekeringen, boekhouding, marketing, afschrijving printer.
Verdeeld over ANNUAL_PRINT_HOURS voor kostprijs per uur."""

ANNUAL_PRINT_HOURS: Final[int] = _get_int('annual_hours', 1920)
"""Verwachte print uren per jaar voor overhead verdeling.
Basis: 240 werkdagen × 8 uur = 1920 uur bij volledige bezetting.
Realistisch voor professionele service met goede planning."""


# === PRICING STRATEGIE PARAMETERS ===
# Deze waarden bepalen de winstgevendheid en competitiviteit

# Markup factoren (als vermenigvuldigingsfactor)
MARKUP_MATERIAL: Final[float] = _get_float('markup_material', 180) / 100
"""Markup factor voor materiaalkosten (180% = factor 1.8).
Rationale: Compenseert voorraadrisico, handling, prijsfluctuaties.
Aangepast aan Belgische marktprijzen."""

MARKUP_VARIABLE: Final[float] = _get_float('markup_variable', 140) / 100  
"""Markup factor voor variabele kosten (140% = factor 1.4).
Rationale: Service pricing voor tijd en expertise.
Competitief voor Belgische markt."""

# Toeslag parameters
SPOED_SURCHARGE_RATE: Final[float] = _get_float('spoed_surcharge', 25) / 100
"""Spoedtoeslag als percentage van finale prijs (25% = factor 0.25).
Percentage schaalt met order grootte: €40 order → +€10, €200 order → +€50.
Compenseert planning disruption en opportunity cost."""

ABRASIVE_SURCHARGE_PER_HOUR: Final[float] = _get_float('abrasive_surcharge', 0.50)
"""Extra toeslag per uur voor abrasieve materialen (CF/GF) in euro.
Compenseert: verhoogde nozzle slijtage, extruder onderhoud, kwaliteitscontrole.
Gebaseerd op 10× snellere nozzle vervanging bij carbon fiber prints."""

COLOR_SETUP_FEE_MIN: Final[int] = _get_int('color_fee_min', 15)
"""Minimum setup fee voor multicolor prints in euro.
Dekt: extra filament wisseling tijd, verhoogd faalrisico, complexere QC."""

COLOR_SETUP_FEE_MAX: Final[int] = _get_int('color_fee_max', 30) 
"""Maximum setup fee voor complexe multicolor prints in euro.
Voor prints met >3 kleuren of complexe kleur overgangen."""

# Automatische tijd estimatie
AUTO_TIME_PER_GRAM_H: Final[float] = _get_float('auto_time_per_gram', 0.04)
"""Standaard print tijd ratio: uur per gram (0.04 = 25g/uur).
Gebaseerd op gemiddelde van 0.2mm layer height, 50mm/s print speed.
Redelijk accuraat voor 80% van standaard prints zonder veel support."""


# === BEREKENDE WAARDEN ===
# Deze waarden worden automatisch afgeleid van bovenstaande parameters

ENERGY_COST_PER_HOUR: Final[float] = PRINTER_POWER_KW * ENERGY_PRICE_PER_KWH
"""Energie kosten per print uur: {PRINTER_POWER_KW}kW × €{ENERGY_PRICE_PER_KWH}/kWh = €{ENERGY_COST_PER_HOUR:.3f}/uur."""

MONITORING_COST_PER_HOUR: Final[float] = LABOUR_COST_PER_HOUR * MONITORING_PERCENTAGE  
"""Monitoring kosten per print uur: €{LABOUR_COST_PER_HOUR}/uur × {MONITORING_PERCENTAGE:.1%} = €{MONITORING_COST_PER_HOUR:.2f}/uur."""

OVERHEAD_COST_PER_HOUR: Final[float] = OVERHEAD_PER_YEAR / ANNUAL_PRINT_HOURS
"""Overhead kosten per print uur: €{OVERHEAD_PER_YEAR}/jaar ÷ {ANNUAL_PRINT_HOURS} uur = €{OVERHEAD_COST_PER_HOUR:.4f}/uur."""

VARIABLE_COST_PER_HOUR_EXCL_MATERIAL: Final[float] = (
    ENERGY_COST_PER_HOUR + 
    MAINTENANCE_COST_PER_HOUR + 
    MONITORING_COST_PER_HOUR + 
    OVERHEAD_COST_PER_HOUR
)
"""Totale variabele kosten per uur exclusief materiaal.
Samenstelling:
- Energie: €{ENERGY_COST_PER_HOUR:.3f}/uur
- Onderhoud: €{MAINTENANCE_COST_PER_HOUR:.4f}/uur  
- Monitoring: €{MONITORING_COST_PER_HOUR:.2f}/uur
- Overhead: €{OVERHEAD_COST_PER_HOUR:.4f}/uur
TOTAAL: €{VARIABLE_COST_PER_HOUR_EXCL_MATERIAL:.2f}/uur"""


# === CONFIGURATIE SNAPSHOT KLASSE ===

@dataclass(frozen=True)
class Settings:
    """Immutable snapshot van alle configuratie instellingen.
    
    Deze dataclass biedt een consistent interface voor toegang tot 
    alle configuratie waarden, handig voor testing en API calls.
    
    Attributes:
    ----------
    energy_cost_per_hour : float
        Berekende energie kosten per print uur
    maintenance_cost_per_hour : float
        Onderhoud en slijtage kosten per uur
    monitoring_cost_per_hour : float
        Arbeidskosten voor print monitoring per uur
    overhead_cost_per_hour : float
        Vaste kosten (overhead) verdeeld per print uur
    variable_cost_per_hour : float
        Totale variabele kosten per uur (exclusief materiaal)
    markup_material : float
        Markup factor voor materiaal kosten (2.0 = 200%)
    markup_variable : float
        Markup factor voor variabele kosten (1.5 = 150%)
        
    Example:
    -------
        >>> settings = get_settings()
        >>> print(f"Totale kosten: €{settings.variable_cost_per_hour:.2f}/uur")
        >>> print(f"Materiaal markup: {settings.markup_material:.0%}")
        
    Note:
    ----
    frozen=True maakt deze class immutable. Voor nieuwe configuratie
    waarden, maak een nieuwe Settings instance.
    """

    # Kosten componenten per uur
    energy_cost_per_hour: float = ENERGY_COST_PER_HOUR
    maintenance_cost_per_hour: float = MAINTENANCE_COST_PER_HOUR  
    monitoring_cost_per_hour: float = MONITORING_COST_PER_HOUR
    overhead_cost_per_hour: float = OVERHEAD_COST_PER_HOUR
    variable_cost_per_hour: float = VARIABLE_COST_PER_HOUR_EXCL_MATERIAL
    
    # Pricing parameters
    markup_material: float = MARKUP_MATERIAL
    markup_variable: float = MARKUP_VARIABLE
    
    @property
    def total_hourly_cost_breakdown(self) -> Dict[str, float]:
        """Gedetailleerde uitsplitsing van kosten per uur.
        
        Returns:
        -------
        Dict[str, float]
            Dictionary met alle kostencomponenten
        """
        return {
            "energie": self.energy_cost_per_hour,
            "onderhoud": self.maintenance_cost_per_hour,
            "monitoring": self.monitoring_cost_per_hour, 
            "overhead": self.overhead_cost_per_hour,
            "totaal": self.variable_cost_per_hour
        }
    
    @property
    def break_even_hours_per_month(self) -> float:
        """Minimum print uren per maand voor break-even.
        
        Returns:
        -------
        float
            Benodigde print uren per maand om overhead te dekken
        """
        monthly_overhead = OVERHEAD_PER_YEAR / 12
        return monthly_overhead / self.variable_cost_per_hour
    
    def cost_estimate(self, hours: float, material_cost: float) -> Dict[str, float]:
        """Snelle kosten schatting voor gegeven parameters.
        
        Parameters:
        ----------
        hours : float
            Print tijd in uren
        material_cost : float
            Materiaal kosten in euro
            
        Returns:
        -------
        Dict[str, float]
            Kosten en pricing schatting
        """
        variable = self.variable_cost_per_hour * hours
        total_cost = material_cost + variable
        
        return {
            "materiaal_kosten": material_cost,
            "variabele_kosten": variable, 
            "totale_kosten": total_cost,
            "advies_prijs": (material_cost * self.markup_material) + (variable * self.markup_variable),
            "geschatte_marge_pct": ((material_cost * self.markup_material + variable * self.markup_variable) - total_cost) / total_cost * 100 if total_cost > 0 else 0
        }


def get_settings() -> Settings:
    """Verkrijg huidige configuratie instellingen als Settings object.
    
    Retourneert een snapshot van alle huidige configuratie waarden.
    Handig voor consistent gebruik door de applicatie.
    
    Returns:
    -------
    Settings
        Immutable settings object met alle configuratie waarden
        
    Example:
    -------
        >>> settings = get_settings()
        >>> breakdown = settings.total_hourly_cost_breakdown
        >>> print(f"Energie: €{breakdown['energie']:.3f}/uur")
        
        >>> estimate = settings.cost_estimate(4.0, 1.40)
        >>> print(f"Geschatte prijs: €{estimate['advies_prijs']:.2f}")
    """
    return Settings()


def validate_configuration() -> Dict[str, str]:
    """Valideer configuratie waarden op redelijkheid.
    
    Returns:
    -------
    Dict[str, str]
        Dictionary met eventuele waarschuwingen of fouten
        
    Example:
    -------
        >>> warnings = validate_configuration()
        >>> if warnings:
        ...     for param, warning in warnings.items():
        ...         print(f"Waarschuwing {param}: {warning}")
    """
    warnings = {}
    
    # Energie kosten redelijkheid
    if ENERGY_COST_PER_HOUR > 1.0:
        warnings['energie'] = f"Hoge energie kosten: €{ENERGY_COST_PER_HOUR:.3f}/uur"
    
    # Markup redelijkheid  
    if MARKUP_MATERIAL < 1.2:
        warnings['markup_material'] = f"Lage materiaal markup: {MARKUP_MATERIAL:.0%}"
    if MARKUP_VARIABLE < 1.2:
        warnings['markup_variable'] = f"Lage variabele markup: {MARKUP_VARIABLE:.0%}"
        
    # Toeslag redelijkheid
    if SPOED_SURCHARGE_RATE > 0.50:
        warnings['spoed'] = f"Hoge spoedtoeslag: {SPOED_SURCHARGE_RATE:.0%}"
        
    return warnings


# === MODULE INITIALISATIE ===
# Valideer configuratie bij module import
_config_warnings = validate_configuration()
if _config_warnings:
    import warnings
    for param, warning in _config_warnings.items():
        warnings.warn(f"Configuratie waarschuwing voor {param}: {warning}", UserWarning) 