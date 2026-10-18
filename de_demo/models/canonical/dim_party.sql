select
    p.party_id,
    p.full_name,
    p.date_of_birth,
    p.segment,
    p.postcode,
    p.party_id in (select party_id from {{ ref('stg_current_accounts') }}) as has_current_account,
    p.party_id in (select party_id from {{ ref('stg_savings') }}) as has_savings,
    p.party_id in (select party_id from {{ ref('stg_mortgages') }}) as has_mortgage
from {{ ref('stg_party') }} as p
qualify row_number() over (partition by p.party_id order by p.party_id) = 1