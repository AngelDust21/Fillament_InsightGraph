"""
Test Data Generator voor calculation_log.csv
===========================================

Genereert realistische test data voor de analytics modules
met het nieuwe uitgebreide logging formaat (31 kolommen).
"""

import csv
import os
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any


def generate_calculation_log_data(num_records: int = 100) -> List[Dict[str, Any]]:
    """Genereer realistische test data voor calculation_log.csv."""
    
    # Materialen met eigenschappen
    materials = {
        'PLA Basic': {'abrasive': False, 'base_price': 0.014},
        'PLA Premium': {'abrasive': False, 'base_price': 0.03},
        'PLA Silk': {'abrasive': False, 'base_price': 0.03},
        'PLA Wood': {'abrasive': False, 'base_price': 0.02},
        'PLA Matte': {'abrasive': False, 'base_price': 0.015},
        'PETG Basic': {'abrasive': False, 'base_price': 0.014},
        'PETG-CF': {'abrasive': True, 'base_price': 0.024},
        'ABS': {'abrasive': False, 'base_price': 0.016},
        'ASA': {'abrasive': False, 'base_price': 0.02},
        'TPU 95A': {'abrasive': False, 'base_price': 0.03},
        'Nylon': {'abrasive': False, 'base_price': 0.04},
        'PC': {'abrasive': False, 'base_price': 0.02},
        'PA-CF': {'abrasive': True, 'base_price': 0.022},
        'PA12-CF': {'abrasive': True, 'base_price': 0.024},
        'PC Carbon': {'abrasive': True, 'base_price': 0.03},
        'Glass Fiber': {'abrasive': True, 'base_price': 0.025}
    }
    
    data = []
    
    # Start datum (30 dagen geleden)
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(num_records):
        # Random tijdstip binnen 30 dagen
        days_offset = random.uniform(0, 30)
        timestamp = start_date + timedelta(days=days_offset)
        
        # Voeg wat variatie toe in tijdstippen (werkuren hebben hogere kans)
        hour = random.choices(
            range(24),
            weights=[1,1,1,1,1,1,2,3,5,8,8,8,6,8,8,8,7,5,3,2,1,1,1,1],
            k=1
        )[0]
        timestamp = timestamp.replace(hour=hour, minute=random.randint(0, 59))
        
        # Random materiaal (meer kans op normale materialen)
        if random.random() < 0.7:  # 70% normale materialen
            material = random.choice([m for m, props in materials.items() if not props['abrasive']])
        else:  # 30% abrasieve materialen
            material = random.choice([m for m, props in materials.items() if props['abrasive']])
        
        material_props = materials[material]
        
        # Random gewicht (realistische verdeling)
        weight_ranges = [
            (10, 50, 0.3),    # Klein: 30%
            (50, 150, 0.4),   # Medium: 40%
            (150, 300, 0.2),  # Groot: 20%
            (300, 600, 0.1)   # Extra groot: 10%
        ]
        
        weight_range = random.choices(
            weight_ranges,
            weights=[w[2] for w in weight_ranges],
            k=1
        )[0]
        weight = round(random.uniform(weight_range[0], weight_range[1]), 1)
        
        # Print tijd (variatie op basis van complexiteit)
        if random.random() < 0.8:  # 80% auto tijd
            auto_hours_used = True
            hours_per_gram = random.uniform(0.015, 0.025)  # Variatie in print snelheid
            print_hours = round(weight * hours_per_gram, 2)
        else:  # 20% manual tijd (complexe prints)
            auto_hours_used = False
            base_hours = weight * 0.02
            complexity_factor = random.uniform(1.2, 2.5)
            print_hours = round(base_hours * complexity_factor, 2)
        
        # Configuratie parameters (realistische waarden met kleine variaties)
        config = {
            'printer_power': round(random.uniform(1.0, 1.1), 2),
            'energy_price': round(random.uniform(0.28, 0.32), 2),
            'labour_cost': round(random.uniform(23.0, 35.0), 1),
            'monitoring_pct': round(random.uniform(8, 12), 0),
            'maintenance_cost': round(random.uniform(0.07, 0.10), 3),
            'overhead_year': round(random.uniform(900, 1200), 0),
            'annual_hours': 2000,
            'markup_material': round(random.uniform(80, 120), 0),
            'markup_variable': round(random.uniform(60, 80), 0),
            'spoed_surcharge': round(random.uniform(25, 50), 0),
            'abrasive_surcharge': 0.5,
            'color_fee_min': round(random.uniform(10, 15), 0),
            'color_fee_max': round(random.uniform(15, 20), 0),
            'auto_time_per_gram': round(hours_per_gram if auto_hours_used else 0.02, 3)
        }
        
        # Bereken kosten
        material_cost = weight * material_props['base_price']
        
        # Variabele kosten berekening
        energy_cost_per_hour = config['printer_power'] * config['energy_price']
        monitoring_cost_per_hour = config['labour_cost'] * (config['monitoring_pct'] / 100)
        overhead_cost_per_hour = config['overhead_year'] / config['annual_hours']
        
        variable_cost_per_hour = (
            energy_cost_per_hour + 
            config['maintenance_cost'] + 
            monitoring_cost_per_hour + 
            overhead_cost_per_hour
        )
        
        variable_cost = variable_cost_per_hour * print_hours
        
        # Abrasief toeslag
        if material_props['abrasive']:
            variable_cost += config['abrasive_surcharge'] * print_hours
        
        # Opties (realistische kansen)
        multicolor = random.random() < 0.15  # 15% multicolor
        rush = random.random() < 0.08  # 8% spoed
        
        total_cost = material_cost + variable_cost
        
        # Verkoopprijs berekening
        sell_price = (
            (material_cost * (1 + config['markup_material'] / 100)) + 
            (variable_cost * (1 + config['markup_variable'] / 100))
        )
        
        # Multicolor toeslag
        if multicolor:
            setup_fee = (config['color_fee_min'] + config['color_fee_max']) / 2
            sell_price += setup_fee
        
        # Spoedtoeslag
        if rush:
            sell_price *= (1 + config['spoed_surcharge'] / 100)
        
        # Bereken marge
        margin_pct = ((sell_price - total_cost) / total_cost) * 100 if total_cost > 0 else 0
        profit_amount = sell_price - total_cost
        
        # Maak record
        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'date': timestamp.strftime('%Y-%m-%d'),
            'time': timestamp.strftime('%H:%M:%S'),
            'day_of_week': timestamp.strftime('%A'),
            'hour_of_day': timestamp.hour,
            'weight_g': weight,
            'material': material,
            'print_hours': print_hours,
            'material_cost': round(material_cost, 2),
            'variable_cost': round(variable_cost, 2),
            'total_cost': round(total_cost, 2),
            'sell_price': round(sell_price, 2),
            'margin_pct': round(margin_pct, 1),
            'profit_amount': round(profit_amount, 2),
            'multicolor': multicolor,
            'abrasive': material_props['abrasive'],
            'rush': rush,
            'printer_power_kw': config['printer_power'],
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
            'auto_hours_used': auto_hours_used
        })
    
    # Sorteer op timestamp
    data.sort(key=lambda x: x['timestamp'])
    
    return data


def write_calculation_log(num_records: int = 100):
    """Schrijf test data naar calculation_log.csv."""
    # Genereer data
    data = generate_calculation_log_data(num_records)
    
    # Bepaal pad naar exports folder
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_path = os.path.join(base_dir, 'exports', 'calculation_log.csv')
    
    # Maak exports folder als die niet bestaat
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Schrijf naar CSV
    if data:
        fieldnames = list(data[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
        print(f"✅ Test data geschreven naar: {output_path}")
        print(f"   Aantal records: {len(data)}")
        
        # Toon statistieken
        abrasive_count = sum(1 for d in data if d['abrasive'])
        multicolor_count = sum(1 for d in data if d['multicolor'])
        rush_count = sum(1 for d in data if d['rush'])
        
        print(f"\n📊 Statistieken:")
        print(f"   Abrasieve prints: {abrasive_count} ({abrasive_count/len(data)*100:.0f}%)")
        print(f"   Multicolor prints: {multicolor_count} ({multicolor_count/len(data)*100:.0f}%)")
        print(f"   Spoed orders: {rush_count} ({rush_count/len(data)*100:.0f}%)")
        
        total_hours = sum(d['print_hours'] for d in data)
        abrasive_hours = sum(d['print_hours'] for d in data if d['abrasive'])
        print(f"\n⏱️ Tijden:")
        print(f"   Totale print uren: {total_hours:.1f}")
        print(f"   Abrasieve uren: {abrasive_hours:.1f}")
        print(f"   Percentage abrasief: {abrasive_hours/total_hours*100:.1f}%")
        
        avg_margin = sum(d['margin_pct'] for d in data) / len(data)
        total_profit = sum(d['profit_amount'] for d in data)
        print(f"\n💰 Financieel:")
        print(f"   Gemiddelde marge: {avg_margin:.1f}%")
        print(f"   Totale winst: €{total_profit:.2f}")
        

if __name__ == "__main__":
    # Genereer 100 test records
    write_calculation_log(100) 