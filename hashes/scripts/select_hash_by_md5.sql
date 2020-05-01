SELECT *
FROM hashes
WHERE md5 = %(md5)s
LIMIT %(limit)s
OFFSET %(offset)s
