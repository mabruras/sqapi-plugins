import io
import logging
import os
import uuid

from langdetect import detect

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_doc.sql'
MAX_BYTE_SIZE_TO_READ = 10000

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    lang = detect_language(config, metadata, data)
    log.info('Language detected: {}'.format(lang))

    save_to_db(database, message, lang)


def detect_language(config, metadata, data):
    log.debug('Detecting language of object')

    lang = None
    for name in config.custom.get('metadata_names'):
        lang = metadata.get(name, None)
        if lang:
            break

    if not lang:
        string_data = data.read(MAX_BYTE_SIZE_TO_READ).decode()
        lang = detect(string_data)

    return lang


def save_to_db(database, message, lang):
    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'lang': lang,
    }
    log.debug('Storing language in database')
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
