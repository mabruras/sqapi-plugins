CREATE TABLE IF NOT EXISTS faces (
  id            TEXT NOT NULL PRIMARY KEY,
  uuid_ref      TEXT,
  meta_location TEXT,
  data_location TEXT,
  user_id       TEXT,
  encoding      FLOAT [],
  box           json,
  created_at    TIMESTAMPTZ DEFAULT Now()
);
