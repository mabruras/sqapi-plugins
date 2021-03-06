# Video Preview

## Intention
Creates thumbnail preview GIFs of videos

## Accepts
* `video/ogg`
* `video/avi`
* `video/x-msvideo`
* `video/mp4`
* `video/mpeg`
* `video/quicktime`
* `video/x-flv`



## Storage
### Disk
N/A

### Data Structure
Read the [init.sql](scripts/init.sql) to see the stored data structure.

## Usage
### Endpoints
* `/video-previews?offset=<offset>&limit=<limit>`: Returns all previews of videos registered
* `/video-previews/<preview_id>?offset=<offset>&limit=<limit>`: Returns all previews created for a specific UUID
* `/video-sequences/<vid_ref>?offset=<offset>&limit=<limit>`: Returns all sequences stored for a specific video
* `/video-sequences/gif/<sequence_id>`: Returns binary gif for specific video sequence

### Pagination
Both query params are optional and intended to be used with pagination,
and goes for all endpoints except the endpoint for downloading the binary file.
* `offset`: [_Optional_], Limit the amount of results (*Defaults to 10*)
* `limit`: [_Optional_], Start at a specific index (*Default to 0*)
