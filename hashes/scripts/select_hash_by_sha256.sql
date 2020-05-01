SELECT *
FROM hashes
WHERE sha256 = %(sha256)s
LIMIT %(limit)s
OFFSET %(offset)s
