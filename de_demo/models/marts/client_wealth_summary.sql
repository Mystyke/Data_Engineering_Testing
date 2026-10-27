with accounts as (
    select account_id, party_id, balance_gbp, product_type from {{ ref('stg_current_accounts') }}
    union all
    select account_id, party_id, balance_gbp, product_type from {{ ref('stg_savings') }}
    union all
    select account_id, party_id, balance_gbp, product_type from {{ ref('stg_mortgages') }}
),

balances as (
    select
        p.party_id,
        p.full_name,
        p.segment,
        coalesce(sum(case when a.product_type = 'current_account' then a.balance_gbp end), 0) as current_balance_gbp,
        coalesce(sum(case when a.product_type = 'savings' then a.balance_gbp end), 0) as savings_balance_gbp,
        coalesce(sum(case when a.product_type = 'mortgage' then a.balance_gbp end), 0) as mortgage_outstanding_gbp
    from {{ ref('dim_party') }} as p
    left join accounts as a on a.party_id = p.party_id
    group by p.party_id, p.full_name, p.segment
)

select
    *,
    current_balance_gbp + savings_balance_gbp as total_deposits_gbp,
    current_balance_gbp + savings_balance_gbp - mortgage_outstanding_gbp as net_position_gbp
from balances