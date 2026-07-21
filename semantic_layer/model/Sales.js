cube(`Sales`, {
  sql: `SELECT * FROM sales_data`,

  title: `Sales Data`,
  description: `Complete sales dataset including revenue, cost, profit, and margin metrics across regions, products, and time periods.`,

  measures: {
    // ─── Revenue Metrics ───────────────────────────────────────────────────────
    totalRevenue: {
      sql: `revenue`,
      type: `sum`,
      title: `Total Revenue`,
      description: `Sum of all revenue across selected dimensions`,
      format: `currency`
    },

    averageRevenue: {
      sql: `revenue`,
      type: `avg`,
      title: `Average Revenue`,
      description: `Average revenue per order`,
      format: `currency`
    },

    // ─── Cost Metrics ──────────────────────────────────────────────────────────
    totalMaterialCost: {
      sql: `material_cost`,
      type: `sum`,
      title: `Total Material Cost`,
      format: `currency`
    },

    totalShippingCost: {
      sql: `shipping_cost`,
      type: `sum`,
      title: `Total Shipping Cost`,
      description: `Sum of all shipping costs — useful for monitoring logistics spend spikes`,
      format: `currency`
    },

    totalOperationalCost: {
      sql: `operational_cost`,
      type: `sum`,
      title: `Total Operational Cost`,
      format: `currency`
    },

    totalCost: {
      sql: `total_cost`,
      type: `sum`,
      title: `Total Cost`,
      format: `currency`
    },

    // ─── Profit & Margin Metrics ───────────────────────────────────────────────
    totalProfit: {
      sql: `profit`,
      type: `sum`,
      title: `Total Profit`,
      description: `Sum of all profit (revenue minus total costs)`,
      format: `currency`
    },

    averageProfit: {
      sql: `profit`,
      type: `avg`,
      title: `Average Profit`,
      format: `currency`
    },

    averageMargin: {
      sql: `margin`,
      type: `avg`,
      title: `Average Margin %`,
      description: `Average profit margin percentage — key metric for Europe Q3 shipping-cost impact analysis`,
      format: `percent`
    },

    // ─── Order Metrics ─────────────────────────────────────────────────────────
    totalOrders: {
      type: `count`,
      title: `Total Orders`,
      description: `Count of all orders in the selected period and dimensions`
    },

    totalQuantity: {
      sql: `quantity`,
      type: `sum`,
      title: `Total Quantity Sold`,
      description: `Total number of units sold`
    }
  },

  dimensions: {
    // ─── Identifiers ───────────────────────────────────────────────────────────
    orderId: {
      sql: `order_id`,
      type: `string`,
      primaryKey: true,
      title: `Order ID`
    },

    // ─── Geography ─────────────────────────────────────────────────────────────
    region: {
      sql: `region`,
      type: `string`,
      title: `Region`,
      description: `Geographic sales region (e.g., Europe, North America, Asia-Pacific)`
    },

    country: {
      sql: `country`,
      type: `string`,
      title: `Country`
    },

    // ─── Product ───────────────────────────────────────────────────────────────
    product: {
      sql: `product`,
      type: `string`,
      title: `Product Name`
    },

    category: {
      sql: `category`,
      type: `string`,
      title: `Product Category`
    },

    // ─── Customer ──────────────────────────────────────────────────────────────
    customerType: {
      sql: `customer_type`,
      type: `string`,
      title: `Customer Type`,
      description: `Segment type (e.g., Retail, Wholesale, Enterprise)`
    },

    // ─── Time ──────────────────────────────────────────────────────────────────
    orderDate: {
      sql: `order_date`,
      type: `time`,
      title: `Order Date`,
      description: `Date the order was placed — supports granularities: day, week, month, quarter, year`
    },

    // ─── Financial Detail ──────────────────────────────────────────────────────
    quarter: {
      sql: `quarter`,
      type: `number`,
      title: `Quarter`,
      description: `Fiscal quarter number (1–4) pre-calculated in the database`
    }
  },

  // ─── Pre-aggregations for Performance ────────────────────────────────────────
  preAggregations: {
    revenueByRegionMonthly: {
      measures: [CUBE.totalRevenue, CUBE.totalProfit, CUBE.averageMargin, CUBE.totalOrders],
      dimensions: [CUBE.region, CUBE.country],
      timeDimension: CUBE.orderDate,
      granularity: `month`,
      refreshKey: {
        every: `1 hour`
      }
    },

    revenueByProductMonthly: {
      measures: [CUBE.totalRevenue, CUBE.totalProfit, CUBE.totalOrders],
      dimensions: [CUBE.product, CUBE.category],
      timeDimension: CUBE.orderDate,
      granularity: `month`
    }
  }
});
