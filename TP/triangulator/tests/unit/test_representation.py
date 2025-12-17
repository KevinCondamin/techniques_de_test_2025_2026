"""Tests for binary representation of points and triangles."""
import struct
from unittest.mock import patch

from main import PointSet, Triangles


def test_triangle_to_binary_error():
    """Test binary conversion error for invalid triangles."""
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    triangle = Triangles(pointset, 1, [[1,3,5]])

    assert triangle.to_binary() is None

def test_triangles_to_binary_complete():
    """Test binary conversion for valid triangles."""
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
    """Test binary conversion for PointSet."""
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    binary = pointset.to_binary()

    expected = (struct.pack('<I', 3) +
                struct.pack('<ff', 1.0, 2.0) +
                struct.pack('<ff', 1.0, 6.0) +
                struct.pack('<ff', 4.0, 4.0))
    assert binary == expected

def test_pointset_to_binary_error():
    """Test binary conversion error for invalid PointSet."""
    pointset = PointSet(-1, [[1.0, 2.0], ['b', 6.0], [4.0, 'a']])

    assert pointset.to_binary() is None

def test_triangles_from_binary_error():
    """Test deserialization error for invalid binary data."""
    binary_data = b'invalid binary data'

    assert Triangles.from_binary(binary_data) is None

def test_triangles_from_binary_complete():
    """Test deserialization of triangles from binary."""
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
    """Test deserialization error for invalid binary data."""
    binary_data = b'invalid binary data'

    assert PointSet.from_binary(binary_data) is None

def test_pointset_from_binary_complete():
    """Test deserialization of PointSet from binary."""
    binary_data = (struct.pack('<I', 3) +
                   struct.pack('<ff', 1.0, 2.0) +
                   struct.pack('<ff', 1.0, 6.0) +
                   struct.pack('<ff', 4.0, 4.0))

    expected = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])

    pointset = PointSet.from_binary(binary_data)

    assert pointset == expected
    assert pointset.num_points == 3
    assert pointset.points == [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]]

def test_pointset_to_binary_negative_points():
    """Cover lines 37-38: n_points < 0"""
    ps = PointSet(-1, [])
    assert ps.to_binary() is None

def test_pointset_from_binary_exception():
    """Cover line 71: Exception during unpack"""
    assert PointSet.from_binary(b'short') is None

def test_triangles_to_binary_invalid_index():
    """Cover line 100: Index out of bounds"""
    ps = PointSet(3, [[0,0], [1,0], [0,1]])
    t = Triangles(ps, 1, [[0, 1, 3]]) # 3 is invalid
    assert t.to_binary() is None

def test_triangles_to_binary_exception():
    """Cover lines 114-115: Exception during pack"""
    ps = PointSet(3, [[0,0], [1,0], [0,1]])
    t = Triangles(ps, 1, [[0, 1, 2]])
    with patch('struct.pack', side_effect=Exception("Pack error")):
        assert t.to_binary() is None

def test_triangles_from_binary_invalid_pointset():
    """Cover lines 147-148: PointSet deserialization fails"""
    # Data too short for PointSet
    assert Triangles.from_binary(b'short') is None

def test_triangles_from_binary_success():
    """Ensure line 153 is reached and covered"""
    ps = PointSet(3, [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    t = Triangles(ps, 1, [[0, 1, 2]])
    binary = t.to_binary()
    t2 = Triangles.from_binary(binary)
    assert t2 is not None
    assert t2.n_triangles == 1