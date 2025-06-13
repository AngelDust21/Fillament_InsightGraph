# Package-init zodat we `from materials import get_price` kunnen doen
from .materials import get_price, list_materials, Material, get_material

# Probeer material properties te importeren
try:
    from .material_properties import (
        MaterialProperties,
        get_material_properties,
        calculate_print_time,
        calculate_wear_cost,
        get_nozzle_recommendation,
        MATERIAL_PROPERTIES
    )
except ImportError:
    # Als bestand niet bestaat
    pass 