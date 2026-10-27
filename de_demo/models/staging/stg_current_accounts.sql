select
    account_no as account_id,
    'P' || lpad(regexp_extract(customer_no, '\d+'), 6, '0') as party_id,
    cast(balance as double) as balance_gbp,
    cast(open_date as date) as opened_date,
    status,
    'current_account' as product_type
from {{ ref('src_current_accounts') }}