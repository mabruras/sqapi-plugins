import io
import json
import logging
import os
from datetime import datetime

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    meta_idx = config.custom.get('metadata_index')
    content_idx = config.custom.get('content_index')
    if not (meta_idx and content_idx):
        raise LookupError('Missing index definition, cannot save to storage')

    log.info('Indexing metadata')
    flatten = config.custom.get('flatten', {})
    delimiter = flatten.get('delimiter', '.')
    meta = flatten_dict(metadata, delimiter) if flatten else metadata

    log.info('Indexing text')
    content = parse_content(data.read().decode('utf-8'))

    storage_data = {meta_idx: dict(), content_idx: dict()}
    storage_data[meta_idx].update(meta)
    storage_data[content_idx].update(content)

    save_to_db(config, database, message, storage_data)


def parse_content(decode_values):
    try:
        # If content is parsable to JSON format, it should sort
        # all keys and values into two separate fields for indexing
        log.debug('Attempting to parse into JSON')
        loaded_json = json.loads(decode_values)
        log.debug('Loaded JSON: {}'.format(loaded_json))

        log.info('Successfully parsing content to JSON')
        parsed_json = get_all_json_keys_and_values(loaded_json)
        log.debug('Parsed JSON: {}'.format(parsed_json))
        content = {
            'keys': ' '.join([str(k) for k in parsed_json.get('keys')]),
            'content': ' '.join([str(k) for k in parsed_json.get('values')]),
        }
        log.info('Successfully extracting keys and values from JSON')

    except json.JSONDecodeError:
        log.warning('Could not parse JSON, expecting content to be text')
        content = {'content': decode_values}

    return content


def get_all_json_keys_and_values(loaded_json):
    keys = set()
    values = set()

    def extract_keys(item):
        if type(item) is dict:
            for key in item:
                keys.add(key)
                extract_keys(item[key])

        elif type(item) is list:
            for e in item:
                extract_keys(e)

        else:
            values.add(item)

    extract_keys(loaded_json)

    return {
        'keys': keys,
        'values': values
    }


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


def _get_index_suffix(config):
    suf = config.custom.get('index_suffix')

    if not suf:
        return ''
    elif suf.get('type') == 'date':
        return '_' + datetime.now().strftime(suf.get('value'))

    return suf.get('value', '')


def save_to_db(config, database, message, body):
    log.debug('Saving body: {}'.format(body))

    for idx in body.keys():
        log.debug('Saving for index ({}), body: {}'.format(idx, body.get(idx, {})))

        output = {
            **body.get(idx, {}),
            'uuid': message.uuid,
            'meta_location': message.meta_location,
            'data_location': message.data_location,
        }
        log.debug(output)

        index_suffix = _get_index_suffix(config)
        database.create_document(idx + index_suffix, output)
