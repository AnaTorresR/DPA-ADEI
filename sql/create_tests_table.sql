set timezone = 'America/Mexico_City';

set role postgres;

DROP TABLE IF EXISTS tests;

CREATE TABLE tests(
  Test varchar,
  Fecha timestamp with time zone,
  Autor varchar
);
