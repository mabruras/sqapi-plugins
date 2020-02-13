# Text

## Intention
This plugin stores metadata fields, and the size of the data payload.


## Accepts
* text/plain
* text/richtext


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
### Endpoints
`/text/search/<idx>?value=<value>`: Searches all fields in an index, by value
`/text/index/<idx>?uuid=<uuid>`: Fetch elements by uuid
