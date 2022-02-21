update stars
set parallax = 0
where parallax = 'NULL';

-- drop view stars_flux_v
CREATE VIEW  stars_flux_v AS
select * from stars
order by flux_visible_light::decimal DESC;

-- drop view stars_parallax
CREATE VIEW  stars_parallax AS
select * from stars
order by parallax::decimal DESC;



 -- select * from stars_flux_v;
-- select * from stars_parallax;