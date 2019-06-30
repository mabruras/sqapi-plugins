-- Select values based on uuid_ref
SELECT dt.* 
FROM datatypes dt
WHERE dt.datatype =  %(datatype)s