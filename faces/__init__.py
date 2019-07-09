import io
import json
import logging
import os
import uuid

from PIL import Image

from . import face_encoder

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'
SELECT_ALL_ENCODINGS = 'select_all_faces.sql'

log = logging.getLogger(__name__)


def execute(config, database, message: dict, metadata: dict, data: io.BufferedReader):
    log.info('Verifying image size')

    im = Image.open(data)
    width, height = im.size
    min_height = config.custom.get('min_height', 100)
    min_width = config.custom.get('min_width', 100)

    if width < min_width or height < min_height:
        log.warning('Size of image "{}" was not valid. Actual: {}, minimum values: {})'.format(
            message.get('uuid_ref', None),
            (width, height),
            (min_height, min_width)
        ))
        return

    log.info('Finding face encodings in image files')
    faces = face_encoder.find_face_encodings_with_location(data)
    log.info('{} faces found in image'.format(len(faces)))

    script = os.path.join(SQL_SCRIPT_DIR, SELECT_ALL_ENCODINGS)
    existing = database.execute_script(script)

    for face in faces:
        profile, dist = face_encoder.compare_face_with_existing(face, existing)
        log.debug('Closest profile found (dist={}): {}'.format(dist, profile))

        face.update({'user_id': profile.get('user_id')})

        log.debug('Converting face encoding to database insert: {}'.format(face))
        out = convert_to_db_insert(message, face)
        save_to_db(database, out)


def convert_to_db_insert(message, face):
    return {
        'id': str(uuid.uuid4()),
        'uuid_ref': message.get('uuid_ref', None),
        'meta_location': message.get('meta_location', None),
        'data_location': message.get('data_location', None),
        'encoding': face.get('encoding', list()),
        'user_id': face.get('user_id', None),
        'box': json.dumps(face.get('box', dict())),
    }


def save_to_db(database, output):
    log.info('Storing encoding in database')
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
