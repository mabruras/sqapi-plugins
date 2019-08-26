import hashlib
import io
import logging
import os
import uuid

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_dup.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    sha_256 = calculate_sha256(metadata, data)

    save_to_db(database, message, sha_256)


def calculate_sha256(metadata, data):
    log.info('Calculating SHA-256 of object')
    sha_256 = metadata.get('sha256', None) or metadata.get('sha-256', None) or metadata.get('sha_256', None)

    if not sha_256:
        sha_256 = hashlib.sha256(data.read()).hexdigest()

    log.debug('Hash calculated: {}'.format(sha_256))
    return sha_256


def save_to_db(database, message, sha_256):
    log.info('Storing hash in database')
    # This defines the kwargs that are sent in as parameters to the SQL script
    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'sha_256': sha_256,
    }
    log.debug(output)

    # Resolve path to the script intended to run, to insert your data structure into the database
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)

    database.execute_script(script, **output)
