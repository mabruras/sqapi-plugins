SELECT hash_digest FROM face_images
WHERE hash_digest = %(hash_digest)s
LIMIT 1
