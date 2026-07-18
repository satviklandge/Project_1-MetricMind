"""
load_data.py
------------
Loads sales_data.csv (Excel format) into the PostgreSQL 'sales_data' table.

Usage:
    python database/load_data.py

Configuration:
    Edit the DB_CONFIG dict below to match your PostgreSQL credentials.
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# ── 1. Database connection settings ──────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "metricmind",   # ← change this
    "user":     "sales_data",        # ← change this
    "password": "Satvik@19",        # ← change this
}

# ── 2. Path to the raw data file ──────────────────────────────────────────────
DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "raw", "sales_data.csv"
)

# ── 3. Column mapping: Excel → PostgreSQL ─────────────────────────────────────
COLUMN_MAP = {
    "Order_ID":         "order_id",
    "Order_Date":       "order_date",
    "Region":           "region",
    "Country":          "country",
    "Product":          "product",
    "Category":         "category",
    "Customer_Type":    "customer_type",
    "Quantity":         "quantity",
    "Unit_Price":       "unit_price",
    "Revenue":          "revenue",
    "Material_Cost":    "material_cost",
    "Shipping_Cost":    "shipping_cost",
    "Operational_Cost": "operational_cost",
    "Total_Cost":       "total_cost",
    "Profit":           "profit",
    "Margin":           "margin",
}

# ── 4. Load & clean ───────────────────────────────────────────────────────────
def load_dataframe(filepath: str) -> pd.DataFrame:
    print(f"📂  Reading file: {filepath}")
    df = pd.read_excel(filepath)

    # Rename to match DB columns
    df = df.rename(columns=COLUMN_MAP)

    # Ensure correct types
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
    df["quantity"]   = df["quantity"].astype(int)

    numeric_cols = [
        "unit_price", "revenue", "material_cost",
        "shipping_cost", "operational_cost", "total_cost",
        "profit", "margin"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    # Drop rows where primary key is missing
    df = df.dropna(subset=["order_id"])
    df["order_id"] = df["order_id"].astype(str).str.strip()

    print(f"✅  Loaded {len(df):,} rows, {len(df.columns)} columns")
    return df


# ── 5. Insert into PostgreSQL ─────────────────────────────────────────────────
INSERT_SQL = """
    INSERT INTO sales_data (
        order_id, order_date, region, country, product, category,
        customer_type, quantity, unit_price, revenue, material_cost,
        shipping_cost, operational_cost, total_cost, profit, margin
    )
    VALUES %s
    ON CONFLICT (order_id) DO UPDATE SET
        order_date       = EXCLUDED.order_date,
        region           = EXCLUDED.region,
        country          = EXCLUDED.country,
        product          = EXCLUDED.product,
        category         = EXCLUDED.category,
        customer_type    = EXCLUDED.customer_type,
        quantity         = EXCLUDED.quantity,
        unit_price       = EXCLUDED.unit_price,
        revenue          = EXCLUDED.revenue,
        material_cost    = EXCLUDED.material_cost,
        shipping_cost    = EXCLUDED.shipping_cost,
        operational_cost = EXCLUDED.operational_cost,
        total_cost       = EXCLUDED.total_cost,
        profit           = EXCLUDED.profit,
        margin           = EXCLUDED.margin;
"""

ORDERED_COLS = [
    "order_id", "order_date", "region", "country", "product", "category",
    "customer_type", "quantity", "unit_price", "revenue", "material_cost",
    "shipping_cost", "operational_cost", "total_cost", "profit", "margin"
]


def insert_data(df: pd.DataFrame):
    print("🔌  Connecting to PostgreSQL …")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    # Convert DataFrame rows → list of tuples in the correct column order
    records = [
        tuple(row[col] for col in ORDERED_COLS)
        for _, row in df.iterrows()
    ]

    print(f"⬆️   Inserting {len(records):,} rows …")
    try:
        execute_values(cur, INSERT_SQL, records, page_size=500)
        conn.commit()
        print("🎉  Data loaded successfully!")
    except Exception as exc:
        conn.rollback()
        print(f"❌  Error during insert: {exc}")
        raise
    finally:
        cur.close()
        conn.close()


# ── 6. Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_dataframe(DATA_FILE)
    insert_data(df)

    # Quick verification
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sales_data;")
    count = cur.fetchone()[0]
    print(f"📊  Total rows now in sales_data: {count:,}")
    cur.close()
    conn.close()
