-- Create your own database initialization here
CREATE TABLE IF NOT EXISTS languages (
  uuid_ref          TEXT NOT NULL PRIMARY KEY,
  meta_location     TEXT,
  data_location     TEXT,
  lang              TEXT,
  created_at        TIMESTAMPTZ DEFAULT Now(),
  updated_at        TIMESTAMPTZ DEFAULT Now()
);
