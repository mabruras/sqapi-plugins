-- Select values based on uuid_ref
SELECT dt.* 
FROM datatypes dt
WHERE dt.mime_type =  %(datatype)s