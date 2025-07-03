{{ config(materialized='view') }}

with source as (

    select * from {{ source('raw', 'raw_flights') }}

),

renamed as (

    select
        icao24,
        trim(callsign) as callsign,
        origin_country,
        last_position_update,
        last_contact,
        longitude,
        latitude,
        on_ground,
        timestamp as record_timestamp

    from source

)

select * from renamed
