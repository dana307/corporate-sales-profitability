# Executive dashboard build plan

**Audience:** Sales director / commercial finance manager. **Decision:** where to investigate margin leakage.

## Phase 1: validate data
Import Orders and check row count, date range, nulls, duplicate Row ID, and `SUM(Sales)`/`SUM(Profit)` against Python `quality_report.json` and monthly totals. Decide whether to use original Orders sheet or cleaned CSV, then keep that choice consistent.

## Phase 2: five worksheets
1. `KPI Overview`: revenue (dataset Sales), profit, profit margin, distinct orders, AOV; selected calendar year and comparable prior-year period.
2. `Monthly Trends`: monthly Sales and Profit trend; annual comparatives.
3. `Category Profitability`: category/sub-category profit bars; highlight negative profitability.
4. `Regional Performance`: region / segment performance with sales, profit and margin; map optional.
5. `Discount vs Profit`: scatterplot at an explicit grain (prefer product/sub-category or order line; document which) with size/tooltip showing Sales.

## Phase 3: executive dashboard
A 1400×950 tiled layout with KPI row, two charts in middle, and profitability/discount drill-down at bottom. Add year, region, and segment filters; use dashboard actions to highlight (not destructively filter) relevant categories. Include one concise finding and one recommended *test* for each major problem.

## Phase 4: QA and publication
- Test date filtering on every chart.
- Check year-over-year calculations on completed/equivalent periods.
- Compare dashboard total to pandas aggregations.
- Confirm no duplicate counts after relating Returns.
- Add data source citation and fictional-data caveat.
- Publish Tableau Public link and screenshot to README.
