{{ config(materialized='table') }}

with ranked as (
    select
        callsign,
        origin_country,
        longitude,
        latitude,
        last_contact,
        row_number() over (
            partition by callsign
            order by last_contact desc
        ) as row_num
    from {{ ref('stg_flights') }}
    where callsign is not null
)
, deduped as (
    select *
    from ranked
    where row_num = 1
)

select * from deduped
