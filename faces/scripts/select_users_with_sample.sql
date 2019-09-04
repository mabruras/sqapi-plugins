SELECT total, faces.user_id, uuid, box, created_at
FROM (
  SELECT user_id, max(id) as id, count(*) as total
  FROM faces
  GROUP BY user_id
) as grouped_faces
INNER JOIN faces ON
  faces.user_id = grouped_faces.user_id AND
  faces.id = grouped_faces.id
ORDER BY
  created_at DESC
LIMIT %(limit)s
OFFSET %(offset)s
