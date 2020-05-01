import hashlib
import io
import logging
import os
import uuid

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_hash.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    hashes = calculate_hashes(config, data)
    log.info('Hash digests calculated')
    log.debug('Hashes: {}'.format(hashes))

    save_to_db(database, message, **hashes)


def calculate_hashes(config, data):
    chunk_size = config.custom.get('chunk_size', 1024)

    data.seek(0, 0)
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    for chunk in _chunk_file_read(data, chunk_size):
        md5.update(chunk)
        sha1.update(chunk)
        sha256.update(chunk)

    return dict({
        'md5': md5.hexdigest(),
        'sha1': sha1.hexdigest(),
        'sha256': sha256.hexdigest(),
    })


def _chunk_file_read(data, chunk_size=1024):
    while True:
        next_chunk = data.read(chunk_size)

        if not next_chunk:
            break

        yield next_chunk


def save_to_db(database, message, **kwargs):
    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        **kwargs,
    }
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
