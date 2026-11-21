# Tableau calculated fields

Use original `Orders` source or the cleaned `orders_clean.csv` (field names change from Title Case to snake_case). Below assumes original Tableau-friendly labels.

## Core metrics
**Profit Margin**
```tableau
IF SUM([Sales]) = 0 THEN NULL ELSE SUM([Profit]) / SUM([Sales]) END
```
**Average Order Value**
```tableau
IF COUNTD([Order ID]) = 0 THEN NULL ELSE SUM([Sales]) / COUNTD([Order ID]) END
```
**Order Count**
```tableau
COUNTD([Order ID])
```
**Loss-Making Line** (for breakdowns; do not confuse with loss-making order)
```tableau
[Profit] < 0
```
**Order Month**
```tableau
DATETRUNC('month', [Order Date])
```

To build YOY metrics, use a date-aware table calculation or a dedicated period-aligned dataset, not an unconditional `LOOKUP()` without validated addressing/partitioning. The dataset has no actual management targets unless you explicitly add a separately documented target table.
