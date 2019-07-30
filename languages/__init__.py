import io
import logging
import os

from langdetect import detect

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_doc.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    lang = detect_language(metadata, data)

    save_to_db(database, message, lang)


def detect_language(metadata, data):
    log.info('Detecting language of object')
    lang = metadata.get('lang', None) or metadata.get('language', None)

    if not lang:
        lang = detect(data.read().decode())

    log.info('Language detected: {}'.format(lang))
    return lang


def save_to_db(database, message, lang):
    log.info('Storing language in database')
    # This defines the kwargs that are sent in as parameters to the SQL script
    output = {
        'uuid_ref': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'lang': lang,
    }
    log.debug(output)

    # Resolve path to the script intended to run, to insert your data structure into the database
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)

    database.execute_script(script, **output)
