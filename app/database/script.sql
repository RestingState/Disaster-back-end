
CREATE TABLE IF NOT EXISTS public."user"
(
    id serial NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    city_id bigint NOT NULL,
    username character varying NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.category
(
    id serial NOT NULL,
    name character varying NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.user_category
(
    user_id serial NOT NULL,
    category_id serial NOT NULL
);

CREATE TABLE IF NOT EXISTS public.city
(
    id serial NOT NULL,
    name character varying NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public."user"
    ADD FOREIGN KEY (city_id)
    REFERENCES public.city (id) ;

ALTER TABLE IF EXISTS public.user_category
    ADD FOREIGN KEY (user_id)
    REFERENCES public."user" (id);

ALTER TABLE IF EXISTS public.user_category
    ADD FOREIGN KEY (category_id)
    REFERENCES public.category (id) ;


-- additional tables for storing information 
CREATE TABLE IF NOT EXISTS public.satellites
(
    norad_id bigint NOT NULL,
	satname character varying NOT NULL,
    inclination character varying NOT NULL,
    ascending_node_longitude character varying NOT NULL,
    eccentricity character varying NOT NULL,
    pericenter_argument character varying NOT NULL,
    average_anomaly character varying NOT NULL,
    call_frequency character varying NOT NULL,
    PRIMARY KEY (norad_id)
);

CREATE TABLE IF NOT EXISTS public.satellite_data_raw
(
    norad_id bigint,
    sat_data jsonb
);

CREATE TABLE IF NOT EXISTS public.stars
(   
    id serial NOT NULL,
    name character varying,
    right_ascension character varying,
    declination character varying,
    flux_visible_light character varying,
    parallax character varying,
    spectral_type character varying,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.planet
(
    id serial NOT NULL,
    name character varying,
    mass character varying,
    density character varying,
    mean_temperature character varying,
    radius character varying,
    visual_mag character varying,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.planet_coordinates
(
    id serial NOT NULL,
    planet_id bigint,
    "date" date,
    dec character varying,
    ra character varying,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public."planet_coordinates"
    ADD FOREIGN KEY (planet_id)
    REFERENCES public.planet (id) ;
    
    
    
    
create procedure delete_planet_coordinates_data (
start_time date,
end_time date)
language plpgsql
as $$
begin
   delete from planet_coordinates 
   where date between start_time and end_time ;
   
   commit;
end; $$

-- example how to call procedure
-- call delete_planet_coordinates_data('2003-01-01','2013-05-05');
