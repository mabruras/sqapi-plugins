#! /usr/bin/env python3
import logging
import os

from flask import Blueprint, current_app
from flask_cors import cross_origin

from sqapi.api import responding

SELECT_DOC_BY_LANG = 'select_doc_by_lang.sql'
SELECT_DOC_BY_UUID = 'select_doc_by_uuidref.sql'

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/languages')


@bp.route('/<lang>', methods=['GET'])
@cross_origin()
def get_docs_by_lang(lang):
    db = get_database()
    lang_dict = {'lang': lang}

    log.info('Fetching all entries with lang: {}'.format(lang))
    script = get_script_path(SELECT_DOC_BY_LANG)
    docs = db.execute_script(script, **lang_dict)

    if not docs:
        log.info('No entries found with lang: {}'.format(lang))
        return responding.no_content(docs)

    log.debug('Entries with lang: {}, {}'.format(lang, docs))
    return responding.ok(docs)


@bp.route('/uuid/<uuid_ref>', methods=['GET'])
@cross_origin()
def get_doc_for_uuid(uuid_ref):
    db = get_database()
    uuid_dict = {'uuid_ref': uuid_ref}

    log.info('Fetching entry with uuid: {}'.format(uuid_ref))
    script = get_script_path(SELECT_DOC_BY_UUID)
    entities = db.execute_script(script, **uuid_dict)

    if not entities:
        log.info('No entries found with uuid: {}'.format(uuid_ref))
        return responding.no_content(entities)

    log.debug('Entity found: {}'.format(entities))
    return responding.ok(entities)


def get_script_path(name):
    plugin_dir = get_config().plugin.get('directory')

    return os.path.join(plugin_dir, 'scripts', name)


def get_database():
    return current_app.database.get('languages')


def get_config():
    return current_app.config.get('languages')
