-- Select values based on uuid_ref
SELECT *
FROM languages
WHERE lang = %(lang)s
