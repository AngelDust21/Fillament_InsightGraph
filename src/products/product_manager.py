"""
Product Manager - H2D Price Calculator
=====================================

VEREENVOUDIGD: Leest direct uit master_calculations.csv
Geen aparte JSON files meer - less is more!
"""

from typing import Dict, List, Optional, Set
from datetime import datetime
import csv
import os

from .product_model import Product


class ProductManager:
    """Vereenvoudigde ProductManager die direct uit master_calculations.csv leest.
    
    Geen aparte JSON meer - alles komt uit één centrale CSV file!
    """
    
    def __init__(self, storage_path: Optional[str] = None, auto_save: bool = True):
        """Initialiseer met pad naar master_calculations.csv"""
        # Bepaal het absolute pad naar de bedrijfsleider directory
        # Dit werkt ongeacht van waar je de GUI start!
        current_file = os.path.abspath(__file__)
        bedrijfsleider_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        
        # Nu altijd het juiste pad naar master_calculations.csv
        self.csv_path = os.path.join(bedrijfsleider_dir, "exports", "master_calculations.csv")
        self._cache: Dict[str, Product] = {}
        
        print(f"📁 Zoek CSV in: {self.csv_path}")
        
        # Laad producten uit CSV
        self._load_from_csv()
        
    def _load_from_csv(self) -> None:
        """Laad alle producten direct uit master_calculations.csv"""
        if not os.path.exists(self.csv_path):
            print(f"⚠️ CSV bestand niet gevonden: {self.csv_path}")
            return
            
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # LAAD ALLE PRODUCTEN - geen filter meer!
                    # Elke berekening is waardevol data
                        
                    # Converteer CSV row naar Product
                    product = Product(
                        name=row['product_name'],
                        description=f"3D geprint {row['product_name']}",
                        weight_g=float(row['weight']),
                        material=row['material'],
                        print_hours=float(row.get('print_hours', float(row['weight']) * 0.04)),
                        multicolor=row['multicolor'] == 'True',
                        abrasive=row['abrasive'] == 'True', 
                        rush=row['rush'] == 'True'
                    )
                    
                    # GEBRUIK GEWOON HET ID UIT DE CSV - geen overbodige formatting!
                    product.product_id = row['product_id']
                    
                    # Zet de juiste waardes
                    product.material_cost = float(row['material_cost'])
                    product.variable_cost = float(row['variable_cost'])
                    product.total_cost = float(row['total_cost'])
                    product.sell_price = float(row['sell_price'])
                    product.margin_pct = float(row['margin_pct'])
                    product.created_at = datetime.fromisoformat(row['timestamp'].replace('T', ' ').split('.')[0])
                    
                    # Voeg toe of het een test/echt product is
                    product.tags = []
                    if row.get('is_product', 'False') == 'False':
                        product.tags.append("test")
                        product.description += " (Test berekening)"
                    else:
                        product.tags.append("product")
                    
                    # Gebruik het product's eigen ID als cache key
                    self._cache[product.product_id] = product
                    
            print(f"✅ {len(self._cache)} producten/berekeningen geladen uit {self.csv_path}")
                    
        except Exception as e:
            print(f"❌ Fout bij laden CSV: {e}")
            
    def create(self, product: Product) -> Product:
        """Voeg nieuw product toe aan CSV"""
        # Voeg toe aan cache
        self._cache[product.product_id] = product
        
        # Append aan CSV
        self._append_to_csv(product)
        
        return product
        
    def _append_to_csv(self, product: Product) -> None:
        """Voeg product toe aan master_calculations.csv"""
        try:
            # Check of bestand bestaat en heeft headers
            file_exists = os.path.exists(self.csv_path)
            
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'timestamp', 'weight', 'material', 'material_cost', 'variable_cost',
                    'total_cost', 'sell_price', 'margin_pct', 'profit_amount',
                    'multicolor', 'abrasive', 'rush', 'day_of_week', 'hour_of_day',
                    'month', 'year', 'product_name', 'product_id', 'is_product'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Schrijf headers als nieuw bestand
                if not file_exists:
                    writer.writeheader()
                
                # Schrijf product data
                now = datetime.now()
                writer.writerow({
                    'timestamp': product.created_at.isoformat(),
                    'weight': product.weight_g,
                    'material': product.material,
                    'material_cost': product.material_cost,
                    'variable_cost': product.variable_cost,
                    'total_cost': product.total_cost,
                    'sell_price': product.sell_price,
                    'margin_pct': product.margin_pct,
                    'profit_amount': product.sell_price - product.total_cost,
                    'multicolor': product.multicolor,
                    'abrasive': product.abrasive,
                    'rush': product.rush,
                    'day_of_week': now.strftime('%A'),
                    'hour_of_day': now.hour,
                    'month': now.strftime('%B'),
                    'year': now.year,
                    'product_name': product.name,
                    'product_id': product.product_id,
                    'is_product': True
                })
                
        except Exception as e:
            print(f"❌ Fout bij schrijven naar CSV: {e}")
        
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Haal product op via ID"""
        return self._cache.get(product_id)
        
    def update(self, product: Product) -> Product:
        """Update = gewoon opnieuw laden van CSV (simpel!)"""
        # In deze vereenvoudigde versie doen we geen updates
        # Alles komt uit de CSV, punt uit
        return product
        
    def delete(self, product_id: str) -> bool:
        """Verwijder uit cache (niet uit CSV)"""
        if product_id in self._cache:
            del self._cache[product_id]
            return True
        return False
        
    def list_all(self) -> List[Product]:
        """Lijst alle producten uit cache"""
        return sorted(self._cache.values(), key=lambda p: p.created_at, reverse=True)
        
    def search(self, query: str) -> List[Product]:
        """Zoek producten op naam"""
        query_lower = query.lower()
        results = []
        
        for product in self._cache.values():
            if query_lower in product.name.lower():
                results.append(product)
                
        return sorted(results, key=lambda p: p.name)
        
    def filter_by_material(self, material: str) -> List[Product]:
        """Filter producten op materiaal"""
        return [p for p in self._cache.values() if p.material == material]
        
    def get_popular(self, limit: int = 10) -> List[Product]:
        """Top producten op basis van marge"""
        products = list(self._cache.values())
        products.sort(key=lambda p: p.margin_pct, reverse=True)
        return products[:limit]
        
    def get_statistics(self) -> Dict[str, any]:
        """Genereer statistieken over producten"""
        if not self._cache:
            return {
                'total_products': 0,
                'materials': {},
                'avg_weight': 0,
                'avg_price': 0,
                'avg_margin': 0,
                'total_orders': 0,
                'most_popular_product': None
            }
            
        products = list(self._cache.values())
        
        # Materiaal verdeling
        materials: Dict[str, int] = {}
        for p in products:
            materials[p.material] = materials.get(p.material, 0) + 1
            
        # Gemiddelden
        weights = [p.weight_g for p in products if p.weight_g > 0]
        prices = [p.sell_price for p in products if p.sell_price > 0]
        margins = [p.margin_pct for p in products if p.margin_pct > 0]
        
        # Meest winstgevend product
        most_profitable = max(products, key=lambda p: p.margin_pct) if products else None
        
        return {
            'total_products': len(products),
            'materials': materials,
            'avg_weight': sum(weights) / len(weights) if weights else 0,
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'avg_margin': sum(margins) / len(margins) if margins else 0,
            'total_orders': len(products),  # Elke entry is een order
            'most_popular_product': most_profitable.name if most_profitable else None
        }
        
    def export_csv(self, filepath: str) -> None:
        """Export = kopieer master_calculations.csv"""
        import shutil
        shutil.copy(self.csv_path, filepath)
        print(f"✅ Geëxporteerd naar {filepath}")
        
    def reload(self) -> None:
        """Herlaad alles uit CSV"""
        self._cache.clear()
        self._load_from_csv()
        
    # Verwijder alle JSON-gerelateerde methods
    def save_all(self) -> None:
        """Niet nodig - alles staat in CSV"""
        pass
        
    def bulk_create(self, products: List[Product]) -> List[Product]:
        """Voeg meerdere producten toe"""
        for product in products:
            self.create(product)
        return products 