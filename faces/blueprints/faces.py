#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_ALL_FACES = 'select_all_faces.sql'
SELECT_FACES_BY_IMG_UUID = 'select_faces_by_img_uuid.sql'
SELECT_FACES_BY_USER_ID = 'select_faces_by_user_id.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/faces')


@bp.route('/profile/<user_id>', methods=['GET'])
@cross_origin()
def find_images_of_user(user_id):
    db = get_database()
    log.info('Finding images of user by user_id: {}'.format(user_id))
    user_dict = {'user_id': user_id}
    script = get_script_path(SELECT_FACES_BY_USER_ID)
    faces = db.execute_script(script, **user_dict)

    if not faces:
        err = 'Could not find any face encodings related to user_id: {}'.format(user_id)
        log.info(err)
        return responding.invalid_request(err)

    return responding.ok(faces)


@bp.route('/similar/<uuid_ref>', methods=['GET'])
@cross_origin()
def find_similar_images(uuid_ref):
    db = get_database()
    log.info('Started looking for similar encodings')
    uuid_dict = {'uuid_ref': uuid_ref}
    script = get_script_path(SELECT_FACES_BY_IMG_UUID)
    faces = db.execute_script(script, **uuid_dict)

    if not faces:
        err = 'Could not find any face encodings related to UUID: {}'.format(uuid_ref)
        log.info(err)
        return responding.invalid_request(err)

    script = get_script_path(SELECT_FACES_BY_USER_ID)
    res = [
        {
            **face,
            'similar': db.execute_script(
                script,
                **{'user_id': face.get('user_id')}
            )
        } for face in faces
    ]

    return responding.ok(res)


@bp.route('/uuid/<uuid_ref>', methods=['GET'])
@cross_origin()
def get_faces_with_img_uuid(uuid_ref):
    db = get_database()
    uuid_dict = {'uuid_ref': uuid_ref}

    log.info('Fetching entry with uuid: {}'.format(uuid_ref))
    script = get_script_path(SELECT_FACES_BY_IMG_UUID)
    entities = db.execute_script(script, **uuid_dict)

    if not entities:
        log.info('No entries found with uuid: {}'.format(uuid_ref))
        return responding.no_content(entities)

    log.debug('Entity found: {}'.format(entities))
    return responding.ok(entities)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('faces')


def get_config():
    return current_app.config.get('faces')
