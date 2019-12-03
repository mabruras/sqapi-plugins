CREATE TABLE IF NOT EXISTS faces (
  id            TEXT NOT NULL PRIMARY KEY,
  uuid          TEXT,
  meta_location TEXT,
  data_location TEXT,
  hash_digest   TEXT,
  user_id       TEXT,
  encoding      FLOAT [],
  box           json,
  created_at    TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS faces_hash_digest_idx ON faces (hash_digest desc);
CREATE INDEX IF NOT EXISTS faces_created_at_idx ON faces (created_at desc);
CREATE INDEX IF NOT EXISTS faces_user_id_idx ON faces (user_id desc);
CREATE INDEX IF NOT EXISTS faces_uuid_idx ON faces (uuid desc);
