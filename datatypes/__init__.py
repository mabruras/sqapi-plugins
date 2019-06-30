import io
import logging
import os

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'

log = logging.getLogger(__name__)


def execute(config, database, message: dict, metadata: dict, data: io.BufferedReader):
    save_to_db(database, message, metadata)


def save_to_db(database, message, metadata):
    log.info('Storing datatype reference in database')
    # This defines the kwargs that are sent in as parameters to the SQL script
    output = {
        'uuid_ref': message.get('uuid_ref', None),
        'meta_location': message.get('meta_location', None),
        'data_location': message.get('data_location', None),
        'datatype': metadata.get('mime.type', None),
    }
    log.debug(output)

    # Resolve path to the script intended to run, to insert your data structure into the database
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)

    database.execute_script(script, **output)
