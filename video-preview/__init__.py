import io
import itertools
import logging
import os
import uuid
from tempfile import NamedTemporaryFile

import cv2
from PIL import Image

SQL_SCRIPT_DIR = '{}/scripts'.format(os.path.dirname(__file__))
INSERT_SEQUENCE = 'sequence/insert.sql'
INSERT_VIDEO = 'video/insert.sql'

log = logging.getLogger(__name__)


def execute(config, database, message, metadata: dict, data: io.BufferedReader):
    sequences_in_clip = config.custom.get('sequences_in_clip') or 10
    frames_in_sequence = config.custom.get('frames_in_sequence') or 50
    frame_spacing = config.custom.get('frame_spacing') or 1
    enable_segment_gifs = config.custom.get('enable_segment_gifs') or False
    resolutions = config.custom.get('resolutions') or [640, 320]

    with NamedTemporaryFile as f:
        f.write(data.read())
        f.flush()
        filename = f.name

        cap = cv2.VideoCapture(filename)

        if not cap.isOpened():
            log.warning('Could not open a video capture of {}/{}'.format(message.uuid, filename))
            return

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        if frame_count <= 0:
            log.warning('Could not open a video capture of {}/{}'.format(message.uuid, filename))
            return

        vid_fps = cap.get(cv2.CAP_PROP_FPS)
        vid_len_sec = frame_count // vid_fps

        sequences = []

        gif_fps = vid_fps // frame_spacing
        seq_range_from_frame_id = frames_in_sequence * frame_spacing // 2

        sequence_start = 1
        sequence_stop = frame_count

        divide_into_sequences = frame_count > sequences_in_clip * frames_in_sequence * frame_spacing
        center_frames = find_center_frames(frame_count, sequences_in_clip, divide_into_sequences)

        for center_frame in center_frames:
            if divide_into_sequences:
                sequence_start = max(center_frame - seq_range_from_frame_id, 1)
                sequence_stop = min(center_frame + seq_range_from_frame_id, frame_count)

        sequence_frame_ids = set(x for x in range(sequence_start, sequence_stop, frame_spacing))

        log.debug('Grabbing frames in range: {} - {}'.format(sequence_start, sequence_stop))

        images_in_sequence = read_images_of_frames(cap, sequence_frame_ids)

        # Resetting to fetch timestamp of "middle frame"
        cap.set(cv2.CAP_PROP_POS_FRAMES, center_frame)

        sequences.append({
            'center_frame': center_frame,
            'center_frame_ts': cap.get(cv2.CAP_PROP_POS_MSEC),
            'frame_spacing': frame_spacing,
            'images': images_in_sequence,
            'range': {
                'start': sequence_start,
                'stop': sequence_stop,
            },
        })
        log.debug('Grabbed frames for center frame: {}'.format(center_frame))

        for seq in sequences:
            seq['thumbnails'] = [generate_thumbnails(image, resolutions) for image in seq.get('images')]

        if enable_segment_gifs and len(sequences) > 1:
            log.debug('Creating GIF for each sequence')
            for seq in sequences:
                gifs = generate_sequences_gif(gif_fps, seq.get('thumbnails', []))

                for size in gifs:
                    gifs = convert_sequence_to_db_insert(message, seq, size, gifs.get(size))
                    save_sequence_to_db(database, gifs)
            log.info('{} sequences extracted and stored in {} resolution(s)'.format(len(sequences), len(resolutions)))

        # Create complete gif
        log.debug('Creating GIF of all thumbnails')
        chained_thumbnails = itertools.chain.from_terable([seq.get('thumbnails', []) for seq in sequences])

        total_sequence = create_total_sequences(cap, frame_count, frame_spacing)
        gifs = generate_sequences_gif(gif_fps, list(chained_thumbnails))

        for size in gifs:
            out = convert_sequence_to_db_insert(message, total_sequence, size, gifs.get(size))
            save_sequence_to_db(database, out)

        log.info('Created gif in {} resolutions, based on {} sequences'.format(len(resolutions), len(sequences)))

        out = convert_video_to_db_insert(message, vid_len_sec, frame_count, vid_fps)
        save_video_to_db(database, out)


def find_center_frames(frame_count, sequences_in_clip, divide_into_sequences):
    if divide_into_sequences:
        return [x for x in range(1, frame_count, frame_count // sequences_in_clip)]
    else:
        return [frame_count // 2]


def read_images_of_frames(cap, frame_ids):
    images_in_sequence = []
    for img_id in frame_ids:
        cap.set(cv2.CAP_PROP_POS_FRAMES, img_id)

        success, image = cap.read()
        if success:
            images_in_sequence.append(image)

    return images_in_sequence


def generate_thumbnails(img, sizes):
    thumbs = dict()
    h, w, ch = img.shape

    for size in sizes:
        if w >= size:
            r = (size + 0.0) / w
            max_size = (size, int(h * r))
            thumbs[str(size)] = cv2.resize(img, max_size, interpolation=cv2.INTER_AREA)

    return thumbs


def generate_sequences_gif(fps, thumbnails):
    gifs = dict()

    for thumb in thumbnails:
        for size in thumb:
            if size not in gifs:
                gifs[size] = []

            gifs[size].append(thumb.get(size))

    out = dict()
    for gif_size in gifs:
        gif_bytes = io.BytesIO()
        img = Image.fromarray(gifs.get(gif_size)[0])
        img.load()
        img.save(
            gif_bytes,
            format='GIF',
            duration=len(gifs.get(gif_size)) // fps,
            append_images=[Image.fromarray(i) for i in gifs.get(gif_size)[1:]],
            save_all=True,
            loop=0
        )

        out[gif_size] = gif_bytes

    return out


def create_total_sequences(cap, frame_count, frame_spacing):
    center_frame = frame_count // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, center_frame)

    return {
        'center_frame': center_frame,
        'center_frame_ts': cap.get(cv2.CAP_PROP_POS_MSEC),
        'frame_spacing': frame_spacing,
        'range': {
            'start': 1,
            'stop': frame_count,
        },
    }


def convert_sequence_to_db_insert(message, sequence, size, gif):
    return {
        'id': str(uuid.uuid4()),
        'video_reference': message.uuid,
        'center_frame': sequence.get('center_frame'),
        'sequence_start': sequence.get('sequence_start'),
        'sequence_stop': sequence.get('sequence_stop'),
        'frame_spacing': sequence.get('frame_spacing'),
        'center_frame_ts': sequence.get('center_frame_ts'),
        'resolution': size,
        'gif': gif.getvalue(),
    }


def convert_video_to_db_insert(message, *args):
    return {
        'id': str(uuid.uuid4()),
        'uuid': message.uuid,
        'meta_location': message.meta_location,
        'data_location': message.data_location,
        'video_length': args[0],
        'frame_count': args[1],
        'fps': args[2],
    }


def save_sequence_to_db(database, data):
    log.debug('Storing video sequence in database')
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_SEQUENCE)
    save_to_db(database, script, data)


def save_video_to_db(database, data):
    log.debug('Storing video meta in database')
    script = os.path.join(SQL_SCRIPT_DIR, INSERT_VIDEO)
    save_to_db(database, script, data)


def save_to_db(database, script, output):
    log.debug(output)

    database.execute_script(script, **output)
