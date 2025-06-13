"""
Product Management Module - H2D Price Calculator
===============================================

Dit module biedt complete product lifecycle management voor het
H2D Price Calculator systeem.

VEREENVOUDIGD: Direct CSV integratie!

Componenten:
-----------
- Product: Domain model voor 3D print producten
- ProductManager: Business logic en CSV integratie
- ProductCharts: Visualisaties met scrollbare grafieken

Gebruik:
-------
    >>> from products import Product, ProductManager, ProductCharts
    >>> 
    >>> # Nieuw product via manager
    >>> manager = ProductManager()
    >>> product = Product(name="Phone Case", weight_g=45, material="PLA Basic")
    >>> saved = manager.create(product)
    >>> print(saved.product_id)
    PRD-20250130-0001
    
    >>> # Toon grafieken
    >>> charts = ProductCharts(parent, manager, colors)

Auteur: H2D Systems
Versie: 2.1 - Met visualisaties!
"""

# Type checking support
from typing import TYPE_CHECKING

# Domain models
from .product_model import Product
from .product_manager import ProductManager

# Probeer charts te importeren (vereist matplotlib)
try:
    from .product_charts import ProductCharts
    __all__ = ['Product', 'ProductManager', 'ProductCharts']
except ImportError:
    # Als matplotlib niet geïnstalleerd is
    __all__ = ['Product', 'ProductManager']

# Versie info
__version__ = '2.1.0' 