SELECT DISTINCT ON (user_id) * FROM face_encodings
WHERE user_id IN (
  SELECT user_id FROM face_encodings
  WHERE hash_digest = %(hash_digest)s
  GROUP BY user_id
)
