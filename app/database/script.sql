CREATE TABLE IF NOT EXISTS public."user"
(
    id serial NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    country character varying NOT NULL,
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

ALTER TABLE IF EXISTS public.user_category
    ADD FOREIGN KEY (user_id)
    REFERENCES public."user" (id) 
	NOT VALID;


ALTER TABLE IF EXISTS public.user_category
    ADD FOREIGN KEY (category_id)
    REFERENCES public.category (id)
    NOT VALID;