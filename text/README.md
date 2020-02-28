# Text

## Intention
This plugin stores metadata fields, and the size of the data payload.


## Accepts
* text/plain
* text/richtext
* application/json


## Storage
The storage solution is using Elasticsearch for indexing
both metadata and content of plain text files.

### Data Structure
#### Metadata
The metadata could be flattened by configuration,
or it will be saved as a structured JSON.

#### Content
Content will be read as bytes, and decoded as `UTF-8`
before it is stored in a `text`-field along with the
`uuid`, `meta_location`, and `data_location`.

## Usage
Note that `&start=0&size=10` can be added
as query params for each of the endpoint.

### Endpoints
`/text/search/<idx>?value=<value>`: Searches all fields in an index, by value
`/text/index/<idx>?<key>=<uuid>`: Fetch elements by uuid

## Configuration
The following configurations are available

| Field | Type | Description | Example Value |
| ----- | ---- | ----------- | ------------- |
| `metadata_index` | `String` | Index for storing metadata (can match `content_index`) | `metadata` |
| `content_index` | `String` | Index for storing content (can match `metadata_index`) | `content` |
| `filter_es_meta` | `Boolean` | Filters *out* metadata provided by ES, for each hit | `true` |
| `limited_fields` | `Array` | Limits the result from ES, by filtering out fields not in this array | `[ "uuid", "data_location" ]` |
| `flatten` | `Dictionary` | Wrapper dictionary | - |
| `flatten.delimiter` | `String` | Delimiter between keys used when metadata dictionary is flattened | `.` |
| `index_suffix` | `Dictionary` | Wrapper dictionary | - |
| `index_suffix.type` | `String` | Used for suffixing each index, supporting `date` now. Making it possible to create indices per day | `date` |
| `index_suffix.value` | `String` | Format of suffix, hard coupled with `type` | `%Y-%m-%d` |
