INSERT INTO faces (
  id,
  uuid,
  meta_location,
  data_location,
  degrees,
  hash_digest,
  user_id,
  encoding,
  box
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(degrees)s,
  %(hash_digest)s,
  %(user_id)s,
  %(encoding)s,
  %(box)s
)
