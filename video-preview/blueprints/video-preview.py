#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_ALL = 'video/select_all.sql'
SELECT_BY_UUID = 'video/select_by_uuid.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/video-previews')


@bp.route('/', methods=['GET'])
@cross_origin()
def get_all_video_previews():
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    return get_database_entries({'limit': limit, 'offset': offset}, SELECT_ALL)


@bp.route('/<preview_id>', methods=['GET'])
@cross_origin()
def get_video_previews_by_uuid(preview_id):
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    return get_database_entries({'uuid': preview_id, 'limit': limit, 'offset': offset}, SELECT_BY_UUID)


def get_database_entries(query, script_path):
    log.info('Fetching all entries by query args: {}'.format(query))
    db = get_database()

    script = get_script_path(script_path)
    results = db.execute_script(script, **query)

    if not results:
        log.info('No entries found with value: {}'.format(query))
        return responding.no_content(results)

    log.debug('Entries with {}: {}'.format(query, results))
    return responding.ok(results)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('video-preview')


def get_config():
    return current_app.config.get('video-preview')
