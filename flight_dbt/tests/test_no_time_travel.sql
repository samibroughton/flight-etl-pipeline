-- tests/test_no_time_travel.sql

SELECT *
FROM {{ ref('stg_flights') }}
WHERE last_contact < last_position_update
