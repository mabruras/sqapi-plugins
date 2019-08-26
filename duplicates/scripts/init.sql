CREATE TABLE IF NOT EXISTS duplicates (
  id             TEXT NOT NULL PRIMARY KEY,
  uuid           TEXT NOT NULL,
  meta_location  TEXT,
  data_location  TEXT,
  sha_256        TEXT,
  created_at     TIMESTAMPTZ DEFAULT Now()
);
