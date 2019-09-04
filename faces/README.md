# Faces

## Intention
This plugin stores the face encodings extracted from the data payload.


## Accepts
Image types; `image/jpeg`, `image/png`, `image/gif`


## Storage
### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.


## Usage
### Endpoints
* `/faces/profile/<user_id>`: Returns occurrences of the user_id in different images
* `/faces/profile/sample?limit=<limit>&offset=<offset>`: Returns unique users with a sample image
  * Both query params are optional and intended to be used with pagination
  * `limit`: [_Optional_], limit the amount of results (*Defaults to 10*)
  * `offset`: [_Optional_], start at a specific index (*Default to 0*)
* `/faces/similar/<uuid>`: Returns other occurrences of all detected faces in an image
* `/faces/uuid/<uuid>`: Returns faces detected in an image
