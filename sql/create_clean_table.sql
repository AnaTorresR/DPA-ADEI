set timezone = 'America/Mexico_City';

set role postgres;

create schema clean;

DROP TABLE IF EXISTS clean.features;

CREATE TABLE clean.features(
inspection_id varchar,
dba_name varchar,
aka_name varchar,
license varchar,
facility_type varchar,
risk varchar,
address varchar,
city varchar,
state varchar,
zip integer,
inspection_date timestamp without time zone,
inspection_type varchar,
results varchar,
violations varchar,
latitude varchar,
longitude varchar
);
