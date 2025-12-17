"""Performance tests for triangulation."""
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


def test_triangulate_three_points_pointset():
    """Test triangulation performance for 3 points."""
    start = time.time()
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])

    triangles = Triangulator.triangulate(pointset)
    end = time.time()
    print(end - start)
    assert triangles.n_triangles == 1
    assert len(triangles.triangles) == 1
    assert set(triangles.triangles[0]) == {0, 1, 2}

def test_triangulate_fifty_points_pointset():
    """Test triangulation performance for 50 points."""
    start = time.time()
    triangles = Triangulator.triangulate(fifty_points_pointset)
    end = time.time()
    print(end - start)
    assert triangles is not None