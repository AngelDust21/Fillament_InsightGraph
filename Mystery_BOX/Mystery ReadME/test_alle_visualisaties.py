"""
Test script om alle visualisaties te controleren op fouten
"""

import sys
import os
sys.path.append('scripts')

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend voor testen
import matplotlib.pyplot as plt

# Importeer alle visualisatie functies
from visualisaties import (
    gf1_top_producten_barplot,
    gf2_omzet_tijdlijn,
    gf3_geografische_spreiding,
    gf4_klanten_segmentatie_matrix,
    gf5_bestellingen_heatmap,
    gf6_product_categorie_donut,
    gf7_betaalmethode_analyse,
    gf8_kaas_brood_combinaties,
    gf9_verkooppatronen,
    gf10_prijsevolutie,
    gf11_toekomstvoorspelling,
    gf12_lange_termijn,
    gf13_seizoens_feestdagen,
    gf14_leadtime_analyse,
    gf15_product_combinaties,
    gf16_klant_lifetime_value,
    gf17_winstgevendheid,
    gf18_klanten_belonen
)

# Test alle visualisaties
visualisaties = [
    ("GF1", gf1_top_producten_barplot),
    ("GF2", gf2_omzet_tijdlijn),
    ("GF3", gf3_geografische_spreiding),
    ("GF4", gf4_klanten_segmentatie_matrix),
    ("GF5", gf5_bestellingen_heatmap),
    ("GF6", gf6_product_categorie_donut),
    ("GF7", gf7_betaalmethode_analyse),
    ("GF8", gf8_kaas_brood_combinaties),
    ("GF9", gf9_verkooppatronen),
    ("GF10", gf10_prijsevolutie),
    ("GF11", gf11_toekomstvoorspelling),
    ("GF12", gf12_lange_termijn),
    ("GF13", gf13_seizoens_feestdagen),
    ("GF14", gf14_leadtime_analyse),
    ("GF15", gf15_product_combinaties),
    ("GF16", gf16_klant_lifetime_value),
    ("GF17", gf17_winstgevendheid),
    ("GF18", gf18_klanten_belonen)
]

print("=== TEST ALLE VISUALISATIES ===\n")

fouten = []
geslaagd = []

for naam, functie in visualisaties:
    try:
        print(f"Test {naam}...", end=" ")
        fig = functie()
        if fig is not None:
            plt.close(fig)  # Sluit figure om geheugen te besparen
            print("✅ OK")
            geslaagd.append(naam)
        else:
            print("❌ FOUT: Geen figure geretourneerd")
            fouten.append((naam, "Geen figure geretourneerd"))
    except Exception as e:
        print(f"❌ FOUT: {str(e)}")
        fouten.append((naam, str(e)))

print(f"\n=== RESULTATEN ===")
print(f"Geslaagd: {len(geslaagd)}/{len(visualisaties)}")
print(f"Fouten: {len(fouten)}/{len(visualisaties)}")

if fouten:
    print("\n=== FOUTEN DETAILS ===")
    for naam, fout in fouten:
        print(f"{naam}: {fout}")
else:
    print("\n✅ Alle visualisaties werken correct!") 