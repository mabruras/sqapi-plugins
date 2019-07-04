-- Select values based on uuid_ref
SELECT *
FROM languages
WHERE uuid_ref = %(uuid_ref)s
