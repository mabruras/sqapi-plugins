#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_HASH_BY_MD5 = 'select_hash_by_md5.sql'
SELECT_HASH_BY_SHA1 = 'select_hash_by_sha1.sql'
SELECT_HASH_BY_SHA256 = 'select_hash_by_sha256.sql'
SELECT_HASH_BY_UUID = 'select_hash_by_uuid.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/hashes')


@bp.route('/md5/<md5>', methods=['GET'])
@cross_origin()
def get_hashes_by_md5(md5):
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    return get_database_entries({'md5': md5, 'limit': limit, 'offset': offset}, SELECT_HASH_BY_MD5)


@bp.route('/sha1/<sha1>', methods=['GET'])
@cross_origin()
def get_hashes_by_sha1(sha1):
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    return get_database_entries({'sha1': sha1, 'limit': limit, 'offset': offset}, SELECT_HASH_BY_SHA1)


@bp.route('/sha256/<sha256>', methods=['GET'])
@cross_origin()
def get_hashes_by_sha256(sha256):
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    return get_database_entries({'sha256': sha256, 'limit': limit, 'offset': offset}, SELECT_HASH_BY_SHA256)


@bp.route('/uuid/<uuid>', methods=['GET'])
@cross_origin()
def get_hash_for_uuid(uuid):
    return get_database_entries({'uuid': uuid}, SELECT_HASH_BY_UUID)


def get_database_entries(query, script_path):
    log.info('Fetching all entries with value: {}'.format(query))
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
    return current_app.database.get('hashes')


def get_config():
    return current_app.config.get('hashes')
