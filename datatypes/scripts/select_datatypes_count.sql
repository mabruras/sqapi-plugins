-- Select values based on uuid_ref
SELECT count(dt.uuid_ref) as total, dt.datatype as datatype 
FROM datatypes dt
GROUP BY (dt.datatype)