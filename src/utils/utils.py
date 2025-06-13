"""
Utilities Module - H2D Price Calculator
======================================

Dit module bevat algemene utility functies die door de hele applicatie
gebruikt worden. Het implementeert cross-cutting concerns zoals formatting,
export functionaliteit, validatie en data conversie.

Design Filosofie:
----------------
- DRY (Don't Repeat Yourself): Gemeenschappelijke functionaliteit centraliseren
- Pure Functions: Predictable input → output zonder side effects
- Type Safety: Duidelijke type hints en validatie
- Error Handling: Graceful degradation met betekenisvolle errors

Categorieën:
-----------
- Financial Formatting: Geld bedragen correct formatteren
- Data Export: CSV en andere formaten  
- Validation: Input sanitization en checks
- Conversion: Type conversies en transformaties
- Clipboard: Modern workflow support

Gebruik:
-------
    >>> amount = round_currency(19.9999)
    >>> print(f"Prijs: {format_euro(amount)}")
    Prijs: €20,00
    
    >>> export_calculation_csv(result, "output.csv")
    CSV bestand succesvol opgeslagen naar output.csv

Auteur: H2D Systems
Versie: 1.0
"""

import csv
import time
import warnings
from typing import Iterable, Dict, Any, Optional, Union, List
from datetime import datetime
from pathlib import Path


# === FINANCIAL FORMATTING ===

def round_currency(amount: float, precision: int = 2) -> float:
    """Rond geldbedrag af op commercieel gebruikelijke precisie.
    
    Deze functie gebruikt Python's ingebouwde round() functie die
    "banker's rounding" implementeert (round half to even) voor
    eerlijke verdeling van afrondingsfouten.
    
    Parameters:
    ----------
    amount : float
        Te afronden bedrag in euro
    precision : int, default=2
        Aantal decimalen (meestal 2 voor centen)
        
    Returns:
    -------
    float
        Afgerond bedrag
        
    Examples:
    --------
        >>> round_currency(19.999)
        20.00
        >>> round_currency(1.235, 2)  # Banker's rounding
        1.24
        >>> round_currency(1.245, 2)  # Banker's rounding  
        1.24
        
    Note:
    ----
    Voor financiële applicaties waar exact afronden cruciaal is,
    overweeg gebruik van decimal.Decimal in plaats van float.
    """
    return round(amount, precision)


def format_euro(amount: float) -> str:
    """Formatteer bedrag als Nederlandse euro notatie.
    
    Gebruikt Nederlandse conventies: punt voor duizendtallen,
    komma voor decimalen, euro symbool vooraan.
    
    Parameters:
    ----------
    amount : float
        Bedrag in euro
        
    Returns:
    -------
    str
        Geformatteerd bedrag (€1.234,56)
        
    Examples:
    --------
        >>> format_euro(1234.56)
        '€1.234,56'
        >>> format_euro(0.99)
        '€0,99'
        >>> format_euro(1000000)
        '€1.000.000,00'
        
    Note:
    ----
    Voor internationale applicaties, overweeg locale.currency()
    voor automatische localisatie.
    """
    rounded = round_currency(amount)
    # Format met Amerikaanse notatie eerst, dan vervangen
    formatted = f"€{rounded:,.2f}"
    # Nederlandse conventie: punt=duizend, komma=decimaal
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def safe_percentage(part: float, whole: float) -> float:
    """Bereken percentage met bescherming tegen division by zero.
    
    Parameters:
    ----------
    part : float
        Deel waarde (teller)
    whole : float
        Hele waarde (noemer)
        
    Returns:
    -------
    float
        Percentage (0-100 schaal), 0.0 bij zero division
        
    Examples:
    --------
        >>> safe_percentage(25, 100)
        25.0
        >>> safe_percentage(13.54, 25.68)  # Winst marge
        52.7
        >>> safe_percentage(10, 0)  # Zero division safe
        0.0
        
    Note:
    ----
    Retourneert altijd 0.0 bij zero division in plaats van exception.
    Voor strikte mathematische correctheid, gebruik try/except.
    """
    if whole == 0:
        return 0.0
    return (part / whole) * 100


# === DATA EXPORT FUNCTIES ===

def export_csv(records: Iterable[Dict[str, Union[float, str, int]]], filepath: str) -> None:
    """Exporteer dictionary records naar CSV bestand.
    
    Algemene CSV export functie voor structured data.
    Automatische header generatie van dictionary keys.
    
    Parameters:
    ----------
    records : Iterable[Dict[str, Union[float, str, int]]]
        Iterable van dictionaries met homogene keys
    filepath : str
        Output bestand pad
        
    Raises:
    ------
    ValueError
        Als records leeg is
    OSError
        Bij bestand schrijf problemen
        
    Examples:
    --------
        >>> data = [
        ...     {"naam": "PLA Basic", "prijs": 13.99, "gram": 100},
        ...     {"naam": "PETG-CF", "prijs": 36.29, "gram": 50}
        ... ]
        >>> export_csv(data, "materialen.csv")
        
        >>> # Export pricing results
        >>> results = [result.to_dict() for result in calculations]
        >>> export_csv(results, "prijslijst.csv")
        
    Note:
    ----
    Gebruikt UTF-8 encoding voor internationale karakters (€ symbool).
    Eerste record bepaalt fieldnames voor alle records.
    """
    records_list = list(records)
    if not records_list:
        raise ValueError("Geen records om te exporteren - lijst is leeg")

    fieldnames = records_list[0].keys()
    
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records_list)
    except OSError as e:
        raise OSError(f"Fout bij wegschrijven naar {filepath}: {e}")


def export_calculation_csv(result_data: Dict[str, Any], filepath: str) -> None:
    """Exporteer GUI calculatie resultaat naar gestructureerd CSV bestand.
    
    Maakt een professioneel geformatteerd CSV rapport van een volledige
    calculatie, geschikt voor klant communicatie en administratie.
    
    Parameters:
    ----------
    result_data : Dict[str, Any]
        Dictionary met calculatie gegevens, moet bevatten:
        - 'weight': gewicht in gram
        - 'material': materiaal naam  
        - 'costs': CostBreakdown object
        - 'price_result': PriceResult object
        - 'timestamp': datetime object
    filepath : str
        Output CSV bestand pad
        
    Raises:
    ------
    ValueError
        Als result_data leeg of incomplete is
    KeyError
        Als verplichte velden ontbreken
    OSError
        Bij bestand schrijf problemen
        
    Examples:
    --------
        >>> result_data = {
        ...     'weight': 100.0,
        ...     'material': 'PLA Basic',
        ...     'costs': cost_breakdown,
        ...     'price_result': price_result,
        ...     'timestamp': datetime.now()
        ... }
        >>> export_calculation_csv(result_data, "offerte_001.csv")
        
        >>> # Automatische filename generatie
        >>> filename = f"H2D_calc_{datetime.now():%Y%m%d_%H%M%S}.csv"
        >>> export_calculation_csv(result_data, filename)
        
    File Format:
    -----------
    Het CSV bestand bevat:
    - Header met applicatie naam en datum
    - Input parameters sectie
    - Gedetailleerde kosten breakdown
    - Verkoop pricing en winstmarge
    - Professionele layout voor klant presentatie
    """
    if not result_data:
        raise ValueError("Geen resultaat data om te exporteren - dictionary is leeg")
    
    # Valideer verplichte velden
    required_fields = ['weight', 'material', 'costs', 'price_result', 'timestamp']
    missing_fields = [field for field in required_fields if field not in result_data]
    if missing_fields:
        raise KeyError(f"Ontbrekende verplichte velden: {missing_fields}")
    
    # Haal data op uit nested objecten
    costs = result_data['costs']
    price_result = result_data['price_result']
    timestamp = result_data['timestamp']
    
    # Bouw CSV data structure
    csv_data = [
        ["H2D Prijs Calculator - Export Rapport", ""],
        ["Gegenereerd", timestamp.strftime('%d-%m-%Y %H:%M:%S')],
        ["", ""],
        
        ["=== INPUT PARAMETERS ===", ""],
        ["Gewicht (gram)", result_data['weight']],
        ["Materiaal", result_data['material']],
        ["Print tijd (geschat)", f"{result_data.get('print_hours', 'Auto')} uur"],
        ["", ""],
        
        ["=== KOSTEN BREAKDOWN ===", "Bedrag (€)"],
        ["Materiaal kosten", format_euro(costs.material_cost)],
        ["Variabele kosten", format_euro(costs.variable_cost)],
        ["Abrasief toeslag", format_euro(costs.surcharge_abrasive) if hasattr(costs, 'surcharge_abrasive') else "€0,00"],
        ["SUBTOTAAL KOSTEN", format_euro(costs.total_cost)],
        ["", ""],
        
        ["=== VERKOOP PRICING ===", "Bedrag (€)"],
        ["Advies verkoopprijs", format_euro(price_result.sell_price)],
        ["Winst bedrag", format_euro(price_result.profit_amount if hasattr(price_result, 'profit_amount') else price_result.sell_price - costs.total_cost)],
        ["Winstmarge", f"{price_result.margin_pct:.1f}%"],
        ["", ""],
        
        ["=== SAMENVATTING ===", ""],
        ["Kostprijs per gram", f"{format_euro(costs.total_cost / result_data['weight'])}"],
        ["Verkoopprijs per gram", f"{format_euro(price_result.sell_price / result_data['weight'])}"],
        ["Markup factor", f"{price_result.markup_factor if hasattr(price_result, 'markup_factor') else (price_result.sell_price / costs.total_cost):.2f}x"],
    ]
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
    except OSError as e:
        raise OSError(f"Fout bij wegschrijven CSV naar {filepath}: {e}")


# === VALIDATION UTILITIES ===

def validate_positive_number(value: Union[float, int, str], name: str) -> float:
    """Valideer dat waarde een positief getal is.
    
    Parameters:
    ----------
    value : Union[float, int, str]
        Te valideren waarde
    name : str
        Naam van het veld voor error messages
        
    Returns:
    -------
    float
        Gevalideerde waarde als float
        
    Raises:
    ------
    ValueError
        Als waarde niet geldig is of niet positief
        
    Examples:
    --------
        >>> weight = validate_positive_number("100.5", "gewicht")
        >>> print(weight)
        100.5
        
        >>> validate_positive_number(-10, "prijs")
        ValueError: prijs moet positief zijn, kreeg: -10
        
        >>> validate_positive_number("abc", "tijd")
        ValueError: tijd moet een geldig getal zijn, kreeg: abc
    """
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{name} moet een geldig getal zijn, kreeg: {value}")
    
    if numeric_value <= 0:
        raise ValueError(f"{name} moet positief zijn, kreeg: {numeric_value}")
    
    return numeric_value


def validate_material_name(material: str, valid_materials: Iterable[str]) -> str:
    """Valideer materiaalnaam tegen lijst van geldige materialen.
    
    Parameters:
    ----------
    material : str
        Te valideren materiaalnaam
    valid_materials : Iterable[str]
        Lijst van geldige materiaal namen
        
    Returns:
    -------
    str
        Gevalideerde en getrimde materiaalnaam
        
    Raises:
    ------
    ValueError
        Als materiaal niet geldig is
    """
    trimmed = material.strip()
    valid_list = list(valid_materials)
    
    if not trimmed:
        raise ValueError("Materiaalnaam mag niet leeg zijn")
    
    if trimmed not in valid_list:
        available = ', '.join(sorted(valid_list))
        raise ValueError(f"Onbekend materiaal: {trimmed}. Beschikbaar: {available}")
    
    return trimmed


# === CLIPBOARD INTEGRATION ===

def copy_to_clipboard(text: str) -> bool:
    """Kopieer tekst naar system clipboard met graceful degradation.
    
    Parameters:
    ----------
    text : str
        Te kopiëren tekst
        
    Returns:
    -------
    bool
        True als succesvol, False bij problemen
        
    Examples:
    --------
        >>> success = copy_to_clipboard("€39.22")
        >>> if success:
        ...     print("Prijs gekopieerd naar clipboard")
        ... else:
        ...     print("Clipboard niet beschikbaar")
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        # pyperclip niet geïnstalleerd
        return False
    except Exception:
        # Andere clipboard problemen (X11, permissions, etc)
        return False


# === TIME FORMATTING ===

def format_duration(minutes: int) -> str:
    """Formatteer minuten als leesbare tijdsduur.
    
    Parameters:
    ----------
    minutes : int
        Duur in minuten
        
    Returns:
    -------
    str
        Geformatteerde tijdsduur
        
    Examples:
    --------
        >>> format_duration(45)
        '45 min'
        >>> format_duration(90)
        '1 uur 30 min'
        >>> format_duration(120)
        '2 uur'
    """
    if minutes < 60:
        return f"{minutes} min"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours} uur"
    else:
        return f"{hours} uur {remaining_minutes} min"


# === PERFORMANCE UTILITIES ===

def timer_decorator(func):
    """Decorator voor functie performance timing.
    
    Example:
    -------
        >>> @timer_decorator
        ... def expensive_calculation():
        ...     time.sleep(1)
        ...     return 42
        >>> result = expensive_calculation()
        expensive_calculation uitvoerd in 1.001s
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"{func.__name__} uitgevoerd in {elapsed_time:.3f}s")
        return result
    return wrapper


# === FILE UTILITIES ===

def ensure_directory_exists(filepath: str) -> Path:
    """Zorg ervoor dat de directory voor een bestand bestaat.
    
    Parameters:
    ----------
    filepath : str
        Bestand pad
        
    Returns:
    -------
    Path
        Path object van het bestand
        
    Example:
    -------
        >>> path = ensure_directory_exists("exports/data/output.csv")
        >>> # Directory "exports/data" wordt aangemaakt indien nodig
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def generate_unique_filename(base_name: str, extension: str = ".csv") -> str:
    """Genereer unieke bestandsnaam met timestamp.
    
    Parameters:
    ----------
    base_name : str
        Basis naam voor het bestand
    extension : str, default=".csv"
        Bestand extensie
        
    Returns:
    -------
    str
        Unieke bestandsnaam
        
    Example:
    -------
        >>> filename = generate_unique_filename("h2d_calc")
        >>> print(filename)
        h2d_calc_20250128_143052.csv
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"


# === MODULE VALIDATION ===

def validate_module_dependencies() -> List[str]:
    """Controleer of alle optionele dependencies beschikbaar zijn.
    
    Returns:
    -------
    List[str]
        Lijst van ontbrekende dependencies
    """
    missing = []
    
    try:
        import pyperclip
    except ImportError:
        missing.append("pyperclip (voor clipboard functionaliteit)")
    
    return missing


# Initialisatie check
_missing_deps = validate_module_dependencies()
if _missing_deps:
    warnings.warn(
        f"Optionele dependencies ontbreken: {', '.join(_missing_deps)}. "
        "Sommige functies werken mogelijk niet optimaal.",
        UserWarning
    ) 