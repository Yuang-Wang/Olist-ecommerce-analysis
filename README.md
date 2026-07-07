## Project Overview

This project is an end-to-end e-commerce data analysis project based on the Brazilian Olist dataset.

The goal of this project is to analyze sales performance, delivery efficiency, and customer satisfaction by combining Python data cleaning, SQL analysis, and Power BI dashboard visualization.

The analysis focuses on the following business questions:

- How much revenue did the platform generate?
- Which product categories contributed the most revenue?
- How did monthly revenue change over time?
- How does late delivery affect customer review scores?
- Which product categories have the highest late delivery rates?
- What does the overall review score distribution look like?

---

## Tools Used

- Python
- Pandas
- NumPy
- SQL / MySQL
- Power BI
- DAX
- Excel
- Data Cleaning
- Data Transformation
- Business Intelligence Dashboarding
- Data Visualization

---

## Dataset

The dataset is based on the Olist Brazilian e-commerce public dataset. It contains order, customer, seller, product, payment, review, and delivery information.

Main raw datasets used:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

---

## Project Workflow

```text
Raw CSV Files
      ↓
Python Data Cleaning
      ↓
Cleaned Master Dataset
      ↓
MySQL / SQL Analysis
      ↓
Power BI Dashboard
      ↓
Business Insights
```

---

## Data Cleaning with Python

Python was used to clean and transform the raw Olist datasets before importing the final dataset into MySQL and Power BI.

Main cleaning and transformation steps included:

- Loaded raw CSV files using Pandas
- Converted order and review date columns into datetime format
- Created monthly order fields
- Calculated delivery days, estimated delivery days, and delivery delay days
- Created a late delivery indicator
- Aggregated payment information by order
- Aggregated review scores by order
- Merged orders, order items, customers, products, sellers, payments, and reviews into one master dataset
- Added English product category names
- Created item-level revenue using product price and freight value
- Exported a cleaned dataset for analysis
- Exported a MySQL-friendly version with missing values handled

Final cleaned datasets:

- `olist_order_items_master.csv`
- `olist_order_items_master_mysql.csv`

---

## Power BI Dashboard Preview

### Business Overview



### Delivery & Customer Satisfaction Analysis



---

## Key Metrics

| Metric | Value |
|---|---:|
| Total Revenue | $15.84M |
| Total Orders | 99K |
| Average Order Value | $160.58 |
| Average Review Score | 4.03 |
| Late Delivery Rate | 6.59% |

---

## Dashboard Pages

### Page 1: Business Overview

This page provides a high-level summary of overall business performance.

It includes:

- Total revenue
- Total orders
- Average order value
- Average review score
- Late delivery rate
- Revenue by product category
- Monthly revenue trend
- Order year filter

### Page 2: Delivery & Customer Satisfaction Analysis

This page focuses on delivery performance and customer satisfaction.

It includes:

- Average review score by delivery status
- Late delivery rate by product category
- Delivery days distribution
- Review score distribution
- Product category filter

---

## Key Insights

### 1. Revenue is concentrated in several major product categories

The highest revenue-generating categories include health & beauty, watches & gifts, bed/bath/table, sports/leisure, and computer accessories.

The top product category generated approximately **$1.44M** in revenue.

---

### 2. Monthly revenue increased strongly over time

Revenue showed strong growth from late 2016 to 2018.

The monthly revenue trend suggests that Olist experienced significant business expansion during the dataset period.

---

### 3. Late delivery has a clear negative impact on customer satisfaction

On-time orders have an average review score of **4.2**, while late orders have an average review score of only **2.3**.

This suggests that delivery performance is strongly connected to customer satisfaction.

---

### 4. Most orders were delivered within 8-14 days

The largest delivery time group was **8-14 days**, with approximately **36K orders**.

| Delivery Days Group | Orders |
|---|---:|
| 0-3 days | 11K |
| 4-7 days | 25K |
| 8-14 days | 36K |
| 15-30 days | 22K |
| 30+ days | 4K |

---

### 5. Some product categories have much higher late delivery rates

The categories with the highest late delivery rates include:

| Product Category | Late Delivery Rate |
|---|---:|
| Furniture mattresses | 13.51% |
| Home comfort 2 | 13.33% |
| Audio | 11.60% |
| Christmas supplies | 10.00% |
| Fashion underwear | 9.45% |

These categories may require further investigation into seller performance, logistics issues, or product handling complexity.

---

### 6. Review scores are generally positive

The review score distribution is strongly skewed toward 5-star reviews.

| Review Score | Orders |
|---|---:|
| 1 | 11K |
| 2 | 3K |
| 3 | 8K |
| 4 | 19K |
| 5 | 57K |

Although most customers gave positive reviews, low-score reviews still represent an important customer experience issue, especially when connected to delivery delays.

---

## Example DAX Measures

```DAX
Total Revenue =
SUM('olist_order_items_master'[price])
```

```DAX
Total Orders =
DISTINCTCOUNT('olist_order_items_master'[order_id])
```

```DAX
Average Order Value =
DIVIDE([Total Revenue], [Total Orders])
```

```DAX
Average Review Score =
AVERAGE('olist_order_items_master'[avg_review_score])
```

```DAX
Late Orders =
CALCULATE(
    [Total Orders],
    'olist_order_items_master'[is_late] = 1
)
```

```DAX
Late Delivery Rate =
DIVIDE([Late Orders], [Total Orders])
```

```DAX
Delivery Days Group =
SWITCH(
    TRUE(),
    ISBLANK([delivery_days]), "Unknown",
    [delivery_days] <= 3, "0-3 days",
    [delivery_days] <= 7, "4-7 days",
    [delivery_days] <= 14, "8-14 days",
    [delivery_days] <= 30, "15-30 days",
    "30+ days"
)
```

```DAX
Delivery Days Group Sort =
SWITCH(
    TRUE(),
    ISBLANK([delivery_days]), 99,
    [delivery_days] <= 3, 1,
    [delivery_days] <= 7, 2,
    [delivery_days] <= 14, 3,
    [delivery_days] <= 30, 4,
    5
)
```

---

## Business Recommendations

Based on the analysis, Olist should focus on improving delivery reliability, especially for categories with high late delivery rates.

Recommended actions:

1. Investigate sellers and logistics partners in high-delay product categories.
2. Improve estimated delivery time accuracy.
3. Monitor late delivery rate as a core customer experience KPI.
4. Prioritize operational improvements for categories with both high revenue and high delivery risk.
5. Use customer review data to identify delivery-related pain points.

---

## Project Structure

```text
olist-ecommerce-sales-delivery-analysis/
│
├── data/
│   ├── raw/
│   │   └── original Olist CSV files
│   │
│   └── cleaned/
│       ├── olist_order_items_master.csv
│       └── olist_order_items_master_mysql.csv
│
├── python/
│   └── data_cleaning.py
│
├── sql/
│   └── SQL analysis queries
│
├── powerbi/
│   └── e-business.pbix
│
├── images/
│   ├── business_overview.png
│   └── delivery_customer_satisfaction.png
│
└── README.md
```

---

## Skills Demonstrated

- Python data cleaning
- Pandas data transformation
- Handling missing values
- Datetime feature engineering
- Dataset merging and aggregation
- SQL joins and aggregation
- KPI calculation
- DAX measures
- Power BI dashboard design
- Business intelligence reporting
- Delivery performance analysis
- Customer satisfaction analysis
- Data storytelling
