CREATE TABLE IF NOT EXISTS exif (
  id            TEXT NOT NULL PRIMARY KEY,
  uuid          TEXT NOT NULL,
  meta_location TEXT,
  data_location TEXT,
  exif          JSON,
  gps           JSON,
  geohash       TEXT,
  created_at    TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS exif_geohash_idx ON exif (geohash desc);
CREATE INDEX IF NOT EXISTS exif_uuid_idx ON exif (uuid desc);
