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
* `/datatypes/uuidrefs/?datatype=<datatype>&date=<date>`: Returns all uuid refs for a given datatype, optionally on a given date.
