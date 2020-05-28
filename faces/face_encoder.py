import io
import logging
import threading
import uuid

import face_recognition
import numpy
from PIL import Image

log = logging.getLogger(__name__)


def find_face_encodings_with_location(file, config=None):
    degrees = config.custom.get('rotation', {}).get('degrees', 360) if config else 360
    number_of_rotations = 360 // (degrees or 360)
    out = []

    thread_pool = [
        threading.Thread(target=execute_face_detection, args=[
            open(file.name, 'rb'), x * degrees, out
        ]) for x in range(number_of_rotations)
    ]

    log.info('{} rotations of {} degrees'.format(number_of_rotations, degrees))

    log.debug('Starting thread pool')
    [t.start() for t in thread_pool]
    log.debug('Collecting threads')
    [t.join() for t in thread_pool]
    log.debug('Threads collected')

    return out


def execute_face_detection(file, degrees, out):
    if degrees and degrees < 360:
        log.debug('Rotating image {} degrees (total rotation:'.format(degrees))
        file = rotate_image(file, degrees)
    log.info('Locating face encodings in image, by {} degrees rotation'.format(degrees))
    out += find_face_encodings(file, degrees)


def rotate_image(file, degrees):
    bio = io.BytesIO()
    img = Image.open(file)
    rotated = img.rotate(degrees)
    rotated.save(bio, img.format)

    return bio


def find_face_encodings(file, degrees=0):
    img = face_recognition.load_image_file(file)
    log.debug('Image loaded')

    encs_locs = find_encodings_with_locations(img)
    log.debug(encs_locs)

    results = [
        dict({
            'encoding': encoding.tolist(),
            'degrees': degrees,
            'box': {
                'y': y1,
                'x': x1,
                'w': x2 - x1,
                'h': y2 - y1,
            },
        })
        for encoding, (y1, x2, y2, x1) in encs_locs
    ]

    log.debug(results)

    return results


def find_encodings_with_locations(img):
    log.debug('Extracting face locations')
    locations = face_recognition.face_locations(img)
    if not locations:
        log.debug('No face locations detected')
        return []

    log.debug('Extracting face encodings')
    encodings = face_recognition.face_encodings(img, known_face_locations=locations)

    log.debug('Zipping encodings with their respective location')
    return [(enc, loc) for (enc, loc) in zip(encodings, locations)]


def compare_face_with_existing(config, face, existing_faces):
    log.debug('face: {}'.format(face))
    log.debug('existing_faces: {}'.format(existing_faces))

    distance_encodings = (dict({
        'distance': face_recognition.face_distance(numpy.array([f.get('encoding')]), face.get('encoding')),
        'face': f
    }) for f in existing_faces)

    default_profile = dict({'user_id': str(uuid.uuid4())})
    closest_profile = dict(default_profile)
    closest_distance = 1

    log.debug('Comparing distances between new and existing encodings')
    for de in distance_encodings:
        log.debug('Comparing current distance ({}) against closest distance ({})'.format(
            de.get('distance'), closest_distance)
        )
        log.debug(de)
        if de.get('distance') < closest_distance:
            closest_distance = de.get('distance')
            closest_profile = de.get('face')

    log.debug('Comparison complete. Closest profile={}, distance={}'.format(closest_profile, closest_distance))
    comparison_threshold = config.custom.get('tolerance', 0.45)

    return (closest_profile, closest_distance) if closest_distance < comparison_threshold else (default_profile, 1)
