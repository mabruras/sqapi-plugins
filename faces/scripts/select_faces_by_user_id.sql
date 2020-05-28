SELECT uuid, user_id, degrees, box, created_at
FROM faces
WHERE user_id = %(user_id)s
