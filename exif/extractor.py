import logging

from PIL import ExifTags, TiffTags

from . import converter

log = logging.getLogger(__name__)


def tiff_exif(img):
    log.debug('Image of type TIFF')
    exif = img.tag
    tags = TiffTags.TAGS

    exif = named_keys_exif(exif, tags)
    gps = extract_gps(exif)

    return converter.convert_raw_values_to_savable(exif), converter.convert_raw_values_to_savable(gps)


def jpeg_exif(img):
    log.debug('Image of type JPEG or PNG')
    exif = img._getexif() or {}
    tags = ExifTags.TAGS

    exif = named_keys_exif(exif, tags)
    gps = extract_gps(exif)

    return converter.convert_raw_values_to_savable(exif), converter.convert_raw_values_to_savable(gps)


def named_keys_exif(exif, tags):
    return {
        tags.get(key, key): exif.get(key)
        for key in exif.keys()
    }


def extract_gps(exif):
    gps_info = exif.get('GPSInfo', {})

    gps = {
        ExifTags.GPSTAGS.get(key, key): gps_info.get(key)
        for key in gps_info
    }

    return gps


def add_decimal_lat_lon(gps):
    lat, lon = converter.get_lat_lon(gps)

    if lat and lon:
        gps.update({
            'GPSLatitudeDec': lat,
            'GPSLongitudeDec': lon,
        })
