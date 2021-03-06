INSERT INTO video_preview (
  id,
  uuid,
  meta_location,
  data_location,
  video_length,
  frame_count,
  fps
) VALUES (
  %(id)s,
  %(uuid)s,
  %(meta_location)s,
  %(data_location)s,
  %(video_length)s,
  %(frame_count)s,
  %(fps)s
)
