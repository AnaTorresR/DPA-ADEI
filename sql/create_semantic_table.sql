set timezone = 'America/Mexico_City';

set role postgres;

create schema semantic;

DROP TABLE IF EXISTS semantic.features;

CREATE TABLE semantic.features(
facility_type varchar,
inspection_type varchar,
risk_high numeric(12,4),
risk_medium numeric(12,4),
risk_low numeric(12,4),
zip numeric(12,4),
inspection_date timestamp without time zone,
violations varchar,
last_inspection varchar,
first_inspection varchar,
label integer
);
