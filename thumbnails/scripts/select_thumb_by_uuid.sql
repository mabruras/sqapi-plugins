-- Select values based on uuid_ref
SELECT *
FROM thumbnails
WHERE uuid_ref = %(uuid_ref)s
