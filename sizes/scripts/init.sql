CREATE TABLE IF NOT EXISTS sizes (
  id            TEXT NOT NULL PRIMARY KEY,
  uuid          TEXT NOT NULL,
  meta_location TEXT,
  data_location TEXT,
  metadata_size INTEGER,
  data_size     INTEGER,
  created_at    TIMESTAMPTZ DEFAULT Now()
);
