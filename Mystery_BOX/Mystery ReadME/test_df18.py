"""
Test script om DF18 data te controleren
"""

import sys
import os
sys.path.append('scripts')

from data_analyse import (
    df18_vip_klanten, 
    df18_loyale_klanten, 
    df18_frequente_klanten, 
    df18_rising_stars, 
    df18_te_reactiveren
)

print("=== DF18 DATA CONTROLE ===")
print(f"\nVIP Klanten: {len(df18_vip_klanten)} klanten")
if len(df18_vip_klanten) > 0:
    print("Top 3 VIP klanten:")
    print(df18_vip_klanten[['totale_uitgaven', 'aantal_orders']].head(3))

print(f"\nLoyale Klanten: {len(df18_loyale_klanten)} klanten")
if len(df18_loyale_klanten) > 0:
    print("Top 3 loyale klanten:")
    print(df18_loyale_klanten[['jaren_klant', 'aantal_orders']].head(3))

print(f"\nFrequente Bestellers: {len(df18_frequente_klanten)} klanten")
print(f"\nRising Stars: {len(df18_rising_stars)} klanten")
print(f"\nTe Reactiveren: {len(df18_te_reactiveren)} klanten")

print("\n=== TEST VISUALISATIE ===")
from visualisaties import gf18_klanten_belonen
import matplotlib.pyplot as plt

fig = gf18_klanten_belonen()
plt.show() 