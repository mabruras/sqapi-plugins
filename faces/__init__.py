import io
import json
import logging
import os
import uuid

from PIL import Image

from . import face_encoder

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'
SELECT_ALL_ENCODINGS = 'select_all_encodings.sql'
SELECT_BY_HASH = 'select_face_by_hash.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    already_processed = _find_existing(database, message.hash_digest)

    if already_processed:
        enc, uid, box = already_processed[0]
        o = convert_to_db_insert(message, {'encoding': enc, 'user_id': uid, 'box': box})
        save_to_db(database, o)

        return

    verify_image_size(config, data, message)

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

    log.info('{} face encodings stored in database'.format(len(faces)))


def _find_existing(db, hash_digest):
    script = os.path.join(SQL_SCRIPT_DIR, SELECT_BY_HASH)
    res = db.execute_script(script, **{'hash_digest': hash_digest})

    return [(f.get('encoding'), f.get('user_id'), f.get('box')) for f in res]


def verify_image_size(config, data, message):
    log.info('Verifying image size')
    im = Image.open(data)
    width, height = im.size
    min_height = config.custom.get('min_height', 100)
    min_width = config.custom.get('min_width', 100)

    if width < min_width or height < min_height:
        raise AttributeError('Size of image {} was not valid. Actual: {}, minimum values: {})'.format(
            message.uuid,
            (width, height),
            (min_height, min_width)
        ))


def convert_to_db_insert(message, face):
    return {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'hash_digest': message.hash_digest,
        'encoding': face.get('encoding', list()),
        'user_id': face.get('user_id', None),
        'box': json.dumps(face.get('box', dict())),
    }


def save_to_db(database, output):
    log.debug('Storing encoding in database')
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
