select
    upper(party_ref) as party_id,
    full_name,
    cast(dob as date) as date_of_birth,
    segment,
    postcode
from {{ ref('src_crm_party') }}