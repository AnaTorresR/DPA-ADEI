set timezone = 'America/Mexico_City';

set role postgres;

DROP TABLE IF EXISTS monitoring;

CREATE TABLE monitoring(
id_inspection integer,
dba_name varchar,
license integer,
facility_type varchar,
risk varchar,
address varchar,
inspection_date timestamp with time zone,
inspection_type varchar,
violations varchar,
ground_truth smallint,
score numeric,
label integer,
predictions_date timestamp with time zone,
model varchar
);
