Deze map bevat alle centrale configuratiebestanden.

- `config.py` definieert basis-constanten zoals uurkosten, overhead, marges enz.
- `__init__.py` maakt de map importeerbaar als package.

Wijzig hier **nooit** business-logica; enkel statische waarden. Zo blijft onderhoud eenvoudig. 