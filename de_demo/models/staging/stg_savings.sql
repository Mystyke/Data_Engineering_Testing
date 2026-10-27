select
    acct_id as account_id,
    'P' || lpad(cast(cust_id as varchar), 6, '0') as party_id,
    cast(balance_gbp as double) as balance_gbp,
    cast(opened as date) as opened_date,
    product_name,
    'savings' as product_type
from {{ ref('src_savings') }}