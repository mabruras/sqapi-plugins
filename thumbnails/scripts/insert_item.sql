INSERT INTO thumbnails (
  id,
  uuid,
  meta_location,
  data_location,
  hash_digest,
  thumbnail
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(hash_digest)s,
  %(thumbnail)s
)
