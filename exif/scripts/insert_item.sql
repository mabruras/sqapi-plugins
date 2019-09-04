INSERT INTO exif (
  id,
  uuid,
  meta_location,
  data_location,
  exif,
  gps,
  geohash
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(exif)s,
  %(gps)s,
  %(geohash)s
)
