CREATE TABLE IF NOT EXISTS datatypes (
  id             TEXT NOT NULL PRIMARY KEY,
  uuid           TEXT NOT NULL,
  meta_location  TEXT,
  data_location  TEXT,
  datatype       TEXT,
  created_at     TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS data_t_fd_idx ON datatypes (datatype);
CREATE INDEX IF NOT EXISTS data_t_created_idx ON datatypes (created_at desc); 
