import io
import logging
import os

from PIL import Image

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    thumbnail_data = create_thumbnail(config, data)

    save_to_db(database, message, thumbnail_data)


def create_thumbnail(config, data):
    width = config.custom.get('thumb_size', {}).get('width', 128)
    height = config.custom.get('thumb_size', {}).get('height', 128)
    log.debug('Creating thumbnail with width/height: {}/{}'.format(width, height))

    try:
        im = Image.open(data)
        im.thumbnail((width, height))

        output = io.BytesIO()
        im.save(output, im.format)

        return output.getvalue()
    except IOError as e:
        err = 'Cannot create thumbnail for {}: {}'.format(data, str(e))
        log.warning(err)
        raise Exception(err)


def save_to_db(database, message, thumbnail_data):
    log.info('Storing thumbnail reference in database')

    output = {
        'uuid_ref': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'thumbnail': thumbnail_data,
    }
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)

    database.execute_script(script, **output)
