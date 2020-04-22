import logging
import uuid

import face_recognition
import numpy

log = logging.getLogger(__name__)


def find_face_encodings_with_location(file):
    img = face_recognition.load_image_file(file)
    log.debug('Image loaded')

    encs_locs = find_encodings_with_locations(img)
    log.debug(encs_locs)

    results = [
        dict({
            'encoding': encoding.tolist(),
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
