import time
from random import randint

fifty_points_pointset = PointSet(50, [[randint(-50, 50).__float__(), randint(-50, 50).__float__()] for _ in range(50)])

def test_triangulate_three_points_pointset():
    start = time.time()
    pointset = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])

    triangles = Triangulator.triangulate(pointset)
    end = time.time()
    print(end - start)
    assert triangles == Triangles(pointset, 1, [[0,1,2]])

def test_triangulate_fifty_points_pointset():
    start = time.time()
    triangles = Triangulator.triangulate(fifty_points_pointset)
    end = time.time()
    print(end - start)
    assert triangles is not None