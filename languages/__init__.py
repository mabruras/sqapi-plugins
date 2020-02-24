import io
import logging
import os
import uuid

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_doc.sql'
MAX_BYTE_SIZE_TO_READ = 10000

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    try:
        lang = detect_language(config, metadata, data)
        save_to_db(database, message, lang)
    except LangDetectException:
        log.info("Could not detect language")


def detect_language(config, metadata, data):
    log.info('Detecting language of object')
    metadata_names = config.custom.get('metadata_names')

    lang = None
    for name in metadata_names:
        lang = metadata.get(name, None)
        if lang:
            break

    if not lang:
        string_data = data.read(MAX_BYTE_SIZE_TO_READ).decode()
        lang = detect(string_data)

    log.info('Language detected: {}'.format(lang))
    return lang


def save_to_db(database, message, lang):
    log.info('Storing language in database')
    # This defines the kwargs that are sent in as parameters to the SQL script
    output = {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'lang': lang,
    }
    log.debug(output)

    # Resolve path to the script intended to run, to insert your data structure into the database
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)

    database.execute_script(script, **output)
