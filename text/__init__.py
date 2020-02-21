import io
import json
import logging
import os
from datetime import datetime

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    idx_suffix = get_suffix(config)

    meta_idx = config.custom.get('metadata_index')
    content_idx = config.custom.get('content_index')

    flatten = config.custom.get('flatten', {})
    delimiter = flatten.get('delimiter', '.')
    meta = flatten_dict(metadata, delimiter) if flatten else metadata

    log.info('Indexing metadata')
    save_to_db(database, message, meta_idx, idx_suffix, **meta)

    log.info('Indexing text')
    decode_values = data.read().decode('utf-8')

    try:
        # If content is parsable to JSON format,
        # it should be flatten and indexed directly
        log.debug('Attempting to parse into JSON')
        loaded_json = json.loads(decode_values)

        log.info('Successfully parsing content to JSON')
        content = flatten_dict(loaded_json, delimiter)

    except json.JSONDecodeError:
        log.info('Storing content as text')
        content = {'text': decode_values}

    save_to_db(database, message, content_idx, idx_suffix, **content)


def get_suffix(config):
    suf = config.custom.get('index_suffix')

    if not suf:
        return ''
    elif suf.get('type') == 'date':
        return '_' + datetime.now().strftime(suf.get('value'))

    return suf.get('value', '')


def flatten_dict(in_dict: dict, delimiter: chr = '.') -> dict:
    """
    Function borrowed from: https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10

    :param in_dict: input dictionary to flatten
    :param delimiter: character to separate joined values
    :return: flatten dictionary
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + delimiter)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + delimiter)
                i += 1
        else:
            out[name[:-1]] = x

    flatten(in_dict)

    return out


def save_to_db(database, message, idx, idx_suffix='', **body):
    if not idx:
        log.warning('Missing index definition, cannot save to storage')
        return

    output = {
        **body,
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
    }
    log.debug(output)

    database.create_document(idx + idx_suffix, output)
