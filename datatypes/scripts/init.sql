CREATE TABLE IF NOT EXISTS datatypes (
  uuid_ref       TEXT NOT NULL PRIMARY KEY,
  meta_location  TEXT,
  data_location  TEXT,
  mime_type      TEXT,
  created_at     TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS mime_t_fd_idx ON datatypes (mime_type);
CREATE INDEX IF NOT EXISTS mime_t_created_idx ON datatypes (created_at desc); 
