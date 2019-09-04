SELECT
  uuid,
  exif,
  gps,
  geohash,
  meta_location,
  data_location,
  created_at
FROM exif
LIMIT %(limit)s
OFFSET %(offset)s
