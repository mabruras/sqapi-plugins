-- Create your own database initialization here
CREATE TABLE IF NOT EXISTS thumbnails (
  uuid_ref       TEXT NOT NULL PRIMARY KEY,
  meta_location  TEXT,
  data_location  TEXT,
  thumb_location TEXT,
  received_date  TIMESTAMPTZ DEFAULT Now(),
  created_at     TIMESTAMPTZ DEFAULT Now()
);
