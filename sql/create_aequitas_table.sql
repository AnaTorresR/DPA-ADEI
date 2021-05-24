set timezone = 'America/Mexico_City';

set role postgres;

DROP TABLE IF EXISTS aequitas;

CREATE TABLE aequitas(
  attribute_name varchar,
  attribute_value varchar,
  for_disparity varchar,
  fnr_disparity varchar,
  tpr_disparity varchar
);
