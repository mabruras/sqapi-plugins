SELECT dt.*
FROM datatypes dt
WHERE dt.datatype = %(datatype)s
LIMIT %(limit)s
OFFSET %(offset)s
