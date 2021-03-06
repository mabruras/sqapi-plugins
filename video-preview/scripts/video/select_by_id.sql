SELECT * FROM video_preview
WHERE uuid = %(uuid)s
LIMIT %(limit)s
OFFSET %(offset)s
