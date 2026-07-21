# 📊 MetricMind Semantic Layer

A Cube.dev-powered semantic layer on top of the MetricMind PostgreSQL database (`metricmind.sales_data`). This layer translates raw SQL tables into **business-friendly metrics** that the AI agent can query using natural language terms.

---

## 🏗️ Architecture

```
AI Agent / Frontend
       │
       ▼
  Cube.dev API  ◄──────── Cube Playground (http://localhost:4000)
  (Port 4000)
       │
       ▼
PostgreSQL DB (metricmind)
  └── sales_data table
```

---

## 📁 Project Structure

```
semantic_layer/
├── model/
│   └── Sales.js          # Sales cube: measures + dimensions
├── .env                  # Database credentials (not committed)
├── cube.js               # Cube server entry point
├── package.json          # Node.js dependencies
└── README.md             # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Node.js ≥ 18.x
- PostgreSQL running locally with `metricmind` database

### Install Dependencies

```bash
cd semantic_layer
npm install
```

### Configure Environment

Edit `.env` with your PostgreSQL credentials:

```env
CUBEJS_DB_TYPE=postgres
CUBEJS_DB_HOST=localhost
CUBEJS_DB_PORT=5432
CUBEJS_DB_NAME=metricmind
CUBEJS_DB_USER=postgres
CUBEJS_DB_PASS=YOUR_PASSWORD

CUBEJS_DEV_MODE=true
```

### Start the Semantic Layer

```bash
npm run dev
```

Open the **Cube Playground** at: [http://localhost:4000](http://localhost:4000)

---

## 📐 Sales Cube — `model/Sales.js`

Maps the `sales_data` PostgreSQL table to structured business metrics.

### 📏 Measures

| Measure | SQL Column | Type | Description |
|---|---|---|---|
| `totalRevenue` | `revenue` | `sum` | Total revenue across filters |
| `averageRevenue` | `revenue` | `avg` | Average revenue per order |
| `totalMaterialCost` | `material_cost` | `sum` | Total material costs |
| `totalShippingCost` | `shipping_cost` | `sum` | Logistics spend |
| `totalOperationalCost` | `operational_cost` | `sum` | Ops overhead |
| `totalCost` | `total_cost` | `sum` | All combined costs |
| `totalProfit` | `profit` | `sum` | Total profit (revenue − cost) |
| `averageProfit` | `profit` | `avg` | Average per-order profit |
| `averageMargin` | `margin` | `avg` | **Avg margin %** — key KPI |
| `totalOrders` | — | `count` | Number of orders |
| `totalQuantity` | `quantity` | `sum` | Units sold |

### 🗂️ Dimensions

| Dimension | SQL Column | Type | Description |
|---|---|---|---|
| `orderId` | `order_id` | `string` | Primary key |
| `region` | `region` | `string` | Geographic region |
| `country` | `country` | `string` | Country |
| `product` | `product` | `string` | Product name |
| `category` | `category` | `string` | Product category |
| `customerType` | `customer_type` | `string` | Customer segment |
| `orderDate` | `order_date` | `time` | Order date (supports granularities) |
| `quarter` | `quarter` | `number` | Pre-calculated quarter (1–4) |

---

## 🔍 Sample Queries (Cube Playground)

### 1. Total Revenue
```
Measure: Sales.totalRevenue
```

### 2. Revenue by Region
```
Measure: Sales.totalRevenue
Dimension: Sales.region
```

### 3. Monthly Revenue Trend
```
Measure: Sales.totalRevenue
Time Dimension: Sales.orderDate → Month
```

### 4. Profit by Product
```
Measure: Sales.totalProfit
Dimension: Sales.product
```

### 5. ⚠️ Europe Q3 Margin Validation
```
Measures: Sales.averageMargin, Sales.totalRevenue, Sales.totalShippingCost
Dimension: Sales.region
Time: Sales.orderDate → Q3 2024
Filter: region = 'Europe'
```
This validates the Europe Q3 scenario where increased shipping costs caused a margin drop.

---

## 🔌 REST API Usage

Once the server is running, you can query it via REST:

```bash
# Get total revenue by region
curl -G http://localhost:4000/cubejs-api/v1/load \
  -H "Authorization: CUBEJS_API_SECRET" \
  --data-urlencode 'query={"measures":["Sales.totalRevenue"],"dimensions":["Sales.region"]}'
```

---

## 🛠️ Pre-aggregations

Two pre-aggregations are defined for query performance:

| Name | Dimensions | Measures | Granularity |
|---|---|---|---|
| `revenueByRegionMonthly` | region, country | revenue, profit, margin, orders | Monthly |
| `revenueByProductMonthly` | product, category | revenue, profit, orders | Monthly |

---

## 🧪 Day 5 Checklist

- [x] Cube.dev installed (`cubejs-cli`)
- [x] PostgreSQL connected (`metricmind` database)
- [x] Semantic layer created (`semantic_layer/`)
- [x] `Sales.js` model completed with all measures and dimensions
- [x] `.env` configured with DB credentials
- [x] `package.json` with correct dependencies
- [x] Cube Playground accessible at `http://localhost:4000`
- [ ] Revenue, profit, margin, and regional queries tested *(run after `npm run dev`)*
- [ ] Europe Q3 margin drop validated *(run the Europe Q3 query above)*
