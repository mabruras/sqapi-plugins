-- Select values based on uuid_ref
SELECT count(dt.uuid_ref) as total, dt.mime_type as datatype 
FROM datatypes dt
GROUP BY (dt.mime_type)