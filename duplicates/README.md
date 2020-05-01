# Duplicates

## DEPRECATED
Deprecated because of [hashes-plugin](../hashes/README.md).
It contains the same information, just extended with more values,
as well as endpoints.

This plugin will not be removed,
since it may be extended/modified to solve other related issues,
eg.: duplicate check on `uuid` or other fields.


## Intention
This plugin uses a sha256 hash to map against objects `uuid`.
The sha256 is reused from the message `hash_digest` field.


## Accepts
All types


## Storage
### Disk
N/A

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.


## Usage
### Endpoints
* `/duplicates/sha/<sha_256>`: Returns all uuid references with the same sha256
* `/duplicates/uuid/<uuid>`: Returns the sha_256 of a specific uuid reference
