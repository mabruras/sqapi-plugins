#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin

from sqapi.api import responding

SELECT_ALL_DATA_TYPES = 'select_datatypes_count.sql'
SELECT_UUIDREFS_BY_DATA_TYPES = 'select_uuidrefs_by_datatypes.sql'
SELECT_UUIDREFS_BY_DATA_TYPES_ON_DATE = 'select_uuidrefs_by_dt_on_date.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/datatypes')

@bp.route('/', methods=['GET'])
@cross_origin()
def get_all_datatypes():
    db = get_database()

    log.info('Fetching all datatypes.')
    script = get_script_path(SELECT_ALL_DATA_TYPES)
    datatypes = db.execute_script(script)

    if not datatypes:
        log.info('No entries found.')
        return responding.no_content(datatypes)

    log.debug('Entries: {}'.format(datatypes))
    return responding.ok(datatypes)

@bp.route('/uuidrefs', methods=['GET'])
@cross_origin()
def get_all_refs():
    db = get_database()
    req_datatype = request.args.get('datatype')
    req_date = request.args.get('date')
    if not req_datatype:
        log.debug('No query parameter was passed to the method. Returning empty.')
        return responding.no_content([])

    entities = []

    if req_datatype and req_date:
        script = get_script_path(SELECT_UUIDREFS_BY_DATA_TYPES_ON_DATE)
        datatype = {'datatype': req_datatype, 'anydate': req_date }
        log.info('Fetching ref uuids for datatype, anydate: {}'.format(datatype))
        entities = db.execute_script(script, **datatype)

    else:
        script = get_script_path(SELECT_UUIDREFS_BY_DATA_TYPES)
        datatype = {'datatype': req_datatype }
        entities = db.execute_script(script, **datatype)
    
    if not entities:
        log.info('No entries found for datatype: {}'.format(datatype))
        return responding.no_content([])

    log.debug('Entity found: {}'.format(entities))
    return responding.ok(entities)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('datatypes')


def get_config():
    return current_app.config.get('datatypes')
