INSERT INTO hashes (
  id,
  uuid,
  meta_location,
  data_location,
  md5,
  sha1,
  sha256
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(md5)s,
  %(sha1)s,
  %(sha256)s
)
