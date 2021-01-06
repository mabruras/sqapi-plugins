SELECT fi.uuid, fi.hash_digest, fe.user_id, fe.degrees, fe.box, fi.created_at
FROM face_images fi
INNER JOIN face_encodings fe
ON fi.hash_digest = fe.hash_digest
WHERE user_id = %(user_id)s
