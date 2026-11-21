-- Optional SQLite staging model. `orders_clean.csv` can be loaded into a table named orders.
-- This is a data contract, not an automatic import script.
CREATE TABLE IF NOT EXISTS orders (
  row_id INTEGER,
  order_id TEXT,
  order_date TEXT,
  ship_date TEXT,
  customer_id TEXT,
  region TEXT,
  category TEXT,
  sub_category TEXT,
  sales REAL,
  profit REAL,
  discount REAL,
  quantity INTEGER
);
