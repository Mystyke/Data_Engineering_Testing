select
    mortgage_id as account_id,
    upper(party_id) as party_id,
    cast(outstanding_balance as double) as balance_gbp,
    cast(start_date as date) as opened_date,
    cast(rate_pct as double) as rate_pct,
    'mortgage' as product_type
from {{ ref('src_mortgages') }}