INSERT INTO duplicates (
  id,
  uuid,
  meta_location,
  data_location,
  sha_256
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(sha_256)s
)
