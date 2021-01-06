INSERT INTO face_images (
  uuid,
  meta_location,
  data_location,
  hash_digest
) VALUES (
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(hash_digest)s
)
ON CONFLICT DO NOTHING
