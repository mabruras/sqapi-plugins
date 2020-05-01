# Hashes

## Intention
This plugin uses different hash algorithms to map against objects uuid_ref.

The following algorithms are used:
* MD5
* SHA1
* SHA256


## Accepts
All types


## Storage
### Disk
N/A

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.

## Usage
### Endpoints
* `/hashes/md5/<md5>?offset=<offset>&limit=<limit>`: Returns all uuid references with the same md5
  * `offset`: [_Optional_], Limit the amount of results (*Defaults to 10*)
  * `limit`: [_Optional_], Start at a specific index (*Default to 0*)
* `/hashes/sha1/<sha1>?offset=<offset>&limit=<limit>`: Returns all uuid references with the same sha1
  * `offset`: [_Optional_], Limit the amount of results (*Defaults to 10*)
  * `limit`: [_Optional_], Start at a specific index (*Default to 0*)
* `/hashes/sha256/<sha256>?offset=<offset>&limit=<limit>`: Returns all uuid references with the same sha256
  * `offset`: [_Optional_], Limit the amount of results (*Defaults to 10*)
  * `limit`: [_Optional_], Start at a specific index (*Default to 0*)
* `/hashes/uuid/<uuid>`: Returns the hashes of a specific uuid reference
