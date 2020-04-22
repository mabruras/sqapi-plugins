import io
import json
import logging
import os
import uuid

import pygeohash
from PIL import Image
from PIL.TiffImagePlugin import TiffImageFile

from . import extractor

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_ITEM = 'insert_item.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    img = Image.open(data)

    exif, gps = get_exif_data(img)
    log.info('Detected {} exif elements, and {} GPS details'.format(len(exif or {}), len(gps or {})))

    geohash = get_geohash(gps)
    log.debug('Geohash calculated: {}'.format(geohash))

    # Extract Date and time stamp to separate field? Example:
    # [*map(int, gps['GPSDateStamp'].split(':')), *map(int, [v for v, _ in gps['GPSTimeStamp']])]

    out = convert_to_db_insert(message, exif, gps, geohash)
    save_to_db(database, out)


def get_exif_data(img):
    log.info('Extracting EXIF and GPS dat from image')
    exif_extractor = extractor.tiff_exif if isinstance(img, TiffImageFile) else extractor.jpeg_exif
    exif, gps = exif_extractor(img)

    if not exif:
        raise ReferenceError('Could not find any exif in image')

    return exif, gps


def get_geohash(gps):
    if not gps:
        log.debug('Cannot calculate Geohash when no GPS-data exists')
        return None

    log.info('Calculating Geohash')
    extractor.add_decimal_lat_lon(gps)

    lat = gps.get('GPSLatitudeDec', None)
    lon = gps.get('GPSLongitudeDec', None)

    return pygeohash.encode(lat, lon) if lat and lon else None


def convert_to_db_insert(message, exif, gps, geohash):
    return {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'geohash': geohash or None,
        'exif': json.dumps(exif) if exif else None,
        'gps': json.dumps(gps) if gps else None,
    }


def save_to_db(database, output):
    log.debug('Storing sizes in database')
    log.debug(output)

    script = os.path.join(SQL_SCRIPT_DIR, INSERT_ITEM)
    database.execute_script(script, **output)
