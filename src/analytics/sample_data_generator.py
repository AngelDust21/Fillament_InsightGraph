"""
Sample Data Generator voor Analytics Demo
========================================

Dit script genereert realistische test data voor de analytics modules.
Wordt gebruikt om de functionaliteit te demonstreren zonder echte data.
"""

import csv
import os
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any


def generate_sample_data(num_records: int = 50) -> List[Dict[str, Any]]:
    """Genereer realistische sample data voor calculation_log.csv."""
    
    # Materialen met eigenschappen
    materials = {
        'PLA Basic': {'abrasive': False, 'base_price': 0.03},
        'PLA Premium': {'abrasive': False, 'base_price': 0.05},
        'PETG': {'abrasive': False, 'base_price': 0.04},
        'ABS': {'abrasive': False, 'base_price': 0.035},
        'Nylon': {'abrasive': False, 'base_price': 0.06},
        'TPU': {'abrasive': False, 'base_price': 0.07},
        'PC Carbon': {'abrasive': True, 'base_price': 0.12},
        'PA-CF': {'abrasive': True, 'base_price': 0.15},
        'Glass Fiber': {'abrasive': True, 'base_price': 0.10},
        'Metal Fill': {'abrasive': True, 'base_price': 0.20}
    }
    
    data = []
    
    # Start datum (30 dagen geleden)
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_records):
        # Random tijdstip binnen 30 dagen
        days_offset = random.uniform(0, 30)
        timestamp = start_date + timedelta(days=days_offset)
        
        # Random materiaal
        material = random.choice(list(materials.keys()))
        material_props = materials[material]
        
        # Random gewicht (10-500 gram)
        weight = round(random.uniform(10, 500), 1)
        
        # Print tijd (0.04 uur per gram + variatie)
        base_hours = weight * 0.04
        hours_variation = random.uniform(0.8, 1.2)
        print_hours = round(base_hours * hours_variation, 2)
        
        # Bereken kosten
        material_cost = weight * material_props['base_price']
        variable_cost = print_hours * 3.5  # Gemiddelde variabele kosten
        
        # Opties
        multicolor = random.random() < 0.2  # 20% kans
        abrasive = material_props['abrasive']
        rush = random.random() < 0.1  # 10% kans
        
        # Extra kosten
        if abrasive:
            variable_cost += print_hours * 0.5
        
        total_cost = material_cost + variable_cost
        
        # Verkoopprijs (markup)
        sell_price = total_cost * random.uniform(2.2, 3.5)
        if multicolor:
            sell_price += random.uniform(15, 30)
        if rush:
            sell_price *= 1.25
            
        margin_pct = ((sell_price - total_cost) / total_cost) * 100
        
        # Configuratie (realistische waarden)
        config = {
            'printer_power': 1.05,
            'energy_price': 0.30,
            'labour_cost': 23.50,
            'monitoring_pct': 10,
            'maintenance_cost': 0.0765,
            'overhead_year': 6669,
            'annual_hours': 2000,
            'markup_material': 200,
            'markup_variable': 150,
            'spoed_surcharge': 25,
            'abrasive_surcharge': 0.50,
            'color_fee_min': 15,
            'color_fee_max': 30,
            'auto_time_per_gram': 0.04
        }
        
        # Voeg record toe
        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'weight': weight,
            'material': material,
            'print_hours': print_hours,
            'material_cost': round(material_cost, 2),
            'variable_cost': round(variable_cost, 2),
            'total_cost': round(total_cost, 2),
            'sell_price': round(sell_price, 2),
            'margin_pct': round(margin_pct, 1),
            'multicolor': multicolor,
            'abrasive': abrasive,
            'rush': rush,
            'printer_power': config['printer_power'],
            'energy_price': config['energy_price'],
            'labour_cost': config['labour_cost'],
            'monitoring_pct': config['monitoring_pct'],
            'maintenance_cost': config['maintenance_cost'],
            'overhead_year': config['overhead_year'],
            'annual_hours': config['annual_hours'],
            'markup_material': config['markup_material'],
            'markup_variable': config['markup_variable'],
            'spoed_surcharge': config['spoed_surcharge'],
            'abrasive_surcharge': config['abrasive_surcharge'],
            'color_fee_min': config['color_fee_min'],
            'color_fee_max': config['color_fee_max'],
            'auto_time_per_gram': config['auto_time_per_gram'],
            'auto_hours_used': True
        })
    
    return data


def write_sample_data(output_file: str = 'calculation_log.csv') -> None:
    """Schrijf sample data naar CSV bestand."""
    # Genereer data
    data = generate_sample_data(50)
    
    # Bepaal volledig pad
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_path = os.path.join(base_dir, output_file)
    
    # Schrijf naar CSV
    if data:
        fieldnames = list(data[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"✅ Sample data geschreven naar: {output_path}")
        print(f"   Aantal records: {len(data)}")
        
        # Toon statistieken
        abrasive_count = sum(1 for d in data if d['abrasive'])
        print(f"   Abrasieve prints: {abrasive_count} ({abrasive_count/len(data)*100:.0f}%)")
        
        total_hours = sum(d['print_hours'] for d in data)
        abrasive_hours = sum(d['print_hours'] for d in data if d['abrasive'])
        print(f"   Totale print uren: {total_hours:.1f}")
        print(f"   Abrasieve uren: {abrasive_hours:.1f}")
        

if __name__ == "__main__":
    write_sample_data() 