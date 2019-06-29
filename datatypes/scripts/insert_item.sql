-- Inserting values into custom table
INSERT INTO datatypes (
  uuid_ref,
  meta_location,
  data_location,
  mime_type
) VALUES (
  %(uuid_ref)s,
  %(meta_location)s,
  %(data_location)s,
  %(mime_type)s
)
