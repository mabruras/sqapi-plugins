CREATE TABLE IF NOT EXISTS hashes (
  id             TEXT NOT NULL PRIMARY KEY,
  uuid           TEXT NOT NULL,
  meta_location  TEXT,
  data_location  TEXT,
  md5            TEXT,
  sha1           TEXT,
  sha256         TEXT,
  created_at     TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS hashes_uuid_idx ON hashes (uuid);
CREATE INDEX IF NOT EXISTS hashes_md5_idx ON hashes (md5);
CREATE INDEX IF NOT EXISTS hashes_sha1_idx ON hashes (sha1);
CREATE INDEX IF NOT EXISTS hashes_sha256_idx ON hashes (sha256);
