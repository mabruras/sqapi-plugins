import io
import logging
import os
import uuid

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    data_type = metadata.get('mime.type', message.type)

    log.info('Detected data type: {}'.format(data_type))
    save_to_db(database, message, data_type)


def save_to_db(database, message, data_type):
    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'datatype': data_type,
    }
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
