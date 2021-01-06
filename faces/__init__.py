import io
import json
import logging
import os
import uuid

from PIL import Image, ImageFile

from . import face_encoder

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))

INSERT_IMAGE_ITEM = 'face/insert.sql'
SELECT_BY_HASH = 'face/select_by_hash.sql'

INSERT_ENCODING_ITEM = 'encoding/insert.sql'
SELECT_CLOSEST_MATCH = 'encoding/select_closest_match.sql'

log = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    if is_image_too_small(config, data, message):
        log.info('Image height/width to small')
        return

    if not _find_existing(database, message.hash_digest):
        try:
            extract_face_encodings(config, database, message, data)

        except AttributeError as e:
            log.debug(str(e))
            return

    save_image_to_db(database, {
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'hash_digest': message.hash_digest,
    })


def is_image_too_small(config, data, message):
    min_height = config.custom.get('min_height', 100)
    min_width = config.custom.get('min_width', 100)
    log.info('Checking image size towards threshold ({}x{})'.format(min_width, min_height))

    im = Image.open(data)
    width, height = im.size

    return width < min_width or height < min_height


def _find_existing(db, hash_digest):
    script = os.path.join(SQL_SCRIPT_DIR, SELECT_BY_HASH)
    res = db.execute_script(script, **{'hash_digest': hash_digest})

    return [(f.get('encoding'), f.get('user_id'), f.get('degrees'), f.get('box')) for f in res]


def extract_face_encodings(config, database, message, data):
    faces = face_encoder.find_face_encodings_with_location(data, config)

    if not faces:
        raise AttributeError('No faces found in picture')

    log.info(f'Total of {len(faces)} face encodings found')
    comparison_threshold = config.custom.get('tolerance', 0.45)

    for encoding in faces:
        log.debug('Comparing detected face encodings towards existing')
        script = os.path.join(SQL_SCRIPT_DIR, SELECT_CLOSEST_MATCH)
        closest_match = database.execute_script(script, **{
            'low_vectors': encoding.get('low_vectors'),
            'high_vectors': encoding.get('high_vectors'),
            'threshold': comparison_threshold,
        })

        encoding.update({'user_id': closest_match[0].get('user_id') if closest_match else str(uuid.uuid4())})

        out = convert_to_db_insert(message, encoding)
        save_encodings_to_db(database, out)


def convert_to_db_insert(message, face):
    return {
        'degrees': face.get('degrees', 0),
        'hash_digest': message.hash_digest,
        'box': json.dumps(face.get('box', dict())),
        'low_vectors': face.get('low_vectors', list()),
        'high_vectors': face.get('high_vectors', list()),
        'user_id': face.get('user_id', None),
    }


def save_encodings_to_db(database, output):
    log.debug('Storing encoding in database')
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ENCODING_ITEM)
    database.execute_script(script, **output)


def save_image_to_db(database, output):
    log.debug('Storing image reference in database')
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_IMAGE_ITEM)
    database.execute_script(script, **output)
