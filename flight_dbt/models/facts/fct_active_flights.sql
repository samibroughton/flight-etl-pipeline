{{ config(materialized='table') }}

with flights as (

    select * from {{ ref('stg_flights') }}

),

by_minute as (

    select
        date_trunc('minute', record_timestamp) as minute,
        count(*) as num_active_flights
    from flights
    where not on_ground
    group by 1

)

select * from by_minute
order by minute desc
