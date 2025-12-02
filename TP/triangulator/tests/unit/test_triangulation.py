from unittest.mock import patch
from TP.triangulator.main import app

@patch("PointSetManager.retrieve")
@patch("Triangulator.triangulate")
def test_triangulate_empty_pointset(mock_retrieve, mock_triangulate):
    mock_retrieve.return_value = PointSet(0, [])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 0, [])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 0, [])

@patch("PointSetManager.retrieve")
@patch("Triangulator.triangulate")
def test_triangulate_two_points_pointset(mock_retrieve, mock_triangulate):
    mock_retrieve.return_value = PointSet(2, [[1.0, 2.0], [1.0, 6.0]])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 0, [])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 0, [])

@patch("PointSetManager.retrieve")
@patch("Triangulator.triangulate")
def test_triangulate_three_points_pointset(mock_retrieve, mock_triangulate):
    mock_retrieve.return_value = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 1, [[0,1,2]])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 1, [[0,1,2]])

@patch("PointSetManager.retrieve")
@patch("Triangulator.triangulate")
def test_triangulate_invalid_pointset(mock_retrieve, mock_triangulate):
    client = app.test_client()
    mock_retrieve.return_value = PointSet(-1, [[1.0, 2.0], ['b', 6.0], [4.0, 'a']])
    mock_triangulate.return_value = None

    pointset = client.get("/pointset/123e4567-e89b-12d3-a456-426614174000")

    assert pointset.status_code == 400

@patch("PointSetManager.retrieve")
@patch("Triangulator.triangulate")
def test_triangulate_collinear_points(mock_retrieve, mock_triangulate):
    mock_retrieve.return_value = PointSet(3, [[1.0, 2.0], [1.0,6.0], [1.0,8.0]])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 1, [[0,1,2]])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 1, [[0,1,2]])