-- Run after loading cleaned order rows into a table named `orders`.
-- Compatible with SQLite if `order_date` is ISO-8601 text.
-- KPI summary by calendar year, avoiding double counting multi-line orders.
SELECT substr(order_date,1,4) AS order_year,
       ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit,
       ROUND(SUM(profit) / NULLIF(SUM(sales),0),4) AS profit_margin,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id),0),2) AS avg_order_value
FROM orders
GROUP BY substr(order_date,1,4)
ORDER BY order_year;

-- Profitability by product sub-category.
SELECT category, sub_category,
       ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit,
       ROUND(SUM(profit)/NULLIF(SUM(sales),0),4) AS profit_margin
FROM orders
GROUP BY category, sub_category
ORDER BY profit ASC;
