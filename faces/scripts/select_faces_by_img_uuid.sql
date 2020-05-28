SELECT uuid, user_id, degrees, box, created_at
FROM faces
WHERE uuid = %(uuid)s
