# EXIF

## Intention
This plugin stores the extracted EXIF data from each received image.


## Accepts
All image types


## Storage
### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.


## Usage
### Endpoints
* `/exif?limit=<limit>&offset=<offset>`: Returns all EXIF data registered
  * Both query params are optional and intended to be used with pagination
  * `limit`: [_Optional_], limit the amount of results (*Defaults to 10*)
  * `offset`: [_Optional_], start at a specific index (*Default to 0*)
* `/exif/uuid/<uuid>`: Returns all EXIF data registered with specific UUID
* `/exif/gps?limit=<limit>&offset=<offset>`: Returns all GPS data registered
  * Both query params are optional and intended to be used with pagination
  * `limit`: [_Optional_], limit the amount of results (*Defaults to 10*)
  * `offset`: [_Optional_], start at a specific index (*Default to 0*)
* `/exif/gps/geohash/<uuid>`: Returns all EXIF data registered with specific UUID
