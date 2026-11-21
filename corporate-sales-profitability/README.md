# Corporate Sales & Profitability | Tableau + Python + SQL

**Status:** Scaffolded — results and dashboard not yet built.

## Business brief
You are supporting the commercial director of a fictional retail company. Build a management dashboard that answers:
1. How are sales and gross profit (as defined by the sample's `Profit` field) trending?
2. Which regions, categories, and sub-categories contribute most to sales and profit?
3. Are heavy discounts associated with unprofitable orders?
4. Which products and customers warrant follow-up?

**Data:** Tableau's fictional **Sample Superstore** dataset. Download the workbook from [Tableau Public Sample Data](https://public.tableau.com/app/resources/sample-data). Dataset versions may differ; inspect the actual workbook before relying on any numerical conclusions.

## Repository structure
```
data/raw/                 # Put your downloaded workbook here; not tracked in git
 data/processed/           # Generated CSVs; not tracked in git
scripts/clean_superstore.py
sql/analysis_queries.sql
sql/schema.sql
tableau/calculated_fields.md
tableau/build_plan.md
docs/data_dictionary.md
docs/business_questions.md
images/                   # Add a dashboard screenshot after publication
tests/test_cleaning.py
requirements.txt
.gitignore
```

## Quick start
```bash
python -m pip install -r requirements.txt
python scripts/clean_superstore.py --input "data/raw/Sample - Superstore.xlsx"
python -m unittest discover -s tests -v
```
Use the actual `.xls` or `.xlsx` filename you downloaded. For `.xls`, `xlrd` is provided in requirements.

The script outputs `data/processed/orders_clean.csv`, optional `returns_clean.csv`, `people_clean.csv`, `monthly_kpis.csv`, and a `quality_report.json`.

## KPI definitions (important)
- **Sales:** `SUM(Sales)` at **order-line** grain; not the number of orders.
- **Profit:** `SUM(Profit)` using the dataset's supplied profit measure; do not call it audited operating profit.
- **Profit margin:** `SUM(Profit) / SUM(Sales)`; never average row-level margins.
- **Orders:** `COUNTD(Order ID)`.
- **Average order value:** `SUM(Sales) / COUNTD(Order ID)`.
- **Return rate:** requires the Returns sheet. Define clearly whether the denominator is distinct orders, and avoid joining returns in a way that duplicates order lines.
- **YOY:** compare equivalent periods and avoid comparing incomplete years with complete years.

## Tableau dashboard
See [`tableau/build_plan.md`](tableau/build_plan.md) and [`tableau/calculated_fields.md`](tableau/calculated_fields.md). After publishing, replace this with a screenshot and live link:

**Dashboard:** _Not yet published_

## Evidence checklist
- [ ] Raw data version, source URL, and download date documented
- [ ] Data quality checks reviewed; duplicate row IDs addressed rather than silently discarded
- [ ] Cleaned dataset created from reproducible script
- [ ] Core KPI definitions tested against Python or SQL totals
- [ ] Executive dashboard built and published to Tableau Public
- [ ] 3 evidence-based findings, limitations, and recommended management follow-ups added here

## Limitations
This is a fictional learning dataset, not real company financials. Sales and Profit measures should not be conflated with audited revenue or net income. A correlation between discount and profit is not evidence of a causal discount effect.
