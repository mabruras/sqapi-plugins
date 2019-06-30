-- Inserting values into custom table
INSERT INTO datatypes (
  uuid_ref,
  meta_location,
  data_location,
  datatype
) VALUES (
  %(uuid_ref)s,
  %(meta_location)s,
  %(data_location)s,
  %(datatype)s
)
