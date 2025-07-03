{{ config(materialized='view') }}

select
  date_trunc('day', last_contact) as flight_day,
  origin_country,
  count(*) as num_active_flights
from {{ ref('stg_flights') }}
where longitude is not null and latitude is not null
group by 1, 2
