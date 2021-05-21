set timezone = 'America/Mexico_City';

set role postgres;

create schema results;

DROP TABLE IF EXISTS results.predictions;

CREATE TABLE results.predictions(
id_inspection varchar,
dba_name varchar,
ground_truth smallint,
score numeric,
label integer,
predictions_date timestamp with time zone
);
