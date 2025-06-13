"""
Data Manager - H2D Price Calculator
==================================

Dit module beheert alle data import/export operaties en analyses.
Het zorgt voor een consistente workflow van:
1. Berekeningen exporteren naar CSV
2. CSV bestanden organiseren in export folder
3. Historische data importeren voor analyse
4. Analyses uitvoeren op verzamelde data

Folder Structuur:
----------------
exports/
├── berekeningen/       # Individuele berekeningen
│   └── calc_YYYYMMDD_HHMMSS.csv
├── producten/          # Product exports
│   └── products_YYYYMMDD_HHMMSS.csv
└── analyses/           # Analyse resultaten
    └── analysis_YYYYMMDD.csv
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from collections import defaultdict

class DataManager:
    """Centrale manager voor alle data operaties.
    
    Deze klasse beheert:
    - Export van berekeningen naar gestructureerde CSV files
    - Import van historische data
    - Analyse van trends en statistieken
    - Rapport generatie
    """
    
    def __init__(self, base_dir: str = "exports"):
        """Initialiseer DataManager met folder structuur.
        
        Parameters:
        ----------
        base_dir : str
            Basis directory voor alle exports (default: "exports")
        """
        self.base_dir = Path(base_dir)
        
        # Maak subdirectories
        self.calc_dir = self.base_dir / "berekeningen"
        self.product_dir = self.base_dir / "producten"
        self.analysis_dir = self.base_dir / "analyses"
        
        # Ensure alle directories bestaan
        for directory in [self.calc_dir, self.product_dir, self.analysis_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        # Master CSV voor alle berekeningen
        self.master_calc_file = self.base_dir / "master_calculations.csv"
        
    def export_calculation(self, calc_data: Dict[str, Any]) -> str:
        """Export een enkele berekening naar CSV.
        
        Parameters:
        ----------
        calc_data : Dict[str, Any]
            Dictionary met berekening data:
            - weight: Gewicht in gram
            - material: Materiaal naam
            - material_cost: Materiaal kosten
            - variable_cost: Variabele kosten
            - total_cost: Totale kosten
            - sell_price: Verkoopprijs
            - margin_pct: Winstmarge percentage
            - timestamp: Tijdstip berekening
            - options: Dict met multicolor, abrasive, rush flags
            
        Returns:
        -------
        str
            Pad naar opgeslagen CSV bestand
        """
        # Timestamp voor bestandsnaam
        timestamp = datetime.now()
        filename = f"calc_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = self.calc_dir / filename
        
        # Voeg extra metadata toe
        enhanced_data = calc_data.copy()
        enhanced_data['export_timestamp'] = timestamp.isoformat()
        enhanced_data['day_of_week'] = timestamp.strftime('%A')
        enhanced_data['hour_of_day'] = timestamp.hour
        enhanced_data['month'] = timestamp.strftime('%B')
        enhanced_data['year'] = timestamp.year
        
        # Extract options indien aanwezig
        options = calc_data.get('options', {})
        enhanced_data['multicolor'] = options.get('multicolor', False)
        enhanced_data['abrasive'] = options.get('abrasive', False)
        enhanced_data['rush'] = options.get('rush', False)
        
        # Schrijf individuele CSV
        headers = [
            'timestamp', 'weight', 'material', 'material_cost', 'variable_cost',
            'total_cost', 'sell_price', 'margin_pct', 'profit_amount',
            'multicolor', 'abrasive', 'rush', 'day_of_week', 'hour_of_day',
            'month', 'year', 'product_name', 'product_id', 'is_product'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow({
                'timestamp': enhanced_data.get('export_timestamp', ''),
                'weight': enhanced_data.get('weight', 0),
                'material': enhanced_data.get('material', ''),
                'material_cost': round(enhanced_data.get('material_cost', 0), 2),
                'variable_cost': round(enhanced_data.get('variable_cost', 0), 2),
                'total_cost': round(enhanced_data.get('total_cost', 0), 2),
                'sell_price': round(enhanced_data.get('sell_price', 0), 2),
                'margin_pct': round(enhanced_data.get('margin_pct', 0), 1),
                'profit_amount': round(enhanced_data.get('sell_price', 0) - enhanced_data.get('total_cost', 0), 2),
                'multicolor': enhanced_data.get('multicolor', False),
                'abrasive': enhanced_data.get('abrasive', False),
                'rush': enhanced_data.get('rush', False),
                'day_of_week': enhanced_data.get('day_of_week', ''),
                'hour_of_day': enhanced_data.get('hour_of_day', 0),
                'month': enhanced_data.get('month', ''),
                'year': enhanced_data.get('year', 0),
                'product_name': enhanced_data.get('product_name', ''),
                'product_id': enhanced_data.get('product_id', ''),
                'is_product': enhanced_data.get('is_product', False)
            })
            
        # Voeg ook toe aan master file
        self._append_to_master(enhanced_data)
        
        return str(filepath)
        
    def log_calculation_simple(self, calc_data: Dict[str, Any]) -> None:
        """Log een uitgebreide berekening naar het logboek (calculation_log.csv).
        
        Dit is een uitgebreid logboek voor debugging en analyse, met ALLE details
        behalve product naam/ID (die zijn voor master database).
        
        Parameters:
        ----------
        calc_data : Dict[str, Any]
            Dictionary met ALLE berekening data inclusief configuratie
        """
        log_file = self.base_dir / "calculation_log.csv"
        print(f"DEBUG: Logging naar: {log_file.absolute()}")
        
        # Check of file bestaat voor header
        file_exists = log_file.exists()
        
        # Extract alle data voor uitgebreid logboek
        timestamp = datetime.now()
        
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Uitgebreide headers voor debugging
            headers = [
                'timestamp', 'date', 'time', 'day_of_week', 'hour_of_day',
                'weight_g', 'material', 'print_hours',
                'material_cost', 'variable_cost', 'total_cost', 'sell_price', 
                'margin_pct', 'profit_amount',
                'multicolor', 'abrasive', 'rush',
                'printer_power_kw', 'energy_price', 'labour_cost', 'monitoring_pct',
                'maintenance_cost', 'overhead_year', 'annual_hours',
                'markup_material', 'markup_variable', 'spoed_surcharge',
                'abrasive_surcharge', 'color_fee_min', 'color_fee_max',
                'auto_time_per_gram', 'auto_hours_used'
            ]
            
            # Schrijf header alleen bij nieuwe file
            if not file_exists:
                writer.writerow(headers)
            
            # Extract options
            options = calc_data.get('options', {})
            config = calc_data.get('config', {})
            
            # Schrijf uitgebreide log entry
            writer.writerow([
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                timestamp.strftime('%Y-%m-%d'),
                timestamp.strftime('%H:%M:%S'),
                timestamp.strftime('%A'),
                timestamp.hour,
                round(calc_data.get('weight', 0), 1),
                calc_data.get('material', ''),
                round(calc_data.get('print_hours', 0), 2),
                round(calc_data.get('material_cost', 0), 2),
                round(calc_data.get('variable_cost', 0), 2),
                round(calc_data.get('total_cost', 0), 2),
                round(calc_data.get('sell_price', 0), 2),
                round(calc_data.get('margin_pct', 0), 1),
                round(calc_data.get('sell_price', 0) - calc_data.get('total_cost', 0), 2),
                options.get('multicolor', False),
                options.get('abrasive', False),
                options.get('rush', False),
                config.get('printer_power', ''),
                config.get('energy_price', ''),
                config.get('labour_cost', ''),
                config.get('monitoring_pct', ''),
                config.get('maintenance_cost', ''),
                config.get('overhead_year', ''),
                config.get('annual_hours', ''),
                config.get('markup_material', ''),
                config.get('markup_variable', ''),
                config.get('spoed_surcharge', ''),
                config.get('abrasive_surcharge', ''),
                config.get('color_fee_min', ''),
                config.get('color_fee_max', ''),
                config.get('auto_time_per_gram', ''),
                calc_data.get('auto_hours_used', False)
            ])
        
    def export_product(self, product_data: Dict[str, Any]) -> None:
        """Export een product als berekening naar het master bestand.
        
        Wanneer een product wordt opgeslagen, wordt het ook toegevoegd
        aan het master bestand zodat het meegenomen wordt in analyses.
        
        Parameters:
        ----------
        product_data : Dict[str, Any]
            Product data om te exporteren
        """
        # Converteer product data naar berekening formaat
        calc_data = {
            'weight': product_data.get('weight_g', 0),
            'material': product_data.get('material', ''),
            'material_cost': product_data.get('material_cost', 0),
            'variable_cost': product_data.get('variable_cost', 0),
            'total_cost': product_data.get('total_cost', 0),
            'sell_price': product_data.get('sell_price', 0),
            'margin_pct': product_data.get('margin_pct', 0),
            'options': {
                'multicolor': product_data.get('multicolor', False),
                'abrasive': product_data.get('abrasive', False),
                'rush': product_data.get('rush', False)
            },
            'product_name': product_data.get('name', ''),  # Extra veld voor product naam
            'product_id': product_data.get('product_id', ''),  # Extra veld voor product ID
            'is_product': True  # Markeer dit als een product, niet een losse berekening
        }
        
        # Gebruik de bestaande export functie
        self.export_calculation(calc_data)
        
    def _append_to_master(self, calc_data: Dict[str, Any]) -> None:
        """Voeg berekening toe aan master CSV bestand.
        
        Dit bestand bevat ALLE berekeningen voor makkelijke analyse.
        """
        headers = [
            'timestamp', 'weight', 'material', 'material_cost', 'variable_cost',
            'total_cost', 'sell_price', 'margin_pct', 'profit_amount',
            'multicolor', 'abrasive', 'rush', 'day_of_week', 'hour_of_day',
            'month', 'year', 'product_name', 'product_id', 'is_product'
        ]
        
        # Check of file bestaat
        file_exists = self.master_calc_file.exists()
        
        with open(self.master_calc_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Schrijf header alleen bij nieuwe file
            if not file_exists:
                writer.writeheader()
                
            writer.writerow({
                'timestamp': calc_data.get('export_timestamp', ''),
                'weight': calc_data.get('weight', 0),
                'material': calc_data.get('material', ''),
                'material_cost': round(calc_data.get('material_cost', 0), 2),
                'variable_cost': round(calc_data.get('variable_cost', 0), 2),
                'total_cost': round(calc_data.get('total_cost', 0), 2),
                'sell_price': round(calc_data.get('sell_price', 0), 2),
                'margin_pct': round(calc_data.get('margin_pct', 0), 1),
                'profit_amount': round(calc_data.get('sell_price', 0) - calc_data.get('total_cost', 0), 2),
                'multicolor': calc_data.get('multicolor', False),
                'abrasive': calc_data.get('abrasive', False),
                'rush': calc_data.get('rush', False),
                'day_of_week': calc_data.get('day_of_week', ''),
                'hour_of_day': calc_data.get('hour_of_day', 0),
                'month': calc_data.get('month', ''),
                'year': calc_data.get('year', 0),
                'product_name': calc_data.get('product_name', ''),
                'product_id': calc_data.get('product_id', ''),
                'is_product': calc_data.get('is_product', False)
            })
            
    def import_calculations(self, from_master: bool = True) -> pd.DataFrame:
        """Importeer alle berekeningen voor analyse.
        
        Parameters:
        ----------
        from_master : bool
            True: Laad van master file (sneller)
            False: Combineer alle individuele CSV files
            
        Returns:
        -------
        pd.DataFrame
            DataFrame met alle berekeningen
        """
        if from_master and self.master_calc_file.exists():
            return pd.read_csv(self.master_calc_file)
        else:
            # Combineer alle individuele CSV files
            all_data = []
            
            for csv_file in self.calc_dir.glob("calc_*.csv"):
                try:
                    df = pd.read_csv(csv_file)
                    all_data.append(df)
                except Exception as e:
                    print(f"Waarschuwing: Kon {csv_file} niet laden: {e}")
                    
            if all_data:
                combined_df = pd.concat(all_data, ignore_index=True)
                # Sorteer op timestamp
                combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
                combined_df.sort_values('timestamp', inplace=True)
                return combined_df
            else:
                # Return lege DataFrame met juiste kolommen
                return pd.DataFrame(columns=[
                    'timestamp', 'weight', 'material', 'material_cost', 
                    'variable_cost', 'total_cost', 'sell_price', 'margin_pct',
                    'profit_amount', 'multicolor', 'abrasive', 'rush',
                    'day_of_week', 'hour_of_day', 'month', 'year', 'product_name', 'product_id', 'is_product'
                ])
                
    def analyze_calculations(self) -> Dict[str, Any]:
        """Voer uitgebreide analyse uit op alle berekeningen.
        
        Analyses:
        --------
        - Totaal aantal berekeningen
        - Populairste materialen
        - Gemiddelde winstmarge per materiaal
        - Trend analyse (prijzen over tijd)
        - Opties gebruik (multicolor, abrasive, rush)
        - Beste/slechtste marges
        - Dag/uur patronen
        
        Returns:
        -------
        Dict[str, Any]
            Dictionary met alle analyse resultaten
        """
        df = self.import_calculations()
        
        if df.empty:
            return {
                'error': 'Geen data beschikbaar voor analyse',
                'total_calculations': 0
            }
            
        # Basis statistieken
        analysis = {
            'total_calculations': len(df),
            'date_range': {
                'first': df['timestamp'].min() if not df.empty else None,
                'last': df['timestamp'].max() if not df.empty else None
            },
            'summary_stats': {
                'avg_weight': round(df['weight'].mean(), 1),
                'avg_cost': round(df['total_cost'].mean(), 2),
                'avg_price': round(df['sell_price'].mean(), 2),
                'avg_margin': round(df['margin_pct'].mean(), 1),
                'total_revenue': round(df['sell_price'].sum(), 2),
                'total_profit': round(df['profit_amount'].sum(), 2)
            }
        }
        
        # Splits data in producten en losse berekeningen
        if 'is_product' in df.columns:
            products_df = df[df['is_product'] == True]
            calculations_df = df[df['is_product'] != True]
            
            analysis['product_stats'] = {
                'total_products': len(products_df),
                'unique_products': products_df['product_id'].nunique() if 'product_id' in products_df else 0,
                'product_revenue': round(products_df['sell_price'].sum(), 2) if len(products_df) > 0 else 0,
                'avg_product_price': round(products_df['sell_price'].mean(), 2) if len(products_df) > 0 else 0
            }
            
            analysis['calculation_stats'] = {
                'total_calculations': len(calculations_df),
                'calculation_revenue': round(calculations_df['sell_price'].sum(), 2) if len(calculations_df) > 0 else 0
            }
            
            # Top producten
            if len(products_df) > 0 and 'product_name' in products_df:
                top_products = products_df.groupby('product_name').agg({
                    'sell_price': 'sum',
                    'product_name': 'count'
                }).rename(columns={'product_name': 'count', 'sell_price': 'revenue'})
                top_products = top_products.sort_values('revenue', ascending=False).head(5)
                analysis['top_products'] = top_products.to_dict('index')
        
        # Materiaal analyse
        material_stats = df.groupby('material').agg({
            'material': 'count',
            'margin_pct': 'mean',
            'profit_amount': 'sum',
            'weight': 'mean'
        }).round(2)
        
        material_stats.columns = ['count', 'avg_margin', 'total_profit', 'avg_weight']
        analysis['material_analysis'] = material_stats.to_dict('index')
        
        # Top 5 populairste materialen
        analysis['top_materials'] = df['material'].value_counts().head(5).to_dict()
        
        # Opties gebruik
        analysis['options_usage'] = {
            'multicolor': df['multicolor'].sum() if 'multicolor' in df else 0,
            'abrasive': df['abrasive'].sum() if 'abrasive' in df else 0,
            'rush': df['rush'].sum() if 'rush' in df else 0
        }
        
        # Tijd patronen
        if 'hour_of_day' in df:
            analysis['hourly_pattern'] = df.groupby('hour_of_day').size().to_dict()
            
        if 'day_of_week' in df:
            analysis['daily_pattern'] = df.groupby('day_of_week').size().to_dict()
            
        # Beste en slechtste marges
        analysis['best_margins'] = df.nlargest(5, 'margin_pct')[
            ['material', 'weight', 'margin_pct', 'sell_price']
        ].to_dict('records')
        
        analysis['worst_margins'] = df.nsmallest(5, 'margin_pct')[
            ['material', 'weight', 'margin_pct', 'sell_price']
        ].to_dict('records')
        
        # Trend analyse (laatste 30 berekeningen)
        recent_df = df.tail(30)
        if len(recent_df) > 1:
            analysis['recent_trend'] = {
                'margin_trend': 'stijgend' if recent_df['margin_pct'].iloc[-1] > recent_df['margin_pct'].iloc[0] else 'dalend',
                'avg_margin_recent': round(recent_df['margin_pct'].mean(), 1),
                'avg_price_recent': round(recent_df['sell_price'].mean(), 2)
            }
            
        # Sla analyse resultaten op
        self._save_analysis_report(analysis)
        
        return analysis
        
    def _save_analysis_report(self, analysis: Dict[str, Any]) -> str:
        """Sla analyse rapport op als JSON en leesbaar tekstbestand.
        
        Parameters:
        ----------
        analysis : Dict[str, Any]
            Analyse resultaten dictionary
            
        Returns:
        -------
        str
            Pad naar opgeslagen rapport
        """
        timestamp = datetime.now()
        
        # JSON voor programmatisch gebruik
        json_file = self.analysis_dir / f"analysis_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, default=str)
            
        # Tekst rapport voor menselijke leesbaarheid
        txt_file = self.analysis_dir / f"rapport_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("H2D PRICE CALCULATOR - ANALYSE RAPPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Gegenereerd op: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Basis statistieken
            f.write("SAMENVATTING\n")
            f.write("-" * 30 + "\n")
            f.write(f"Totaal aantal berekeningen: {analysis['total_calculations']}\n")
            
            if analysis['total_calculations'] > 0:
                stats = analysis['summary_stats']
                f.write(f"Gemiddeld gewicht: {stats['avg_weight']}g\n")
                f.write(f"Gemiddelde kostprijs: €{stats['avg_cost']}\n")
                f.write(f"Gemiddelde verkoopprijs: €{stats['avg_price']}\n")
                f.write(f"Gemiddelde winstmarge: {stats['avg_margin']}%\n")
                f.write(f"Totale omzet: €{stats['total_revenue']}\n")
                f.write(f"Totale winst: €{stats['total_profit']}\n\n")
                
                # Top materialen
                f.write("TOP 5 MATERIALEN\n")
                f.write("-" * 30 + "\n")
                for material, count in list(analysis.get('top_materials', {}).items())[:5]:
                    f.write(f"{material}: {count} keer gebruikt\n")
                    
                f.write("\n")
                
                # Opties gebruik
                f.write("OPTIES GEBRUIK\n")
                f.write("-" * 30 + "\n")
                options = analysis.get('options_usage', {})
                f.write(f"Multicolor prints: {options.get('multicolor', 0)}\n")
                f.write(f"Abrasieve materialen: {options.get('abrasive', 0)}\n")
                f.write(f"Spoedopdrachten: {options.get('rush', 0)}\n")
                
        return str(txt_file)
        
    def export_analysis_to_excel(self, analysis: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Export analyse naar Excel bestand met meerdere sheets.
        
        Parameters:
        ----------
        analysis : Dict[str, Any]
            Analyse resultaten
        filename : Optional[str]
            Output bestandsnaam
            
        Returns:
        -------
        str
            Pad naar Excel bestand
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analyse_{timestamp}.xlsx"
            
        filepath = self.analysis_dir / filename
        
        # Probeer pandas ExcelWriter
        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Samenvatting sheet
                summary_df = pd.DataFrame([analysis['summary_stats']])
                summary_df.to_excel(writer, sheet_name='Samenvatting', index=False)
                
                # Materiaal analyse sheet
                if 'material_analysis' in analysis:
                    material_df = pd.DataFrame.from_dict(
                        analysis['material_analysis'], 
                        orient='index'
                    )
                    material_df.to_excel(writer, sheet_name='Materiaal Analyse')
                    
                # Beste marges sheet
                if 'best_margins' in analysis:
                    best_df = pd.DataFrame(analysis['best_margins'])
                    best_df.to_excel(writer, sheet_name='Beste Marges', index=False)
                    
                # Slechtste marges sheet
                if 'worst_margins' in analysis:
                    worst_df = pd.DataFrame(analysis['worst_margins'])
                    worst_df.to_excel(writer, sheet_name='Slechtste Marges', index=False)
                    
            return str(filepath)
            
        except ImportError:
            # Fallback naar CSV als openpyxl niet beschikbaar is
            csv_file = filepath.with_suffix('.csv')
            summary_df = pd.DataFrame([analysis['summary_stats']])
            summary_df.to_csv(csv_file, index=False)
            return str(csv_file)
            
    def get_export_statistics(self) -> Dict[str, Any]:
        """Haal statistieken op over opgeslagen exports.
        
        Returns:
        -------
        Dict[str, Any]
            Statistieken over export bestanden
        """
        stats = {
            'total_calculations': len(list(self.calc_dir.glob("calc_*.csv"))),
            'total_products': len(list(self.product_dir.glob("products_*.csv"))),
            'total_analyses': len(list(self.analysis_dir.glob("analysis_*.json"))),
            'master_file_exists': self.master_calc_file.exists(),
            'total_size_mb': 0
        }
        
        # Bereken totale grootte
        total_size = 0
        for directory in [self.calc_dir, self.product_dir, self.analysis_dir]:
            for file in directory.rglob("*"):
                if file.is_file():
                    total_size += file.stat().st_size
                    
        stats['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        return stats
        
    def cleanup_old_exports(self, days_to_keep: int = 30) -> int:
        """Verwijder oude export bestanden.
        
        Parameters:
        ----------
        days_to_keep : int
            Aantal dagen om exports te bewaren
            
        Returns:
        -------
        int
            Aantal verwijderde bestanden
        """
        count = 0
        cutoff = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        for directory in [self.calc_dir, self.product_dir, self.analysis_dir]:
            for file in directory.glob("*"):
                if file.is_file() and file.stat().st_mtime < cutoff:
                    # Bewaar master file altijd
                    if file != self.master_calc_file:
                        file.unlink()
                        count += 1
                        
        return count


# Voor makkelijke imports
__all__ = ['DataManager'] 