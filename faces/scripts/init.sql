CREATE EXTENSION IF NOT EXISTS CUBE;

CREATE TABLE IF NOT EXISTS face_images (
  uuid          TEXT NOT NULL PRIMARY KEY,
  meta_location TEXT,
  data_location TEXT,
  hash_digest   TEXT,
  created_at    TIMESTAMPTZ DEFAULT Now()
);
CREATE INDEX IF NOT EXISTS face_img_hash_digest_idx ON face_images (hash_digest);
CREATE INDEX IF NOT EXISTS face_img_created_at_idx ON face_images (created_at DESC);

CREATE TABLE IF NOT EXISTS face_encodings (
  id            SERIAL PRIMARY KEY,
  hash_digest   TEXT,
  user_id       TEXT,
  low_vectors   CUBE,
  high_vectors  CUBE,
  box           JSON,
  degrees       INTEGER,
  UNIQUE        (hash_digest, low_vectors, high_vectors)
);

CREATE INDEX IF NOT EXISTS face_enc_vectors_idx ON face_encodings (low_vectors, high_vectors);
CREATE INDEX IF NOT EXISTS face_enc_hash_digest_idx ON face_encodings (hash_digest);
CREATE INDEX IF NOT EXISTS face_enc_user_id_idx ON face_encodings (user_id);
