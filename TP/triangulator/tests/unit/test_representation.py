import struct

def test_triangle_to_binary_error():
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    triangle = Triangles(pointset, 1, [[1,3,5]])

    assert triangle.to_binary() is None

def test_triangles_to_binary_complete():
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    triangles = Triangles(pointset, 1, [[0, 1, 2]])  # indices 0-based
    binary = triangles.to_binary()

    # Partie PointSet (28 bytes) + partie Triangles (16 bytes)
    expected = (struct.pack('<I', 3) +
                struct.pack('<ff', 1.0, 2.0) +
                struct.pack('<ff', 1.0, 6.0) +
                struct.pack('<ff', 4.0, 4.0) +
                struct.pack('<I', 1) +  # nb triangles
                struct.pack('<III', 0, 1, 2))  # indices du triangle
    assert binary == expected

def test_pointset_to_binary_complete():
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    binary = pointset.to_binary()

    expected = (struct.pack('<I', 3) +
                struct.pack('<ff', 1.0, 2.0) +
                struct.pack('<ff', 1.0, 6.0) +
                struct.pack('<ff', 4.0, 4.0))
    assert binary == expected

def test_pointset_to_binary_error():
    pointset = PointSet(-1, [[1.0, 2.0], ['b', 6.0], [4.0, 'a']])

    assert pointset.to_binary() is None

def test_triangles_from_binary_error():
    binary_data = b'invalid binary data'

    assert Triangles.from_binary(binary_data) is None

def test_triangles_from_binary_complete():
    binary_data = (struct.pack('<I', 3) +
                   struct.pack('<ff', 1.0, 2.0) +
                   struct.pack('<ff', 1.0, 6.0) +
                   struct.pack('<ff', 4.0, 4.0) +
                   struct.pack('<I', 1) +
                   struct.pack('<III', 0, 1, 2))

    triangles = Triangles.from_binary(binary_data)

    assert triangles.pointset.n_points == 3
    assert triangles.n_triangles == 1
    assert triangles.triangles == [[0, 1, 2]]

def test_pointset_from_binary_error():
    binary_data = b'invalid binary data'

    assert PointSet.from_binary(binary_data) is None

def test_pointset_from_binary_complete():
    binary_data = (struct.pack('<I', 3) +
                   struct.pack('<ff', 1.0, 2.0) +
                   struct.pack('<ff', 1.0, 6.0) +
                   struct.pack('<ff', 4.0, 4.0))

    expected = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])

    pointset = PointSet.from_binary(binary_data)

    assert pointset == expected
    assert pointset.num_points == 3
    assert pointset.points == [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]]

