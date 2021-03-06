#! /usr/bin/env python3
import io
import logging
import os

from flask import Blueprint, current_app, request, send_file
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_ALL = 'sequence/select_all.sql'
SELECT_BY_VID_REF = 'sequence/select_by_video_reference.sql'
SELECT_BY_ID = 'sequence/select_by_id.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/video-sequence')


@bp.route('/<vid_ref>', methods=['GET'])
@cross_origin()
def get_sequences_by_video_reference(vid_ref):
    db = get_database()
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    query = {'video_reference': vid_ref, 'limit': limit, 'offset': offset}
    log.info('Fetching all entries by query args: {}'.format(query))

    script = get_script_path(SELECT_BY_VID_REF)
    results = db.execute_script(script, **query)

    if not results:
        log.info('No entries found with value: {}'.format(query))
        return responding.no_content(results)

    log.debug('Entries with {}: {}'.format(query, results))
    return responding.ok(results)


@bp.route('/gif/<seq_id>', methods=['GET'])
@cross_origin()
def get_sequence_by_id(seq_id):
    db = get_database()
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    query = {'id': seq_id, 'limit': limit, 'offset': offset}
    log.info('Fetching binary data by query args: {}'.format(query))

    script = get_script_path(SELECT_BY_ID)
    results = db.execute_script(script, **query)

    if not results:
        log.info('No entries found with value: {}'.format(query))
        return responding.no_content(results)

    log.debug('Sequence id={}'.format(seq_id))

    return send_file(
        io.BytesIO(results[0].get('gif', b'')),
        attachment_filename=seq_id
    )


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('video-preview')


def get_config():
    return current_app.config.get('video-preview')
