"""
Command Line Interface Module - H2D Price Calculator
===================================================

Dit module implementeert de command line interface voor de H2D Price Calculator.
Het biedt een flexibele CLI die zowel volledige automation als interactieve
gebruiker dialogen ondersteunt.

CLI Design Filosofie:
--------------------
- Flexibele input: CLI args, interactive prompts, of hybride
- User-friendly: Nederlandse prompts en duidelijke feedback  
- Automation ready: Scriptable voor batch processing
- Graceful degradation: Robust error handling met meaningful messages

Gebruik Modi:
------------
1. Volledig CLI: python cli.py 100 "PLA Basic" --hours 4.0
2. Interactief: python cli.py (vraagt om alle invoer)
3. Hybride: python cli.py 100 (vraagt alleen ontbrekende parameters)

Output:
------
Gestructureerde output geschikt voor zowel menselijk als programmatisch gebruik.
Gebruikt pprint voor leesbare formatting van complexe data.

Auteur: H2D Systems
Versie: 1.0
"""

import argparse
import sys
from typing import List, Optional, Any
from pprint import pprint

from ..materials import list_materials, get_material
from ..core import calculate_sell_price
from ..utils import validate_positive_number, format_euro


def _build_argument_parser() -> argparse.ArgumentParser:
    """Bouw en configureer de argument parser voor CLI interface.
    
    Implementeert een gebruiksvriendelijke argument structuur met
    positionele argumenten voor basis parameters en optionele flags
    voor geavanceerde opties.
    
    Returns:
    -------
    argparse.ArgumentParser
        Geconfigureerde argument parser
        
    Design Overwegingen:
    -------------------
    - Positionele args voor meest gebruikte parameters (weight, material)
    - Optional arguments met duidelijke defaults
    - Help strings in het Nederlands voor lokale gebruikers
    - ArgumentDefaultsHelpFormatter toont default waarden in help
    """
    parser = argparse.ArgumentParser(
        description="H2D Price Calculator - Command Line Interface\n"
                   "Bereken kostprijs en advies verkoopprijs voor 3D prints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  %(prog)s 100 "PLA Basic"                    # Basis berekening
  %(prog)s 150 "PETG-CF" --hours 6 --abrasive # Geavanceerde opties
  %(prog)s 50 "PLA Basic" --multicolor --spoed # Met toeslagen
  %(prog)s                                     # Volledig interactief
  
Ondersteunde materialen:
  Gebruik zonder argumenten voor volledige lijst, of bekijk
  de materials database voor actuele prijzen en beschikbaarheid.
        """
    )
    
    # Positionele argumenten (optioneel via nargs="?")
    parser.add_argument(
        "weight", 
        type=float, 
        nargs="?", 
        help="Gewicht van de print in gram (positief getal)"
    )
    parser.add_argument(
        "material", 
        nargs="?", 
        help='Materiaal naam (bijv. "PLA Basic", "PETG-CF")'
    )

    # Optionele parameters
    parser.add_argument(
        "--hours", "--time",
        type=float,
        default=None,
        metavar="UREN",
        help="Handmatige printduur in uren (default: automatisch op basis van gewicht)"
    )
    
    # Boolean flags voor special cases
    parser.add_argument(
        "--abrasive", "--cf", "--gf",
        action="store_true", 
        help="Abrasief materiaal (Carbon Fiber/Glass Fiber) - verhoogt slijtagekosten"
    )
    parser.add_argument(
        "--multicolor", "--ams",
        action="store_true", 
        help="Multi-kleur print - voegt setup fee toe"
    )
    parser.add_argument(
        "--spoed", "--rush",
        action="store_true", 
        help="Spoedopdracht (<48 uur) - voegt urgentie toeslag toe"
    )
    
    # Utility flags
    parser.add_argument(
        "--list-materials", "--list",
        action="store_true",
        help="Toon alle beschikbare materialen en prijzen"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimale output, alleen eindresultaat"
    )
    
    return parser


def _display_materials() -> None:
    """Toon overzicht van alle beschikbare materialen met prijzen.
    
    Geformatteerd overzicht geschikt voor gebruiker selectie.
    Sorteert materialen op prijs voor overzichtelijkheid.
    """
    print("\n=== Beschikbare Materialen ===")
    print(f"{'Materiaal':<20} {'Prijs/kg':<12} {'Prijs/gram':<12}")
    print("-" * 45)
    
    materials = list_materials()
    # Sorteer op prijs voor logische volgorde
    sorted_materials = sorted(materials.items(), key=lambda x: x[1].price_per_kg)
    
    for name, material in sorted_materials:
        price_kg = format_euro(material.price_per_kg)
        price_g = f"€{material.price_per_gram:.3f}"
        print(f"{name:<20} {price_kg:<12} {price_g:<12}")
    
    print(f"\nTotaal {len(materials)} materialen beschikbaar")


def _get_interactive_weight() -> float:
    """Vraag gebruiker om gewicht input met validatie.
    
    Returns:
    -------
    float
        Gevalideerd gewicht in gram
        
    Raises:
    ------
    KeyboardInterrupt
        Als gebruiker Ctrl+C indrukt
    ValueError
        Als na meerdere pogingen geen geldig gewicht
    """
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            weight_input = input("Gewicht in gram: ").strip()
            if not weight_input:
                print("Gewicht is verplicht. Probeer opnieuw.")
                attempts += 1
                continue
                
            return validate_positive_number(weight_input, "gewicht")
            
        except ValueError as e:
            print(f"Ongeldige invoer: {e}")
            attempts += 1
            if attempts < max_attempts:
                print(f"Nog {max_attempts - attempts} poging(en) over.")
    
    raise ValueError("Te veel ongeldige invoerpogingen voor gewicht")


def _get_interactive_material() -> str:
    """Vraag gebruiker om materiaal selectie met validatie.
    
    Toont eerst de beschikbare materialen, dan vraagt om selectie.
    Ondersteunt zowel naam als nummer selectie.
    
    Returns:
    -------
    str
        Gevalideerde materiaalnaam
        
    Raises:
    ------
    ValueError
        Als na meerdere pogingen geen geldig materiaal
    """
    materials = list_materials()
    material_list = list(materials.keys())
    
    print("\nBeschikbare materialen:")
    for i, name in enumerate(material_list, 1):
        price = format_euro(materials[name].price_per_kg)
        print(f"{i:2d}. {name:<20} {price}")
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            selection = input("\nKies materiaal (naam of nummer): ").strip()
            if not selection:
                print("Materiaal selectie is verplicht.")
                attempts += 1
                continue
            
            # Probeer als nummer
            try:
                index = int(selection) - 1
                if 0 <= index < len(material_list):
                    return material_list[index]
                else:
                    print(f"Nummer moet tussen 1 en {len(material_list)} zijn.")
            except ValueError:
                # Probeer als naam
                if selection in materials:
                    return selection
                else:
                    print(f"Onbekend materiaal: {selection}")
            
            attempts += 1
            if attempts < max_attempts:
                print(f"Nog {max_attempts - attempts} poging(en) over.")
                
        except KeyboardInterrupt:
            print("\nGeannuleerd door gebruiker.")
            sys.exit(1)
    
    raise ValueError("Te veel ongeldige invoerpogingen voor materiaal")


def _get_interactive_hours() -> Optional[float]:
    """Vraag gebruiker optioneel om handmatige printduur.
    
    Returns:
    -------
    Optional[float]
        Printduur in uren, of None voor automatische berekening
    """
    response = input("Handmatige printduur opgeven? [y/N]: ").strip().lower()
    if response in ('y', 'yes', 'ja'):
        try:
            hours_input = input("Printduur in uren: ").strip()
            return validate_positive_number(hours_input, "printduur")
        except ValueError as e:
            print(f"Ongeldige printduur: {e}. Gebruik automatische berekening.")
            return None
    return None


def _get_interactive_boolean(prompt: str) -> bool:
    """Vraag gebruiker om yes/no antwoord.
    
    Parameters:
    ----------
    prompt : str
        Vraag tekst
        
    Returns:
    -------
    bool
        True voor yes/ja, False voor no/nee
    """
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ('y', 'yes', 'ja')


def _format_calculation_output(result: Any, quiet: bool = False) -> None:
    """Format en print het calculatie resultaat.
    
    Parameters:
    ----------
    result : PriceResult
        Resultaat van calculate_sell_price()
    quiet : bool
        True voor minimale output, False voor volledig rapport
    """
    if quiet:
        # Minimale output voor scripting
        print(f"{result.sell_price:.2f}")
        return
    
    print("\n" + "=" * 50)
    print("H2D PRICE CALCULATOR - RESULTAAT")
    print("=" * 50)
    
    # Kosten breakdown
    breakdown = result.breakdown
    print(f"\nKOSTEN BREAKDOWN:")
    print(f"  Materiaal kosten:     {format_euro(breakdown.material_cost)}")
    print(f"  Variabele kosten:     {format_euro(breakdown.variable_cost)}")
    if hasattr(breakdown, 'surcharge_abrasive') and breakdown.surcharge_abrasive > 0:
        print(f"  Abrasief toeslag:     {format_euro(breakdown.surcharge_abrasive)}")
    print(f"  {'─' * 30}")
    print(f"  TOTAAL KOSTEN:        {format_euro(breakdown.total_cost)}")
    
    # Verkoop pricing
    print(f"\nPRICING RESULTAAT:")
    print(f"  Advies verkoopprijs:  {format_euro(result.sell_price)}")
    profit = result.sell_price - breakdown.total_cost
    print(f"  Winst bedrag:         {format_euro(profit)}")
    print(f"  Winstmarge:           {result.margin_pct:.1f}%")
    
    # Samenvatting
    print(f"\nSAMENVATTING:")
    markup_factor = result.sell_price / breakdown.total_cost if breakdown.total_cost > 0 else 0
    print(f"  Markup factor:        {markup_factor:.2f}x")
    print(f"  Break-even prijs:     {format_euro(breakdown.total_cost)}")
    
    print("=" * 50)


def main(argv: Optional[List[str]] = None) -> int:
    """Hoofdfunctie van de CLI interface.
    
    Parameters:
    ----------
    argv : Optional[List[str]]
        Command line argumenten, None voor sys.argv
        
    Returns:
    -------
    int
        Exit code (0 voor succes, 1 voor fout)
        
    Examples:
    --------
        >>> # Programmatisch gebruik
        >>> exit_code = main(["100", "PLA Basic", "--multicolor"])
        >>> print(f"Exit code: {exit_code}")
        
        >>> # CLI gebruik
        >>> # python cli.py 100 "PLA Basic" --hours 4
    """
    try:
        parser = _build_argument_parser()
        args = parser.parse_args(argv)
        
        # Handle utility flags
        if args.list_materials:
            _display_materials()
            return 0
        
        # Collect required parameters (interactive if missing)
        weight = args.weight
        if weight is None:
            if not args.quiet:
                print("H2D Price Calculator - Interactieve Modus")
                print("-" * 40)
            weight = _get_interactive_weight()
        
        material = args.material  
        if material is None:
            material = _get_interactive_material()
        
        # Validate material exists
        if not get_material(material):
            available = ', '.join(list_materials().keys())
            print(f"Fout: Onbekend materiaal '{material}'")
            print(f"Beschikbaar: {available}")
            return 1
        
        # Optional parameters
        hours = args.hours
        if hours is None and not any([args.abrasive, args.multicolor, args.spoed]):
            # Only ask for hours if no flags set (interactive mode)
            hours = _get_interactive_hours()
        
        # Interactive boolean flags if none set via CLI
        abrasive = args.abrasive
        multicolor = args.multicolor  
        spoed = args.spoed
        
        if not any([abrasive, multicolor, spoed]) and weight and material and not args.quiet:
            print("\nOptionele parameters:")
            multicolor = _get_interactive_boolean("Multi-kleur print?")
            abrasive = _get_interactive_boolean("Abrasief materiaal?") 
            spoed = _get_interactive_boolean("Spoedopdracht?")
        
        # Perform calculation
        result = calculate_sell_price(
            weight_g=weight,
            material=material,
            print_hours=hours,
            abrasive=abrasive,
            multicolor=multicolor,
            spoed=spoed,
        )
        
        # Output results
        _format_calculation_output(result, quiet=args.quiet)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nGeannuleerd door gebruiker.")
        return 1
    except Exception as e:
        print(f"Fout: {e}")
        if not args.quiet if 'args' in locals() else True:
            print("Gebruik --help voor meer informatie.")
        return 1


if __name__ == "__main__":
    """Entry point voor directe CLI uitvoering."""
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code) 