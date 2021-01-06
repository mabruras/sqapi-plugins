INSERT INTO face_encodings (
  hash_digest,
  user_id,
  low_vectors,
  high_vectors,
  box,
  degrees
) VALUES (
  %(hash_digest)s,
  %(user_id)s,
  CUBE(%(low_vectors)s),
  CUBE(%(high_vectors)s),
  %(box)s,
  %(degrees)s
)
ON CONFLICT DO NOTHING
