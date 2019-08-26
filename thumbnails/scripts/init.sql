CREATE TABLE IF NOT EXISTS thumbnails (
  id             TEXT NOT NULL PRIMARY KEY,
  uuid           TEXT NOT NULL,
  meta_location  TEXT,
  data_location  TEXT,
  thumbnail      bytea,
  created_at     TIMESTAMPTZ DEFAULT Now()
);
