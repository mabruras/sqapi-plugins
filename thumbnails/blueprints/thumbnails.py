#! /usr/bin/env python3
import io
import logging
import os

from flask import Blueprint, current_app, send_file
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_THUMB_BY_UUID = 'select_thumb_by_uuid.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/thumbnails')


@bp.route('/<uuid>', methods=['GET'])
@cross_origin()
def thumbnail_by_uuid(uuid):
    db = get_database()
    uuid_dict = {'uuid': uuid}

    log.info('Fetching thumbnail for uuid: {}'.format(uuid))
    script = get_script_path(SELECT_THUMB_BY_UUID)
    thumbnails = db.execute_script(script, **uuid_dict)
    log.debug('Thumbnails found: {}'.format(thumbnails))

    if not thumbnails:
        err = 'No thumbnail found with UUID: {}'.format(uuid)
        log.warning(err)
        return responding.no_content(err)

    log.debug('Thumbnail uuid: {}'.format(uuid))

    return send_file(
        io.BytesIO(thumbnails[0].get('thumbnail', b'')),
        attachment_filename=uuid
    )


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('thumbnails')


def get_config():
    return current_app.config.get('thumbnails')
