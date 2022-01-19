
-- drop view satellite_data;
CREATE VIEW satellite_data AS
select
 norad_id,
 TRIM(REPLACE (MAX(substring(tle_second_line, position+2)), '  ', ' ')) AS tle
from
(select
	norad_id,
	REPLACE(((regexp_split_to_array(sat_data->>'tle', '\n'))[2]),'   ',' ' ) as tle_second_line,
    position(norad_id::text IN (regexp_split_to_array(sat_data->>'tle', '\n'))[2]) + length(norad_id::text) as position
   from satellite_data_raw ) t
GROUP BY norad_id;

-- select * from satellite_data;

-- drop view satellite_name
CREATE VIEW satellite_name AS
SELECT
norad_id,
trim(max(substring(satname_line::text,(position+12))))  as satname
from
(select
 norad_id,
(regexp_split_to_array(sat_data->>'info', '\n')) as satname_line ,
position ('satname'::text in (regexp_split_to_array(sat_data->>'info', '\n'))::text) as position
from satellite_data_raw) t
GROUP BY norad_id
;

-- select * from satellite_name;
INSERT INTO satellites
SELECT
	t.norad_id,  REPLACE(substring (sat_name::text, 0, length(sat_name) - 6 ), '\', '') as satname
    , split_part(tle::TEXT, ' ', 1)::character varying AS inclination
    , split_part(tle::TEXT, ' ', 2)::character varying AS ascending_node_longitude
    , split_part(tle::TEXT, ' ', 3)::character varying AS eccentricity
    , split_part(tle::TEXT, ' ', 4)::character varying AS pericenter_argument
    , split_part(tle::TEXT, ' ', 5)::character varying AS average_anomaly
    , split_part(tle::TEXT, ' ', 6)::character varying AS call_frequency
from
(select norad_id,
 TRIM(REPLACE (satname, '\"transactionscount\": ', '')) as sat_name
 from satellite_name) t
inner join satellite_data
on t.norad_id = satellite_data.norad_id
where tle is NOT NULL
order by t.norad_id asc;


