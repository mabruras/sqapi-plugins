SELECT uuid_ref, user_id, box, created_at
FROM faces
WHERE user_id = %(user_id)s
