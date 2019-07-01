-- Select values based on uuid_ref
SELECT *
FROM lang_detect
WHERE uuid_ref = %(uuid_ref)s
