-- Inserting values into custom table
INSERT INTO lang_detect (
  uuid_ref,
  meta_location,
  data_location,
  lang
) VALUES (
  %(uuid_ref)s,
  %(meta_location)s,
  %(data_location)s,
  %(lang)s
)
