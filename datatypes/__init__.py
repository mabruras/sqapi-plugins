import io
import logging
import os
import uuid

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    save_to_db(database, message, metadata)


def save_to_db(database, message, metadata):
    log.info('Storing datatype reference in database')
    # This defines the kwargs that are sent in as parameters to the SQL script
    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'datatype': metadata.get('mime.type', message.type),
    }
    log.debug(output)

    # Resolve path to the script intended to run, to insert your data structure into the database
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)

    database.execute_script(script, **output)
