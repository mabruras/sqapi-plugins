SELECT DISTINCT ON (user_id)
  grouped_faces.total,
  grouped_faces.user_id,
  grouped_faces.hash_digest,
  face_images.uuid,
  face_encodings.degrees,
  face_encodings.box,
  face_images.created_at
FROM (
  SELECT
    user_id,
    hash_digest,
    max(id) as id,
    count(*) as total
  FROM face_encodings
  GROUP BY user_id, hash_digest
) grouped_faces
INNER JOIN face_images face_images
  ON face_images.hash_digest = grouped_faces.hash_digest
INNER JOIN face_encodings face_encodings
  ON face_encodings.user_id = grouped_faces.user_id
ORDER BY
  face_images.created_at DESC
LIMIT %(limit)s
OFFSET %(offset)s
