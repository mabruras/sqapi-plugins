#! /usr/bin/env python3
import logging
import urllib

from flask import Blueprint, current_app, request
from flask_cors import cross_origin
from sqapi.api import responding

log = logging.getLogger(__name__)
bp = Blueprint(__name__, __name__, url_prefix='/text')


@bp.route('/search/<idx>', methods=['GET'])
@cross_origin()
def search_all_fields(idx):
    value = request.args.get('value')
    if not value:
        return responding.invalid_request('Missing search value parameter')

    text = urllib.parse.unquote(value)
    db = get_database()

    log.info('Searching for text: {}'.format(text))
    result = db.fetch_document(idx + '*', {'query': text, 'fields': ['*']}, 'multi_match', **dict(request.args))

    return filter_results(result)


@bp.route('/index/<idx>', methods=['GET'])
@cross_origin()
def get_all_by_params(idx):
    if not request.args:
        return responding.invalid_request('Missing parameters to query against')

    # Remove pagination variables from query params
    pagination_args = ['start', 'size']
    args = {k: request.args[k] for k in request.args.keys() if k not in pagination_args}

    log.info('Fetching all documents matching: {}'.format(args))
    query = {'must': [{'match': {b: request.args[b]}} for b in args]}
    result = get_database().fetch_document(idx + '*', query, 'bool', **dict(request.args))

    return filter_results(result)


def filter_results(result):
    log.debug('Entries: {}'.format(result))

    limited_fields = get_config().custom.get('limited_fields', [])
    log.debug('Filtering results to only contain: {}'.format(limited_fields))

    if limited_fields:
        for entry in result.get('hits'):
            entry['_source'] = {
                key: entry.get('_source')[key]
                for key in entry.get('_source')
                if key in limited_fields
            }

    log.info('Post filter: {}'.format(result))

    only_source = get_config().custom.get('filter_es_meta', False)
    if only_source:
        result['hits'] = [r.get('_source') for r in result.get('hits')]
        return responding.ok(result)

    return responding.ok(result)


def get_database():
    return current_app.database.get('text')


def get_config():
    return current_app.config.get('text')
