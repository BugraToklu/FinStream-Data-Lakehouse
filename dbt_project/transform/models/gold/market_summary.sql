{{ config(materialized='table') }}
SELECT
    symbol,
    count(*) as total_trades,
    avg(price) as avg_price,
    sum(total_value) as total_volume
FROM {{ ref('cleaned_trades') }}
GROUP BY symbol