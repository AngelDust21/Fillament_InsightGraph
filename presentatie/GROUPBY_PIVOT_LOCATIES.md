# GroupBy en Pivot Functies in SRC Map

Dit document bevat een overzicht van alle `groupby()` en `pivot()` functies die gebruikt worden in de `/src` map van het Fillament InsightGraph project.

## Overzicht Bestanden

### 1. **src/utils/data_manager.py**
Dit bestand bevat 4 groupby functies voor data aggregatie:

- **Regel 404**: Top producten analyse
  ```python
  top_products = products_df.groupby('product_name').agg({...})
  ```
  Groepeert producten op naam voor productanalyse

- **Regel 412**: Materiaal statistieken
  ```python
  material_stats = df.groupby('material').agg({...})
  ```
  Groepeert data op materiaaltype voor materiaalanalyse

- **Regel 434**: Uurpatroon analyse
  ```python
  analysis['hourly_pattern'] = df.groupby('hour_of_day').size().to_dict()
  ```
  Groepeert data per uur van de dag

- **Regel 437**: Dagpatroon analyse
  ```python
  analysis['daily_pattern'] = df.groupby('day_of_week').size().to_dict()
  ```
  Groepeert data per dag van de week

### 2. **src/analytics/slijtage/grafiek.py**
Dit bestand gebruikt zowel groupby als pivot functies voor slijtage visualisaties:

- **Regel 140**: Materiaal uren berekening
  ```python
  material_hours = abrasive_df.groupby('material')['print_hours'].sum()
  ```
  Berekent totale printuren per materiaal

- **Regel 238**: Dagelijkse data aggregatie
  ```python
  daily_data = df.groupby(['date', 'abrasive'])['print_hours'].sum().unstack(fill_value=0)
  ```
  Groepeert printuren per dag en schuurmiddel

- **Regel 518**: Heatmap pivot table
  ```python
  pivot = df_filtered.groupby(['weekday', 'hour'])['print_hours'].sum().unstack(fill_value=0)
  ```
  Maakt een pivot table voor weekdag/uur heatmap visualisatie

### 3. **src/analytics/basis/print_waardes.py**
Bevat 1 groupby functie voor prijsanalyse:

- **Regel 252**: Prijs statistieken per categorie
  ```python
  price_stats = df_filtered.groupby('category')['price_per_gram'].mean()
  ```
  Berekent gemiddelde prijs per gram per categorie

### 4. **src/analytics/basis/dagelijkse_activiteit.py**
Gebruikt zowel groupby als pivot_table:

- **Regel 141**: Dagelijkse tellingen
  ```python
  daily_counts = df.groupby(df['date']).size()
  ```
  Telt aantal activiteiten per dag

- **Regel 281-287**: Heatmap pivot table
  ```python
  heatmap_data = df.pivot_table(
      values='timestamp',
      index='hour_of_day',
      columns='day_of_week',
      aggfunc='count',
      fill_value=0
  )
  ```
  Maakt een pivot table voor heatmap visualisatie van activiteit per uur en weekdag

## Samenvatting

In totaal zijn er **minstens 3 gegroepeerde functies** gevonden in de src map:

1. **GroupBy functies**: 7 instanties
   - Data aggregatie (producten, materialen)
   - Tijdspatroon analyse (uur, dag, datum)
   - Prijsstatistieken

2. **Pivot/Unstack functies**: 3 instanties
   - Heatmap visualisaties
   - Data transformatie van lang naar breed formaat

Deze functies worden voornamelijk gebruikt voor:
- **Data aggregatie**: Van details naar totalen
- **Patroonherkenning**: Tijdsgebaseerde analyses
- **Visualisatievoorbereiding**: Vooral voor heatmaps en grafieken

## Notitie voor de Leerkracht

De gevraagde 3 gegroepeerde functies zijn ruimschoots aanwezig in het project. De belangrijkste voorbeelden zijn:

1. **Product aggregatie** in `data_manager.py` (regel 404-408)
   ```python
   top_products = products_df.groupby('product_name').agg({
       'sell_price': 'sum',
       'product_name': 'count'
   }).rename(columns={'product_name': 'count', 'sell_price': 'revenue'})
   ```

2. **Materiaal statistieken** in `data_manager.py` (regel 412-420)
   ```python
   material_stats = df.groupby('material').agg({
       'material': 'count',
       'margin_pct': 'mean',
       'profit_amount': 'sum',
       'weight': 'mean'
   }).round(2)
   ```

3. **Heatmap pivot table** in `dagelijkse_activiteit.py` (regel 281-287)
   ```python
   heatmap_data = df.pivot_table(
       values='timestamp',
       index='hour_of_day',
       columns='day_of_week',
       aggfunc='count',
       fill_value=0
   )
   ```

Al deze functies gebruiken pandas groupby/pivot functionaliteit voor data transformatie en analyse. 