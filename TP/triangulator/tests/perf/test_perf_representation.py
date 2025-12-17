"""Performance tests for binary representation."""
import struct
import time
from random import randint

from main import PointSet, Triangles, Triangulator

fifty_points_pointset = PointSet(
    50,
    [
        [randint(-50, 50).__float__(), randint(-50, 50).__float__()]
        for _ in range(50)
    ],
)


def test_pointset_to_binary_three_points_pointset():
    """Test binary conversion performance for 3-point PointSet."""
    start = time.time()
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    binary = pointset.to_binary()
    end = time.time()
    print(end - start)
    assert binary is not None

def test_pointset_to_binary_fifty_points_pointset():
    """Test binary conversion performance for 50-point PointSet."""
    start = time.time()
    pointset = fifty_points_pointset
    binary = pointset.to_binary()
    end = time.time()
    print(end - start)
    assert binary is not None

def test_triangles_to_binary_three_points_pointset():
    """Test binary conversion performance for triangles with 3 points."""
    start = time.time()
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    triangles = Triangles(pointset, 1, [[0, 1, 2]])
    binary = triangles.to_binary()
    end = time.time()
    print(end - start)
    assert binary is not None

def test_triangles_to_binary_fifty_points_pointset():
    """Test binary conversion performance for triangles with 50 points."""
    start = time.time()
    triangles = Triangulator.triangulate(fifty_points_pointset)
    binaries = triangles.to_binary()
    end = time.time()
    print(end - start)
    assert triangles is not None
    assert binaries is not None

def test_pointset_from_binary_three_points_pointset():
    """Test deserialization performance for 3-point PointSet."""
    start = time.time()
    initial_binary = (struct.pack('<I', 3) +
                      struct.pack('<ff', 1.0, 2.0) +
                      struct.pack('<ff', 1.0, 6.0) +
                      struct.pack('<ff', 4.0, 4.0))
    pointset = PointSet.from_binary(initial_binary)
    end = time.time()
    print(end - start)
    assert pointset is not None

def test_pointset_from_binary_fifty_points_pointset():
    """Test deserialization performance for 50-point PointSet."""
    start = time.time()
    initial_binary = fifty_points_pointset.to_binary()
    pointset = PointSet.from_binary(initial_binary)
    end = time.time()
    print(end - start)
    assert pointset is not None

def test_triangles_from_binary_three_points_pointset():
    """Test deserialization performance for triangles with 3 points."""
    start = time.time()
    initial_binary = (struct.pack('<I', 3)
                      + struct.pack('<ff', 1.0, 2.0)
                      + struct.pack('<ff', 1.0, 6.0)
                      + struct.pack('<ff', 4.0, 4.0)
                      + struct.pack('<I', 1)
                      + struct.pack('<III', 0, 1, 2))
    triangles = Triangles.from_binary(initial_binary)
    end = time.time()
    print(end - start)
    assert triangles is not None