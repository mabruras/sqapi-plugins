SELECT uuid, user_id, box, created_at
FROM faces
WHERE uuid = %(uuid)s
