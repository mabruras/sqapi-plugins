-- Select values based on uuid_ref
SELECT *
FROM lang_detect
WHERE lang = %(lang)s
