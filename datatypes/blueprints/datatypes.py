#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding

SELECT_ALL_DATA_TYPES = 'select_datatypes_count.sql'
SELECT_BY_UUID = 'select_by_uuid.sql'
SELECT_BY_DATA_TYPES = 'select_by_datatype.sql'
SELECT_BY_DATA_TYPES_ON_DATE = 'select_by_datatype_on_date.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/datatypes')


@bp.route('/', methods=['GET'])
@cross_origin()
def get_all_data_types():
    db = get_database()
    req_data_type = request.args.get('datatype')
    req_date = request.args.get('date')
    limit = request.args.get('limit') or 10
    offset = request.args.get('offset') or 0

    if not req_data_type:
        log.info('Fetching all data types')
        fields = {}
        script = get_script_path(SELECT_ALL_DATA_TYPES)

    elif req_data_type and req_date:
        log.info('Fetching by type ({}), limited by date ({})'.format(req_data_type, req_date))
        fields = {'datatype': req_data_type, 'anydate': req_date, 'limit': limit, 'offset': offset}
        script = get_script_path(SELECT_BY_DATA_TYPES_ON_DATE)

    else:
        log.info('Fetching by data type: {}'.format(req_data_type))
        fields = {'datatype': req_data_type, 'limit': limit, 'offset': offset}
        script = get_script_path(SELECT_BY_DATA_TYPES)

    entities = db.execute_script(script, **fields)
    if not entities:
        log.info('No entities found for data type: {}'.format(req_data_type))
        return responding.no_content(entities)

    log.debug('Entities found: {}'.format(entities))
    return responding.ok(entities)


@bp.route('/<uuid>', methods=['GET'])
@cross_origin()
def get_data_type_of_uuid(uuid):
    db = get_database()
    query_dict = {'uuid': uuid}

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
    return current_app.database.get('datatypes')


def get_config():
    return current_app.config.get('datatypes')
