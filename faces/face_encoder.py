import io
import logging
import threading

import face_recognition
from PIL import Image, ImageFile

log = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True


def find_face_encodings_with_location(file, config=None):
    degrees = config.custom.get('rotation', {}).get('degrees', 360) if config else 360
    number_of_rotations = 360 // (degrees or 360)
    out = []

    thread_pool = [
        threading.Thread(target=execute_face_detection, args=[
            open(file.name, 'rb'), x * degrees, out
        ], daemon=True) for x in range(number_of_rotations)
    ]

    log.info(f'{number_of_rotations} rotations of {degrees} degrees')

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
    encodings = find_face_encodings(file, degrees)
    log.info(f'Locating {len(encodings)} face encodings by {degrees} degrees rotation')
    out += encodings


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
            'low_vectors': encoding[0:64],
            'high_vectors': encoding[64:128],
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
    return [(enc.tolist(), loc) for (enc, loc) in zip(encodings, locations)]
