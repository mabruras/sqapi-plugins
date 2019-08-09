#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding


log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/nlp')


@bp.route('/', methods=['GET'])
@cross_origin()
def get_all_nlp():
    db = get_database()

    log.info('Fetching all nlp')
    script = get_script_path('SELECT * FROM nlp;')
    result = db.execute_script(script)

    if not result:
        log.info('No entries found')
        return responding.no_content(result)

    log.debug('Entries: {}'.format(result))
    return responding.ok(result)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('nlp')


def get_config():
    return current_app.config.get('nlp')
