INSERT INTO video_sequence (
  id,
  video_reference,
  center_frame,
  sequence_start,
  sequence_stop,
  frame_spacing,
  center_frame_ts,
  resolution,
  gif
) VALUES (
  %(id)s,
  %(video_reference)s,
  %(center_frame)s,
  %(sequence_start)s,
  %(sequence_stop)s,
  %(frame_spacing)s,
  %(center_frame_ts)s,
  %(resolution)s,
  %(gif)s
)
