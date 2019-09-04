#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_ALL = os.sep.join(['exif', 'select_all.sql'])
SELECT_BY_UUID = os.sep.join(['exif', 'select_by_uuid.sql'])

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/exif')


@bp.route('/', methods=['GET'])
@cross_origin()
def get_all_exif():
    db = get_database()

    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0
    query_dict = {'limit': limit, 'offset': offset}

    log.info('Fetching all entries'.format())
    script = get_script_path(SELECT_ALL)
    items = db.execute_script(script, **query_dict)

    if not items:
        log.info('No entries found')
        return responding.no_content(items)

    log.debug('Entries found: {}'.format(items))
    return responding.ok(items)


@bp.route('/uuid/<uuid>', methods=['GET'])
@cross_origin()
def get_exif_by_uuid(uuid):
    db = get_database()

    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0
    query_dict = {'limit': limit, 'offset': offset, 'uuid': uuid}

    log.info('Fetching entry with uuid: {}'.format(uuid))
    script = get_script_path(SELECT_BY_UUID)
    items = db.execute_script(script, **query_dict)

    if not items:
        log.info('No entry found with uuid: {}'.format(uuid))
        return responding.no_content(items)

    log.debug('Entry with uuid: {}, {}'.format(uuid, items))
    return responding.ok(items)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('exif')


def get_config():
    return current_app.config.get('exif')
