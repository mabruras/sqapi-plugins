SELECT user_id, degrees, box
FROM face_encodings
WHERE hash_digest = %(hash_digest)s
