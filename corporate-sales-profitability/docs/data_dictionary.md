# Data dictionary (confirm against your workbook)

The common `Orders` sheet has order-line grain, with fields such as `Order ID`, `Order Date`, `Ship Date`, `Customer ID`, `Product ID`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, `Profit`. Exact versions differ; validate on import.

| Clean field | Meaning | Grain |
|---|---|---|
| `order_id` | Order identifier; can repeat across product lines | order |
| `order_date` | Order placement date | order |
| `sales` | Amount attributed to order line | order line |
| `profit` | Dataset-provided profit contribution | order line |
| `discount` | Recorded discount fraction | order line |
| `profit_margin_line` | `profit / sales` where nonzero | order line |
| `order_month` | Calendar YYYY-MM derived from order date | order line |
| `shipping_days` | Days between ship and order date | order line |
| `is_loss_line` | Profit is negative | order line |

Optional `Returns` and `People` sheets should be modeled on their own grains, not naïvely joined in a way that duplicates order lines. `Returns` may be one record per returned order; `People` typically maps region to responsible person.
