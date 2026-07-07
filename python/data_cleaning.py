import pandas as pd
import numpy as np
from pathlib import Path

# Project path
project_root = Path(r"C:\Projects\ecommerce-sales-delivery-analysis")

raw_dir = project_root / "data" / "raw"
cleaned_dir = project_root / "data" / "cleaned"
cleaned_dir.mkdir(parents=True, exist_ok=True)

print("Raw folder exists:", raw_dir.exists())
print("Files in raw folder:")
for file in raw_dir.iterdir():
    print(file.name)

# File names
files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# Check files
for name, filename in files.items():
    path = raw_dir / filename
    print(name, "exists:", path.exists(), "|", filename)


customers = pd.read_csv(raw_dir / files["customers"])
orders = pd.read_csv(raw_dir / files["orders"])
order_items = pd.read_csv(raw_dir / files["order_items"])
payments = pd.read_csv(raw_dir / files["payments"])
reviews = pd.read_csv(raw_dir / files["reviews"])
products = pd.read_csv(raw_dir / files["products"])
sellers = pd.read_csv(raw_dir / files["sellers"])
category_translation = pd.read_csv(raw_dir / files["category_translation"])

datasets = {
    "customers": customers,
    "orders": orders,
    "order_items": order_items,
    "payments": payments,
    "reviews": reviews,
    "products": products,
    "sellers": sellers,
    "category_translation": category_translation
}

for name, df in datasets.items():
    print(name, df.shape)

for name, df in datasets.items():
    print("\n" + name)
    print(df.columns.tolist())


## date columns conversion
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"], errors="coerce")
reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"], errors="coerce")

print(orders[date_cols].dtypes)

## Order time and delivery metrics
orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
).dt.days

orders["estimated_delivery_days"] = (
    orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
).dt.days

orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
).dt.days

orders["is_late"] = np.where(
    orders["delivery_delay_days"].isna(),
    np.nan,
    np.where(orders["delivery_delay_days"] > 0, 1, 0)
)

orders[[
    "order_id",
    "order_status",
    "order_month",
    "delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "is_late"
]].head()

## Payment Aggregation by order_id
def most_common_value(series):
    mode_values = series.mode()
    if len(mode_values) > 0:
        return mode_values.iloc[0]
    return np.nan

payments_agg = payments.groupby("order_id").agg(
    total_payment_value=("payment_value", "sum"),
    payment_count=("payment_sequential", "max"),
    max_installments=("payment_installments", "max"),
    main_payment_type=("payment_type", most_common_value)
).reset_index()

payments_agg.head()

## Review Aggregation by order_id
reviews_agg = reviews.groupby("order_id").agg(
    avg_review_score=("review_score", "mean"),
    review_count=("review_id", "nunique")
).reset_index()

reviews_agg.head()

## English category names
products_clean = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)


## Aggregate product categories
products_clean[[
    "product_id",
    "product_category_name",
    "product_category_name_english"
]].head()

master = order_items.merge(
    orders,
    on="order_id",
    how="left"
)

master = master.merge(
    customers,
    on="customer_id",
    how="left"
)

master = master.merge(
    products_clean,
    on="product_id",
    how="left"
)

master = master.merge(
    sellers,
    on="seller_id",
    how="left"
)

master = master.merge(
    payments_agg,
    on="order_id",
    how="left"
)

master = master.merge(
    reviews_agg,
    on="order_id",
    how="left"
)

master["item_revenue"] = master["price"] + master["freight_value"]

print(master.shape)
master.head()


## Select final columns for analysis
final_cols = [
    "order_id",
    "order_item_id",
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "order_status",
    "order_purchase_timestamp",
    "order_month",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "is_late",
    "product_id",
    "product_category_name",
    "product_category_name_english",
    "seller_id",
    "seller_city",
    "seller_state",
    "price",
    "freight_value",
    "item_revenue",
    "total_payment_value",
    "main_payment_type",
    "max_installments",
    "avg_review_score",
    "review_count"
]

master_clean = master[final_cols].copy()

print(master_clean.shape)
master_clean.head()

## Summarize missing values
missing_summary = master_clean.isna().sum().sort_values(ascending=False)

missing_summary[missing_summary > 0]

output_path = cleaned_dir / "olist_order_items_master.csv"

master_clean.to_csv(output_path, index=False)


# Export a MySQL-friendly version with no blank values
mysql_clean = master_clean.copy()

# Fill missing text values
text_cols = [
    "customer_city",
    "customer_state",
    "order_status",
    "product_category_name",
    "product_category_name_english",
    "seller_city",
    "seller_state",
    "main_payment_type"
]

for col in text_cols:
    mysql_clean[col] = mysql_clean[col].fillna("Unknown")

# Fill missing numeric values
mysql_clean["delivery_days"] = mysql_clean["delivery_days"].fillna(-1)
mysql_clean["estimated_delivery_days"] = mysql_clean["estimated_delivery_days"].fillna(-1)
mysql_clean["delivery_delay_days"] = mysql_clean["delivery_delay_days"].fillna(-999)
mysql_clean["is_late"] = mysql_clean["is_late"].fillna(-1)

mysql_clean["total_payment_value"] = mysql_clean["total_payment_value"].fillna(0)
mysql_clean["max_installments"] = mysql_clean["max_installments"].fillna(0)
mysql_clean["avg_review_score"] = mysql_clean["avg_review_score"].fillna(-1)
mysql_clean["review_count"] = mysql_clean["review_count"].fillna(0)

# Fill missing dates with placeholder dates
mysql_clean["order_delivered_customer_date"] = mysql_clean["order_delivered_customer_date"].fillna("1900-01-01 00:00:00")
mysql_clean["order_estimated_delivery_date"] = mysql_clean["order_estimated_delivery_date"].fillna("1900-01-01 00:00:00")

# Export MySQL import file
mysql_output_path = cleaned_dir / "olist_order_items_master_mysql.csv"
mysql_clean.to_csv(mysql_output_path, index=False)

print("Saved MySQL import file to:", mysql_output_path)
print("Rows:", mysql_clean.shape[0])
print("Columns:", mysql_clean.shape[1])
