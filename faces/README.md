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
* `/faces/similar/<uuid>`: Returns other occurrences of all detected faces in an image
* `/faces/uuid/<uuid>`: Returns faces detected in an image
