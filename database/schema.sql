CREATE DATABASE metricmind;


DROP TABLE sales_data;

CREATE TABLE sales_data (
    order_id VARCHAR(20),
    order_date DATE,
    region VARCHAR(50),
    country VARCHAR(50),
    product VARCHAR(50),
    category VARCHAR(50),
    customer_type VARCHAR(30),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    revenue NUMERIC(12,2),
    material_cost NUMERIC(12,2),
    shipping_cost NUMERIC(12,2),
    operational_cost NUMERIC(12,2),
    total_cost NUMERIC(12,2),
    profit NUMERIC(12,2),
    margin NUMERIC(6,2)
);

ALTER TABLE sales_data
ADD COLUMN quarter INT;

SELECT * FROM sales_data;

-- Verify Import
SELECT COUNT(*)
FROM sales_data;


-- Test SQL Queries
--- Revenue by Region
SELECT
    region,
    SUM(revenue)
FROM sales_data
GROUP BY region;

--- Average Margin
SELECT
AVG(margin)
FROM sales_data;

--- European Q3 Margin
SELECT
AVG(margin)
FROM sales_data
WHERE region='Europe'
AND EXTRACT(QUARTER FROM order_date)=3;