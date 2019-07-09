SELECT uuid_ref, user_id, box, created_at
FROM faces
WHERE uuid_ref = %(uuid_ref)s
