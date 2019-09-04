SELECT
  uuid,
  exif,
  gps,
  geohash,
  meta_location,
  data_location,
  created_at
FROM exif
WHERE uuid = %(uuid)s
LIMIT %(limit)s
OFFSET %(offset)s
