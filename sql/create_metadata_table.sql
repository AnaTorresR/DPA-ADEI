set timezone = 'America/Mexico_City';

set role postgres;

DROP TABLE IF EXISTS metadata;

CREATE TABLE metadata(
  Task varchar,
  Ingestion varchar,
  Fecha timestamp without time zone,
  Autor varchar
);
