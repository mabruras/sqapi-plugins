# Language detection

## Intention
This plugin uses pip package to detect language of plain/text files

## Accepts
plain/text

## Storage
### Disk
N/A

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.

## Usage
### Endpoints
* `/languages/<language>`: Returns all uuid references with the same language
* `/languages/uuid/<uuid_ref>`: Returns the language of a specific uuid reference
