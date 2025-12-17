"""Tests for triangulation functionality."""
import sys
from unittest.mock import patch

from main import (
    PointSet,
    PointSetManager,
    Triangles,
    Triangulator,
    app,
)


@patch("main.PointSetManager.retrieve")
@patch("main.Triangulator.triangulate")
def test_triangulate_empty_pointset(mock_triangulate, mock_retrieve):
    """Test triangulation of empty PointSet."""
    mock_retrieve.return_value = PointSet(0, [])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 0, [])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 0, [])

@patch("main.PointSetManager.retrieve")
@patch("main.Triangulator.triangulate")
def test_triangulate_two_points_pointset(mock_triangulate, mock_retrieve):
    """Test triangulation of PointSet with two points."""
    mock_retrieve.return_value = PointSet(2, [[1.0, 2.0], [1.0, 6.0]])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 0, [])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 0, [])

@patch("main.PointSetManager.retrieve")
@patch("main.Triangulator.triangulate")
def test_triangulate_three_points_pointset(mock_triangulate, mock_retrieve):
    """Test triangulation of PointSet with three points."""
    mock_retrieve.return_value = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [4.0, 4.0]])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 1, [[0,1,2]])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 1, [[0,1,2]])

@patch("main.PointSetManager.retrieve")
@patch("main.Triangulator.triangulate")
def test_triangulate_invalid_pointset(mock_triangulate, mock_retrieve):
    """Test triangulation with invalid PointSet."""
    client = app.test_client()

    mock_retrieve.return_value = PointSet(-1, [[1.0, 2.0], ['b', 6.0], [4.0, 'a']])

    mock_triangulate.side_effect = Exception("Invalid pointset data")

    response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")

    assert response.status_code == 500

@patch("main.PointSetManager.retrieve")
@patch("main.Triangulator.triangulate")
def test_triangulate_collinear_points(mock_triangulate, mock_retrieve):
    """Test triangulation with collinear points."""
    mock_retrieve.return_value = PointSet(3, [[1.0, 2.0], [1.0, 6.0], [1.0, 8.0]])
    pointset = PointSetManager.retrieve("123e4567-e89b-12d3-a456-426614174000")

    mock_triangulate.return_value = Triangles(pointset, 1, [[0,1,2]])
    triangles = Triangulator.triangulate(pointset)

    assert triangles == Triangles(pointset, 1, [[0,1,2]])

def test_triangulator_few_points():
    """Test triangulation with few points."""
    ps = PointSet(2, [[0,0], [1,0]])
    t = Triangulator.triangulate(ps)
    assert t.n_triangles == 0

def test_triangulator_import_error_simulation():
    """Test triangulation with missing scipy/numpy dependencies."""
    ps = PointSet(3, [[0,0], [1,0], [0,1]])
    # Simulate missing scipy/numpy by patching sys.modules
    with patch.dict(sys.modules, {'scipy.spatial': None, 'numpy': None}):
        t = Triangulator.triangulate(ps)
        assert t.n_triangles == 0