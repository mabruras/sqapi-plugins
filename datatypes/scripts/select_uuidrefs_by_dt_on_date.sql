-- Select values based on uuid_ref
SELECT dt.* 
FROM datatypes dt
WHERE dt.mime_type =  %(datatype)s
AND dt.created_at BETWEEN %(anydate)s::date AND %(anydate)s::date + interval '1' day