-- Inserting values into custom table
INSERT INTO thumbnails (
  uuid_ref,
  meta_location,
  data_location,
  thumbnail
) VALUES (
  %(uuid_ref)s,
  %(meta_location)s,
  %(data_location)s,
  %(thumbnail)s
)
