SELECT * FROM sales_data;

-- Verify the data 
SELECT COUNT(*) AS total_rows
FROM sales_data;

-- View sample data
SELECT *
FROM sales_data
LIMIT 10 ;

-- Total Revenue 
SELECT 
ROUND(SUM(revenue),2) AS total_revenue
FROM sales_data;

-- Total Profit 
SELECT 
ROUND(SUM(profit),2) AS total_profit
FROM sales_data;

-- Total_Cost 
SELECT 
ROUND(SUM(total_cost),2) AS total_cost
FROM sales_data;

-- Revenue by Region
SELECT 
region,
ROUND(SUM(revenue),2) AS revenue
FROM sales_data
GROUP BY region 
ORDER BY revenue DESC;

-- Profit by Region
SELECT 
region,
ROUND(SUM(profit),2) AS Profit
FROM sales_data
GROUP BY region 
ORDER BY profit DESC;

-- Revenue by Country
SELECT
country,
ROUND(SUM(revenue),2) AS revenue
FROM sales_data
GROUP BY country
ORDER BY revenue DESC;

-- Top 10 Products
SELECT 
product,
ROUND(SUM(revenue),2) AS revenue
FROM sales_data
GROUP BY product 
ORDER BY revenue DESC
LIMIT 10;

-- Customer Type Analysis
SELECT 
customer_type,
COUNT(*) AS orders,
ROUND(SUM(revenue),2) AS revenue,
ROUND(SUM(profit),2) AS profit
FROM sales_data 
GROUP BY customer_type;

-- Monthly Sales Trend
SELECT
DATE_TRUNC('month', order_date) AS month,
ROUND(SUM(revenue),2) AS revenue
FROM sales_data
GROUP BY month
ORDER BY month;

-- Europe Analysis (Main Business Question)
SELECT
    region,
    EXTRACT(QUARTER FROM order_date) AS quarter,
    SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY
    region,
    EXTRACT(QUARTER FROM order_date)
ORDER BY region, quarter;


