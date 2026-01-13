{{ config(
    materialized='table'
) }}

SELECT
    trade_id,
    symbol,
    price,
    quantity,
    side,
    -- DÜZELTME: Delta Lake için mikrosaniye (6) hassasiyeti şart
    cast("timestamp" as timestamp(6)) as trade_time,
    (price * quantity) as total_value
FROM {{ source('lakehouse', 'trades') }}
WHERE price > 0
