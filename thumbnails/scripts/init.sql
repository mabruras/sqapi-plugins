CREATE TABLE IF NOT EXISTS thumbnails (
  id             TEXT NOT NULL PRIMARY KEY,
  uuid           TEXT NOT NULL,
  meta_location  TEXT,
  data_location  TEXT,
  hash_digest    TEXT,
  thumbnail      bytea,
  created_at     TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS thumbnails_hash_digest_idx ON faces (hash_digest desc);
CREATE INDEX IF NOT EXISTS thumbnails_uuid_idx ON faces (uuid desc);
