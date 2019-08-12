import io
import logging
import os
import threading

import spacy

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    data = data.read()
    process_pool = [
        threading.Thread(
            target=nlp_processing,
            args=[lang, data.decode('utf-8'), database, message]
        )
        for lang in (config.packages.get('spacy') or {}).get('download') or []
    ]

    log.info('Starting NLP processing')
    [t.start() for t in process_pool]
    [t.join() for t in process_pool]


def nlp_processing(language, data, db, msg):
    log.debug('NER processing')
    nlp = spacy.load(language)
    doc = nlp(data)

    ner = [{
        'uuid': msg.uuid,
        'text': ent.text,
        'start': ent.start_char,
        'end': ent.end_char,
        'label': ent.label_,
        'nlp_lang_pack': language,
    } for ent in doc.ents]

    for n in ner:
        save_to_db(db, msg, n)


def save_to_db(database, message, body):
    log.debug('Storing nlp processed text in database')

    output = {
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        **body,
    }
    log.debug(output)

    database.create_document('nlp', output)
