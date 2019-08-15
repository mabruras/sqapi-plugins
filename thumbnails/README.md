# Thumbnails

## Intention
This plugin is intended to create, store and serve thumbnails, for each incoming image file.


## Accepts
Image types; `image/jpeg`, `image/png`, `image/gif`.


## Storage
### Database
The thumbnails are stored with its uuid references in the database as a
[`bytea`-type](https://www.postgresql.org/docs/current/datatype-binary.html).

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.

## Usage
### Endpoints
* `/thumbnails/<uuid_ref>`: returns a thumbnail based on uuid_ref, it it exist
