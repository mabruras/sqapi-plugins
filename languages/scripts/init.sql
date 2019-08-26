-- Create your own database initialization here
CREATE TABLE IF NOT EXISTS languages (
  id                TEXT NOT NULL PRIMARY KEY,
  uuid              TEXT NOT NULL,
  meta_location     TEXT,
  data_location     TEXT,
  lang              TEXT,
  created_at        TIMESTAMPTZ DEFAULT Now(),
  updated_at        TIMESTAMPTZ DEFAULT Now()
);
