SELECT count(dt.uuid) as total, dt.datatype
FROM datatypes dt
GROUP BY (dt.datatype)
