set timezone = 'America/Mexico_City';

set role postgres;

-------- IngestionMetadata

DROP TABLE IF EXISTS ingestion_metadata;

CREATE TABLE ingestion_metadata(
  Ingestion varchar,
  Fecha timestamp without time zone,
  Autor varchar
);
------------- AlmacenamientoMetadata
DROP TABLE IF EXISTS almacenamieto_metadata;

CREATE TABLE almacenamiento_metadata(
  Fecha timestamp without time zone,
  Autor varchar,
  N_cols integer,
  N_registros integer
);

--------------CleaningMetadata
DROP TABLE IF EXISTS cleaning_metadata;

CREATE TABLE cleaning_metadata(
  Fecha timestamp without time zone,
  Autor varchar,
  N_cols integer,
  N_registros integer
);


--------------FEMetadata
DROP TABLE IF EXISTS feature_engineering_metadata;

  CREATE TABLE feature_engineering_metadata(
    Fecha timestamp without time zone,
    Autor varchar,
    N_cols integer,
    N_registros integer
  );
