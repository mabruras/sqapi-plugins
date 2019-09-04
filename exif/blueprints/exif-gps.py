#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_ALL_LOCATIONS = os.sep.join(['gps', 'select_all_locations.sql'])
SELECT_BY_GEOHASH = os.sep.join(['gps', 'select_by_geohash.sql'])

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/exif/gps')


@bp.route('/', methods=['GET'])
@cross_origin()
def get_all_locations():
    db = get_database()

    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0
    query_dict = {'limit': limit, 'offset': offset}

    log.info('Fetching all entries with GPS data'.format())
    script = get_script_path(SELECT_ALL_LOCATIONS)
    items = db.execute_script(script, **query_dict)

    if not items:
        log.info('No entries found')
        return responding.no_content(items)

    log.debug('Entries found: {}'.format(items))
    return responding.ok(items)


@bp.route('/geohash/<geohash>', methods=['GET'])
@cross_origin()
def get_gpsinfo_by_geohash(geohash):
    db = get_database()

    query_dict = {'geohash': geohash + '%'}

    log.info('Fetching GPS data by geohash: {}'.format(query_dict))
    script = get_script_path(SELECT_BY_GEOHASH)
    items = db.execute_script(script, **query_dict)

    if not items:
        log.info('No entry found with geohash: {}'.format(geohash))
        return responding.no_content(items)

    log.debug('Entries found with geohash={}: {}'.format(geohash, items))
    return responding.ok(items)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('exif')


def get_config():
    return current_app.config.get('exif')
