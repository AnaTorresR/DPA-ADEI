set timezone = 'America/Mexico_City';

set role postgres;

create schema semantic;

DROP TABLE IF EXISTS semantic.features;

CREATE TABLE semantic.features(
facility_type varchar,
risk varchar,
zip numeric(12,4),
inspection_date timestamp without time zone,
inspection_type varchar,
violations varchar,
last_inspection varchar,
first_inspection varchar,
label integer
);
