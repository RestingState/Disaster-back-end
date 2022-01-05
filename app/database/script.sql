
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
	owner character varying NOT NULL,
    launchdate date,
    launchsite character varying NOT NULL,
    inclination character varying NOT NULL,
    ascending_node_longitude character varying NOT NULL,
    eccentricity character varying NOT NULL,
    pericenter_argument character varying NOT NULL,
    average_anomaly character varying NOT NULL,
    call_frequency character varying NOT NULL,
    PRIMARY KEY (norad_id)
);

CREATE TABLE IF NOT EXISTS public.stars
(   
    id serial NOT NULL,
    name character varying NOT NULL,
    right_ascension character varying NOT NULL,
    declination character varying NOT NULL,
    flux_visible_light decimal NOT NULL,
    parallax decimal NOT NULL,
    spectral_type character varying NOT NULL,
    PRIMARY KEY (id)
);
