INSERT INTO sizes (
  id,
  uuid,
  meta_location,
  data_location,
  metadata_size,
  data_size
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(metadata_size)s,
  %(data_size)s
)
