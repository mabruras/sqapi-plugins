# Data Types

## Intention
This plugin keeps track of data types for each object uuid_refs.


## Accepts
All types


## Storage
### Disk
N/A

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.

## Usage
### Endpoints
* `/datatypes`: Returns all data types with a count (total items).
* `/datatypes?datatype=<datatype>&date=<date>&offset=<offset>&limit=<limit>`: Returns all objects for a given datatype, optionally on a given date.
  * `datatype`: 
    - Required: The data type that you want to search for objects with.
  * `date`: [_Optional_]
    - If specified, the endpoint will only return objects created within a 24h interval of that date. 
    - Valid ISO 8601-date (e.g. 2019-08-24T00:00:00.000Z).
  * The following query params are optional and intended to be used with pagination
    * `limit`: [_Optional_]
      - Limit the amount of results (*Defaults to 10*)
    * `offset`: [_Optional_]
      - Start at a specific index (*Default to 0*)
  * Example: `/datatypes?datatype=video/mp4&date=2019-08-24T00:00:00.000Z&offset=10&limit=20`
* `/datatypes/<uuid>`: Fetch all information on specific data type
