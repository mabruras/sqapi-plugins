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
    result = db.fetch_document(idx + '*', {'query': text, 'fields': ['*']}, 'multi_match')

    if not result:
        log.info('No entries found')
        return responding.no_content(result)

    log.debug('Entries: {}'.format(result))
    return filter_results(result)


@bp.route('/index/<idx>', methods=['GET'])
@cross_origin()
def get_all_by_params(idx):
    if not request.args:
        return responding.invalid_request('Missing uuid parameter')

    db = get_database()

    log.info('Fetching all documents matching: {}'.format(request.args))
    query = {'must': [{'match': {b: request.args[b]}} for b in request.args]}
    result = db.fetch_document(idx + '*', query, 'bool')

    if not result:
        log.info('No entries found')
        return responding.no_content(result)

    log.debug('Entries: {}'.format(result))
    return filter_results(result)


def filter_results(result):
    only_source = get_config().custom.get('filter_es_meta', True)

    if only_source:
        return responding.ok([r.get('_source') for r in result])

    return responding.ok(result)


def get_database():
    return current_app.database.get('text')


def get_config():
    return current_app.config.get('text')
