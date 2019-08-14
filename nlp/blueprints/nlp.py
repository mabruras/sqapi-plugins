#! /usr/bin/env python3
import logging
import os
import urllib

from flask import Blueprint, current_app
from flask_cors import cross_origin

from sqapi.api import responding

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/nlp')


@bp.route('/text/<text>', methods=['GET'])
@cross_origin()
def search_all_fields(text):
    text = urllib.parse.unquote(text)
    db = get_database()

    log.info('Fetching all nlp')
    result = db.fetch_document('nlp', {'query': text, 'fields': ['*']}, 'multi_match')

    if not result:
        log.info('No entries found')
        return responding.no_content(result)

    log.debug('Entries: {}'.format(result))
    return responding.ok([r.get('_source') for r in result])


@bp.route('/uuid/<uuid_ref>', methods=['GET'])
@cross_origin()
def get_all_nlp(uuid_ref):
    db = get_database()

    log.info('Fetching all nlp')
    result = db.fetch_document('nlp', {'uuid': uuid_ref}, 'match')

    if not result:
        log.info('No entries found')
        return responding.no_content(result)

    log.debug('Entries: {}'.format(result))
    return responding.ok([r.get('_source') for r in result])


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('nlp')


def get_config():
    return current_app.config.get('nlp')
