SELECT *
FROM hashes
WHERE sha1 = %(sha1)s
LIMIT %(limit)s
OFFSET %(offset)s
