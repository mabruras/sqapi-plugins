import logging

log = logging.getLogger(__name__)


def get_lat_lon(gps_info):
    # Based on https://gist.github.com/valgur/2fbed04680864fab1bfc#file-get_exif_gps_info-py-L34
    lat = None
    lon = None

    def convert_to_degrees(value):
        try:
            d, m, s = value
            return d + (m / 60.0) + (s / 3600.0)
        except Exception as e:
            log.warning('Could not convert "{}" to degrees: {}'.format(value, str(e)))

    if gps_info:
        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get("GPSLatitudeRef")
        gps_longitude = gps_info.get("GPSLongitude")
        gps_longitude_ref = gps_info.get("GPSLongitudeRef")

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = convert_to_degrees(gps_latitude)
            if lat and gps_latitude_ref != "N":
                lat = -lat

            lon = convert_to_degrees(gps_longitude)
            if lon and gps_longitude_ref != "E":
                lon = -lon

    return lat, lon


def convert_raw_values_to_savable(input):
    return {
               key: convert_raw_value(input.get(key))
               for key in input.keys()
           } or {}


def convert_raw_value(value):
    # Based on : https://gist.github.com/valgur/2fbed04680864fab1bfc
    def is_fraction(val):
        return isinstance(val, tuple) and len(val) == 2 and all(isinstance(v, int) for v in val)

    def frac_to_dec(frac):
        return float(frac[0]) / float(frac[1])

    try:
        if is_fraction(value):
            return frac_to_dec(value)
        elif all(is_fraction(v) for v in value):
            return tuple(map(frac_to_dec, value))
        elif isinstance(value, bytes):
            return value.decode('utf-8').strip('\0')
    except Exception as e:
        log.debug('Failed convert value: {}'.format(str(e)))

    return str(value).strip('\0')
