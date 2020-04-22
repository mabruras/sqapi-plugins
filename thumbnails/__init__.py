import io
import logging
import os
import uuid

from PIL import Image

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'
SELECT_BY_HASH = 'select_thumb_by_hash.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    log.info('Searching for existing items of same hash')
    existing = _find_existing(database, message.hash_digest)

    thumbnail_data = existing or create_thumbnail(config, data)

    save_to_db(database, message, thumbnail_data)


def _find_existing(db, hash_digest):
    script = os.path.join(SQL_SCRIPT_DIR, SELECT_BY_HASH)
    res = db.execute_script(script, **{'hash_digest': hash_digest})

    return res[0].get('thumbnail') if res else res


def create_thumbnail(config, data):
    width = config.custom.get('thumb_size', {}).get('width', 128)
    height = config.custom.get('thumb_size', {}).get('height', 128)
    log.info('Creating thumbnail with width/height: {}/{}'.format(width, height))

    try:
        im = Image.open(data)
        im.thumbnail((width, height))

        output = io.BytesIO()
        im.save(output, im.format)

        return output.getvalue()

    except IOError as e:
        err = 'Cannot create thumbnail for {}: {}'.format(data, str(e))
        log.warning(err)
        raise IOError(err, e)


def save_to_db(database, message, thumbnail_data):
    log.debug('Storing thumbnail in database')

    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'hash_digest': message.hash_digest,
        'thumbnail': thumbnail_data,
    }
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
