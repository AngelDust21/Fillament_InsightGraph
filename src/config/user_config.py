"""
Gebruikersconfiguratie voor H2D Calculator
==========================================

Dit bestand wordt automatisch gegenereerd door de GUI configuratie tab.
Pas dit NIET handmatig aan - gebruik de GUI configuratie tab.
"""

import json
from pathlib import Path
from typing import Dict, Any

CONFIG_FILE = Path(__file__).parent / "user_settings.json"

def save_user_config(config_data: Dict[str, Any]) -> None:
    """Sla gebruikersconfiguratie op naar JSON bestand."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)

def load_user_config() -> Dict[str, Any]:
    """Laad gebruikersconfiguratie uit JSON bestand."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_config_value(key: str, default: Any = None) -> Any:
    """Haal een specifieke configuratie waarde op."""
    config = load_user_config()
    return config.get(key, default)

def config_exists() -> bool:
    """Check of er een gebruikersconfiguratie bestaat."""
    return CONFIG_FILE.exists() 