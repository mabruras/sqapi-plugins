SELECT
  id,
  video_reference,
  center_frame,
  sequence_start,
  sequence_stop,
  frame_spacing,
  center_frame_ts,
  resolution,
  created_at
FROM video_sequence
WHERE video_reference = %(video_reference)s
LIMIT %(limit)s
OFFSET %(offset)s
