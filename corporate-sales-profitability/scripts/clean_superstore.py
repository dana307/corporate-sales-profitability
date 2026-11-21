"""Clean common variants of Tableau Sample Superstore without inventing missing data.

Run: python scripts/clean_superstore.py --input 'data/raw/Sample - Superstore.xlsx'
The input is NOT shipped with this repository. Download from Tableau Public sample data.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import pandas as pd

REQUIRED = {"order_id", "order_date", "sales", "profit", "quantity", "discount"}
DATE_COLS = ("order_date", "ship_date")
NUM_COLS = ("sales", "profit", "quantity", "discount")


def snake(name: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def sheet_name(names: list[str], wanted: str) -> str | None:
    return next((n for n in names if snake(n) == wanted), None)


def clean_orders(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = frame.copy()
    df.columns = [snake(c) for c in df.columns]
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Orders sheet missing required columns: {sorted(missing)}")
    raw_rows = len(df)
    for col in DATE_COLS:
        if col in df:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in NUM_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["order_id"] = df["order_id"].astype("string").str.strip()
    if "row_id" in df:
        duplicate_row_ids = int(df["row_id"].duplicated(keep=False).sum())
    else:
        duplicate_row_ids = None
    # Preserve source rows, including any repeated keys: report issues for manual inspection.
    df["order_year"] = df["order_date"].dt.year.astype("Int64")
    df["order_month"] = df["order_date"].dt.to_period("M").astype("string")
    df["profit_margin_line"] = df["profit"].div(df["sales"].where(df["sales"] != 0))
    df["is_loss_line"] = df["profit"] < 0
    if "ship_date" in df:
        df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
    report = {
        "input_rows": raw_rows,
        "output_rows": len(df),
        "nulls_by_column": {str(k): int(v) for k, v in df.isna().sum().items()},
        "duplicate_row_id_rows": duplicate_row_ids,
        "invalid_discount_outside_0_1": int((df["discount"].notna() & ~df["discount"].between(0, 1)).sum()),
        "nonpositive_sales_rows": int((df["sales"].notna() & (df["sales"] <= 0)).sum()),
        "ship_before_order_rows": int((df["shipping_days"].dropna() < 0).sum()) if "shipping_days" in df else None,
        "distinct_orders": int(df["order_id"].nunique()),
        "dataset_years": sorted(int(x) for x in df["order_year"].dropna().unique()),
    }
    return df, report


def monthly_kpis(orders: pd.DataFrame) -> pd.DataFrame:
    valid = orders.dropna(subset=["order_month", "sales", "profit", "order_id"])
    grouped = valid.groupby("order_month", as_index=False).agg(
        sales=("sales", "sum"), profit=("profit", "sum"),
        orders=("order_id", "nunique"), order_lines=("order_id", "size")
    )
    grouped["profit_margin"] = grouped["profit"].div(grouped["sales"].where(grouped["sales"] != 0))
    grouped["average_order_value"] = grouped["sales"].div(grouped["orders"].where(grouped["orders"] != 0))
    return grouped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", default="data/processed", type=Path)
    args = parser.parse_args()
    if not args.input.exists():
        parser.error(f"Input not found: {args.input}")
    excel = pd.ExcelFile(args.input)
    orders_name = sheet_name(excel.sheet_names, "orders")
    if not orders_name:
        parser.error(f"Expected 'Orders' worksheet; found {excel.sheet_names}")
    orders, report = clean_orders(pd.read_excel(excel, sheet_name=orders_name))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    orders.to_csv(args.output_dir / "orders_clean.csv", index=False)
    monthly_kpis(orders).to_csv(args.output_dir / "monthly_kpis.csv", index=False)
    for optional in ("returns", "people"):
        name = sheet_name(excel.sheet_names, optional)
        if name:
            frame = pd.read_excel(excel, sheet_name=name)
            frame.columns = [snake(c) for c in frame.columns]
            for c in ("order_id", "region"):
                if c in frame:
                    frame[c] = frame[c].astype("string").str.strip()
            frame.to_csv(args.output_dir / f"{optional}_clean.csv", index=False)
            report[f"{optional}_rows"] = len(frame)
        else:
            report[f"{optional}_rows"] = None
    (args.output_dir / "quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Cleaned files saved to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
