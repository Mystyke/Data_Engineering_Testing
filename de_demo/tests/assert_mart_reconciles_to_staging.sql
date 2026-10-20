with mart as (
    select
        sum(current_balance_gbp) as c,
        sum(savings_balance_gbp) as s,
        sum(mortgage_outstanding_gbp) as m
    from {{ ref('client_wealth_summary') }}
),

src as (
    select
        (select sum(balance_gbp) from {{ ref('stg_current_accounts') }}) as c,
        (select sum(balance_gbp) from {{ ref('stg_savings') }}) as s,
        (select sum(balance_gbp) from {{ ref('stg_mortgages') }}) as m
)

select *
from mart, src
where abs(mart.c - src.c) > 0.01
   or abs(mart.s - src.s) > 0.01
   or abs(mart.m - src.m) > 0.01