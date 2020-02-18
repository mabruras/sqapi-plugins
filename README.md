# sqAPI Plugins

_Are you actually looking for the
[sqAPI Core Repository](https://github.com/mabruras/sqapi)?_

## About
Collection repository for custom business logic of
[sqAPI](https://github.com/mabruras/sqapi).
All different sqAPI logic elements are to be imported as plugins.
This README defines how to develop new plugins,
what is required and recommended when developing plugins for sqAPI.

When using the plugins, they are to be imported into:
`sqapi/plugin/plugins`, within the sqAPI project root directory.
This means that when using with Docker, the plugins can be mounted by
`-v sqapi-plugins:/opt/mab/sqapi/plugin/plugins`

## Requirements
There are some technical requirements for a plugin to be able to load into sqAPI.

### Structure
The folder structure of a plugin is as follows:
```bash
./sqapi/plugin/plugins/        # Parent Plugins collection directory
└── plugin_name                # Plugin directory
    ├── blueprints             # Directory for keeping blueprints
    │   ├── endpoints.py       # Blueprints for specific endpoints
    │   └── __init__.py        #
    ├── config.yml             # Plugin Specific configuration - overwrites sqAPI configuration
    ├── __init__.py            # Execution definition : See more below "Business logic"
    ├── scripts                # Normal directory for keeping SQL scripts
    │   └── insert_item.sql    # Specific SQL script to use in
    └── README.md              # Description of the plugin
```

#### Blueprints
Blueprints are python modules containing a set of endpoints,
where logic for fetching the plugins custom data set gets implemented.

Within the blueprints directory,
each API resource should exist in separate modules.

Eg.:
* `./blueprints/images.py` - (Serves all `/images/*` endpoints)
* `./blueprints/thumbnails.py` - (Serves all `/thumbnails/*` endpoints)

Each of the blueprints will be automatically picked up,
and referenced to by a `bp`-variable.
sqAPI will not register the blueprint if the variable name is incorrect.

This means that every blueprint module must include the `bp`-variable, preferably like follows.

_Example with `./blueprints/thumbnails.py`_:
```python
from flask import Blueprint
bp = Blueprint(__name__, __name__, url_prefix='/thumbnails')
```

##### Extra
Within the blueprints, there will be some extra objects available as default.
These objects are made available in each blueprint when starting up sqAPI.

###### Config
To get access to the configuration object for the plugin,
just call for `flask.current_app.config.get('plugin_name')`.

_Example with `./plugins/image_plugin`_:
```python
from flask import current_app
cfg = current_app.config['image_plugin']
```

###### Database
The database object is used equally as with the sqAPI loader,
by calling for `flask.current_app.database.get('plugin_name')`.

_Example with `./plugins/image_plugin`_:
```python
from flask import current_app
db = current_app.database['image_plugin']
```


#### Config file
The configuration file: `config.yml`, this name is not changeable.

The plugin-specific configuration is used to override default configuration from
[sqAPI-config](https://github.com/mabruras/sqapi/blob/master/src/sqapi/resources/sqapi.yml).

The configuration can be extended with what ever fields
you want to use within the business logic (both `execute` and blueprints).
If a field already exists in the default configuration,
it will be overwritten for each of the plugins overriding it.

Typical usage, will be for defining database connection,
as well as supported mime types.


#### Business Logic
All business logic is defined within the `__init__.py`, for the specific plugin.
When a plugin is triggered, sqAPI looks for a definition of `execute`.
If the `execute` function is not available, it will not import the module.

Within the `execute` function, you configure, structure and store the data in any way you want.

##### Minimum setup
The only required setup, is that the following method is defined, within `__init__.py`.

```python
def execute(config, database, message: Message, metadata: dict, data: bytes):
    pass
```

##### Example usage
This example tests each of the input arguments.

```python
def execute(config, database, message: Message, metadata: dict, data: bytes):

    # Config
    log.debug('My configuration: {}'.format(config))

    # Database
    log.debug('Database ready for usage: {}'.format(database.active_connection()))

    # Message body
    for k,v in message.body.items():
        log.debug('{} = {}'.format(k,v))

    # Metadata
    log.info('Metadata: {}'.format(metadata))

    # Data
    filesize = data.seek(0, 2)
    log.info('File size: {}'.format(filesize))
```

##### Arguments
###### Config
This is the complete configuration for this plugin,
as mentioned within the [Configuration](#configuration).

Note that the configuration elements are based upon custom configuration,
and can contain what ever you put into it.

###### Database
The database object is selected based up on what is defined in the plugins specifications.

Each type of database should always be available for the following methods:
```python
# Should read out query (or similar) from file, and replace variables based on kwargs
def execute_script(self, script_path: str, **kwargs): pass

# Should replace variables in query, based on the kwargs
def execute_query(self, query: str, **kwargs): pass

# Returnes True or False, based on the database being able to handle connections
def active_connection(self): pass

# Runs the configured initialization script/logic, to prepare the database
def initialize_database(self): pass
```

The execution is based on a script and a set of kwargs.
The script or query is intended to execute your custom logic for storing a custom data set,
while the kwargs should replace placeholder variables within the script/query.

This depends on the database module implementation,
and what kind of system is running as database.

###### Message
This is the received message from the message system, represented as a
[sqAPI Message](https://github.com/mabruras/sqapi/blob/master/src/sqapi/messaging/message.py).
It will have a `body` with a dictionary containing set of key/value pairs,
that you could use if you see it necessary.

Typical usage is to refer to the identification of the data received (`message.uuid`).

The message also includes a hash digest (`message.hash_digest`) and mime type (`message.type`).
Make sure to note that the `message.type` can explicitly be defined within the message up front of sqAPI.
This means that the mime type will only be guessed by sqAPI if it is not already defined.
If there is not a type defined in the message up front,
and sqAPI is not able to guess, it will default to `application/octet-stream`.

###### Metadata
Metadata fetched from the `metadata store`,
or the `message` object, as dictionary.
The key/value pairs within this object is dependent on your backend system,
and storage solution.

###### Data
Data object fetched from the `data store`, in a file like object.
Access to this data object will in most cases be through the use of a file handler,
and will typical have default IO methods available.

#### Database Scripts
The database scripts is a directory for setup and interaction with the database.
Put all .sql scripts (example for postgres) within this directory,
and refer to them through the `execute`-function.

##### Initialize Database
To initialize the database, there should be a database script defined.
The database script should be referred to in the configuration like follows:
```yaml
database:
  init: 'scripts/init.sql'
```

Note that the path is relative to the plugin directory,
as the full project path in this example is
`./sqapi/plugin/plugins/my_plugin/scripts/init.sql`.

By defining the script, sqAPI will automatically have
the database initialized upon constructing the database object.

##### Insert Custom Data
This example shows how one can insert custom data in the database.
Note that you would still have to initialize the database.

###### SQL Script
```sql
INSERT INTO items (
  uuid_ref,
  mime_type
) VALUES (
  %(uuid_ref)s,
  %(mime_type)s
)
```

###### Execute
```python
import os

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))


def execute(config, database, message: Message, metadata: dict, data: bytes):
    insert_script = 'insert_item.sql'

    output = {
        'uuid_ref': message.uuid,
        'mime_type': message.type,
    }

    script = os.path.join(SQL_SCRIPT_DIR, insert_script)
    database.execute_script(script, **output)
```

#### README.md
Information about this specific plugin.
This will be exposed through one of the default sqAPI endpoints,
so please make the README understandable and nicely formatted.


### Configuration
sqAPI has its own configuration, defined at the system level.
This should always be overwritten for each plugin,
so we always ensure custom logic for each usage.
For more about the configuration, read the
[Configuration document](https://github.com/mabruras/sqapi/blob/master/resources/docs/CONFIGURATION.md).

##### Example usage
When accessing a topic of configuration, you will call it directly on the Config object.
Each topic is a dictionary, created from the yaml configuration file, added to the Config object.

```python
def execute(config, database, message: Message, metadata: dict, data: bytes):
    # Access a topic
    meta_store = config.meta_store  # Returns a dictionary of meta_store, defined in the configuration file
    
    # Safely access a field within the topic
    meta_store_host = meta_store.get('host', 'localhost')  # Defaults to localhost if not found in configuration
```
