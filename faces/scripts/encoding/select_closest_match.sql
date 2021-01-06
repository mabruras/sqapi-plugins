SELECT user_id FROM face_encodings
WHERE sqrt(
  power(CUBE(%(low_vectors)s) <-> low_vectors, 2)
  + power(CUBE(%(high_vectors)s) <-> high_vectors, 2)
) <= %(threshold)s
ORDER BY sqrt(
  power(CUBE(%(low_vectors)s) <-> low_vectors, 2)
  + power(CUBE(%(high_vectors)s) <-> high_vectors, 2)
) DESC
LIMIT 1
