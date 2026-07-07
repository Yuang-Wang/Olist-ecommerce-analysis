USE ecommerce_analysis;

-- 1. Overall business summary
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    ROUND(SUM(item_revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score,
    ROUND(AVG(CASE WHEN is_late IN (0, 1) THEN is_late END) * 100, 2) AS late_delivery_rate
FROM olist_order_items_master;


-- 2. Monthly revenue trend
SELECT
    order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    ROUND(SUM(item_revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score
FROM olist_order_items_master
GROUP BY order_month
ORDER BY order_month;


-- 3. Top 10 product categories by revenue
SELECT
    product_category_name_english AS product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    ROUND(AVG(price), 2) AS avg_item_price,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score
FROM olist_order_items_master
WHERE product_category_name_english <> 'Unknown'
GROUP BY product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Revenue by customer state
SELECT
    customer_state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    ROUND(SUM(item_revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score
FROM olist_order_items_master
GROUP BY customer_state
ORDER BY total_revenue DESC;


-- 5. Delivery status vs review score
SELECT
    CASE
        WHEN is_late = 1 THEN 'Late'
        WHEN is_late = 0 THEN 'On Time'
        ELSE 'Unknown'
    END AS delivery_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(NULLIF(delivery_days, -1)), 2) AS avg_delivery_days,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score
FROM olist_order_items_master
GROUP BY
    CASE
        WHEN is_late = 1 THEN 'Late'
        WHEN is_late = 0 THEN 'On Time'
        ELSE 'Unknown'
    END
ORDER BY total_orders DESC;


-- 6. Delivery delay group vs review score
SELECT
    CASE
        WHEN delivery_delay_days = -999 THEN 'Unknown'
        WHEN delivery_delay_days <= -7 THEN '7+ Days Early'
        WHEN delivery_delay_days BETWEEN -6 AND -1 THEN '1-6 Days Early'
        WHEN delivery_delay_days = 0 THEN 'On Estimated Date'
        WHEN delivery_delay_days BETWEEN 1 AND 7 THEN '1-7 Days Late'
        ELSE '8+ Days Late'
    END AS delivery_delay_group,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(NULLIF(delivery_days, -1)), 2) AS avg_delivery_days,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score
FROM olist_order_items_master
GROUP BY
    CASE
        WHEN delivery_delay_days = -999 THEN 'Unknown'
        WHEN delivery_delay_days <= -7 THEN '7+ Days Early'
        WHEN delivery_delay_days BETWEEN -6 AND -1 THEN '1-6 Days Early'
        WHEN delivery_delay_days = 0 THEN 'On Estimated Date'
        WHEN delivery_delay_days BETWEEN 1 AND 7 THEN '1-7 Days Late'
        ELSE '8+ Days Late'
    END
ORDER BY avg_review_score DESC;


-- 7. Top 10 sellers by revenue
SELECT
    seller_id,
    seller_state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    ROUND(AVG(NULLIF(avg_review_score, -1)), 2) AS avg_review_score
FROM olist_order_items_master
GROUP BY seller_id, seller_state
ORDER BY total_revenue DESC
LIMIT 10;


-- 8. Payment type analysis
SELECT
    main_payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    ROUND(AVG(total_payment_value), 2) AS avg_payment_value,
    ROUND(AVG(max_installments), 2) AS avg_installments
FROM olist_order_items_master
WHERE main_payment_type <> 'Unknown'
GROUP BY main_payment_type
ORDER BY total_revenue DESC;