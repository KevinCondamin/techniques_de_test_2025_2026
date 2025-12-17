"""Tests for the PointSetManager API client."""
import struct
import unittest
from unittest.mock import patch, MagicMock

from main import PointSetManager, PointSet, app


class PointSetManagerAPIClient:
    """Client for interacting with PointSetManager API."""

    def __init__(self, base_url="http://localhost"):
        """Initialize API client.

        Args:
            base_url: Base URL for the API.

        """
        self.base_url = base_url

    def create_pointset(self, binary_data):
        """POST /pointset - Create a new PointSet.

        Args:
            binary_data: Binary data for the PointSet.

        """
        pass

    def retrieve_pointset(self, pointset_id):
        """GET /pointset/{pointSetId} - Retrieve PointSet.

        Args:
            pointset_id: ID of the PointSet to retrieve.

        """
        pass


class TestAPI(unittest.TestCase):
    """Tests for PointSetManager API endpoints."""

    # Tests POST /pointset - createPointSet

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch.object(PointSetManagerAPIClient, 'create_pointset')
    def test_create_pointset_success(self, mock_create):
        """Test successful PointSet creation (201)."""
        expected_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_create.return_value = {"pointSetId": expected_id, "status_code": 201}

        binary_data = (struct.pack('<I', 3) +
                       struct.pack('<ff', 1.0, 2.0) +
                       struct.pack('<ff', 1.0, 6.0) +
                       struct.pack('<ff', 4.0, 4.0))

        client = PointSetManagerAPIClient()
        response = client.create_pointset(binary_data)

        assert response["status_code"] == 201
        assert response["pointSetId"] == expected_id
        mock_create.assert_called_once_with(binary_data)


    @patch.object(PointSetManagerAPIClient, 'create_pointset')
    def test_create_pointset_invalid_binary(self, mock_create):
        """Test creation with invalid binary format (400)."""
        mock_create.return_value = {
            "status_code": 400,
            "code": "INVALID_FORMAT",
            "message": "Bad request, e.g., invalid binary format."
        }

        client = PointSetManagerAPIClient()
        response = client.create_pointset(b'invalid')

        assert response["status_code"] == 400
        assert response["code"] == "INVALID_FORMAT"


    @patch.object(PointSetManagerAPIClient, 'create_pointset')
    def test_create_pointset_database_unavailable(self, mock_create):
        """Test creation when database unavailable (503)."""
        mock_create.return_value = {
            "status_code": 503,
            "code": "SERVICE_UNAVAILABLE",
            "message": "The PointSet storage layer (database) is unavailable."
        }

        binary_data = (struct.pack('<I', 3) +
                       struct.pack('<ff', 1.0, 2.0) +
                       struct.pack('<ff', 1.0, 6.0) +
                       struct.pack('<ff', 4.0, 4.0))

        client = PointSetManagerAPIClient()
        response = client.create_pointset(binary_data)

        assert response["status_code"] == 503
        assert response["code"] == "SERVICE_UNAVAILABLE"


    # Tests GET /pointset/{pointSetId} - getPointSetById

    @patch.object(PointSetManagerAPIClient, 'retrieve_pointset')
    def test_retrieve_pointset_success(self, mock_retrieve):
        """Test successful PointSet retrieval (200)."""
        pointset_id = "123e4567-e89b-12d3-a456-426614174000"
        binary_data = (struct.pack('<I', 3) +
                       struct.pack('<ff', 1.0, 2.0) +
                       struct.pack('<ff', 1.0, 6.0) +
                       struct.pack('<ff', 4.0, 4.0))

        mock_retrieve.return_value = {"status_code": 200, "data": binary_data}

        client = PointSetManagerAPIClient()
        response = client.retrieve_pointset(pointset_id)

        assert response["status_code"] == 200
        assert response["data"] == binary_data
        mock_retrieve.assert_called_once_with(pointset_id)


    @patch.object(PointSetManagerAPIClient, 'retrieve_pointset')
    def test_retrieve_pointset_not_found(self, mock_retrieve):
        """Test retrieval of nonexistent PointSet (404)."""
        pointset_id = "999e9999-e99b-99d9-a999-999999999999"
        mock_retrieve.return_value = {
            "status_code": 404,
            "code": "NOT_FOUND",
            "message": "A PointSet with the specified ID was not found."
        }

        client = PointSetManagerAPIClient()
        response = client.retrieve_pointset(pointset_id)

        assert response["status_code"] == 404
        assert response["code"] == "NOT_FOUND"


    @patch.object(PointSetManagerAPIClient, 'retrieve_pointset')
    def test_retrieve_pointset_invalid_id_format(self, mock_retrieve):
        """Test retrieval with invalid ID format (400)."""
        invalid_id = "invalid-id-format"
        mock_retrieve.return_value = {
            "status_code": 400,
            "code": "INVALID_ID_FORMAT",
            "message": "Bad request, e.g., invalid PointSetID format."
        }

        client = PointSetManagerAPIClient()
        response = client.retrieve_pointset(invalid_id)

        assert response["status_code"] == 400
        assert response["code"] == "INVALID_ID_FORMAT"


    @patch.object(PointSetManagerAPIClient, 'retrieve_pointset')
    def test_retrieve_pointset_database_unavailable(self, mock_retrieve):
        """Test retrieval when database unavailable (503)."""
        pointset_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_retrieve.return_value = {
            "status_code": 503,
            "code": "SERVICE_UNAVAILABLE",
            "message": "The PointSet storage layer (database) is unavailable."
        }

        client = PointSetManagerAPIClient()
        response = client.retrieve_pointset(pointset_id)

        assert response["status_code"] == 503
        assert response["code"] == "SERVICE_UNAVAILABLE"

    @patch('requests.get')
    def test_pointset_manager_retrieve_500(self, mock_get):
        """Cover lines 179-191: Status code not 200/404"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as cm:
            PointSetManager.retrieve("some-id")
        self.assertIn("PointSetManager returned 500", str(cm.exception))

    def test_route_invalid_uuid(self):
        """Cover lines 249-250: ValueError on UUID"""
        response = self.app.get('/triangulation/not-a-uuid')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['code'], "INVALID_POINTSET_ID")

    @patch('main.PointSetManager.retrieve')
    def test_route_connection_error(self, mock_retrieve):
        """Cover lines 262-273: ConnectionError"""
        mock_retrieve.side_effect = ConnectionError("DB down")
        response = self.app.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json['code'], "SERVICE_UNAVAILABLE")

    @patch('main.PointSetManager.retrieve')
    def test_route_generic_error(self, mock_retrieve):
        """Cover line 276: Generic Exception"""
        mock_retrieve.side_effect = Exception("Something bad")
        response = self.app.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['code'], "INTERNAL_ERROR")

    @patch('main.PointSetManager.retrieve')
    def test_route_not_found(self, mock_retrieve):
        """Cover line 285: PointSet is None"""
        mock_retrieve.return_value = None
        response = self.app.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['code'], "POINTSET_NOT_FOUND")

    @patch('main.PointSetManager.retrieve')
    @patch('main.Triangulator.triangulate')
    def test_route_triangulation_exception(self, mock_triangulate, mock_retrieve):
        """Cover line 291: Exception during triangulation"""
        mock_retrieve.return_value = PointSet(3, [[0,0], [1,0], [0,1]])
        mock_triangulate.side_effect = Exception("Math error")
        response = self.app.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json['code'], "TRIANGULATION_FAILED")

