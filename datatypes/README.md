# Datatypes

## Intention
This plugin keeps track of datatypes for each object uuid_refs.


## Accepts
All types


## Storage
### Disk
N/A

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.

## Usage
### Endpoints
* `/datatypes/`: Returns all datatypes with a count (total items).
* `/datatypes/uuidrefs/?datatype=<datatype>&date=<date>`: Returns all objects for a given datatype, optionally on a given date.
  * `datatype`: 
    - Required: The datatype that you want to search for objects with.
  * `date`:
    - If specified, the endpoint will only return objects created within a 24h interval of that date. 
    - Valid ISO 8601-date (e.g. 2019-08-24T00:00:00.000Z).
  * Example: `/datatypes/uuidrefs/?datatype=video/mp4&date=2019-08-24T00:00:00.000Z`
