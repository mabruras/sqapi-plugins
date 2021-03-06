CREATE TABLE IF NOT EXISTS video_preview (
  id                  TEXT NOT NULL PRIMARY KEY,
  uuid                TEXT NOT NULL,
  meta_location       TEXT,
  data_location       TEXT,
  video_length        INT,
  frame_count         INT,
  fps                 INT,
  created_at          TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE IF NOT EXISTS video_sequence (
  id                  TEXT NOT NULL PRIMARY KEY,
  video_reference     TEXT NOT NULL,
  center_frame        INT,
  sequence_start      INT,
  sequence_stop       INT,
  frame_spacing       INT,
  center_frame_ts     INT,
  resolution          INT,
  gif                 bytea,
  created_at          TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX IF NOT EXISTS video_preview_uuid_idx ON video_preview (uuid);
CREATE INDEX IF NOT EXISTS video_preview_data_location_idx ON video_preview (data_location);
CREATE INDEX IF NOT EXISTS video_sequence_video_reference_idx ON video_sequence (video_reference);
