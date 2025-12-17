"""Flask server to triangulate point sets."""
import struct
import uuid

import requests
from flask import Flask, Response, jsonify


class PointSet:
    """Represent a set of points for triangulation."""

    def __init__(self, n_points, points):
        """Initialize a PointSet.

        Args:
            n_points: Number of points.
            points: List of point coordinates.

        """
        self.n_points = n_points
        self.points = points

    def to_binary(self):
        """Convert PointSet to binary representation.

        Returns:
            Binary data or None if invalid.

        """
        if self.n_points < 0:
            return None
        try:
            data = struct.pack('<I', self.n_points)
            for p in self.points:
                data += struct.pack('<ff', float(p[0]), float(p[1]))
            return data
        except Exception:
            return None

    @staticmethod
    def from_binary(data):
        """Create PointSet from binary representation.

        Args:
            data: Binary data to parse.

        Returns:
            PointSet instance or None if invalid.

        """
        try:
            n_points = struct.unpack('<I', data[:4])[0]
            points = []
            offset = 4
            for _ in range(n_points):
                x, y = struct.unpack('<ff', data[offset:offset + 8])
                points.append([x, y])
                offset += 8
            return PointSet(n_points, points)
        except Exception:
            return None

    @property
    def num_points(self):
        """Get number of points."""
        return self.n_points

    def __eq__(self, other):
        """Check equality with another PointSet."""
        if not isinstance(other, PointSet):
            return False
        return self.n_points == other.n_points and self.points == other.points


class Triangles:
    """Represent triangles formed from a set of points."""

    def __init__(self, pointset, n_triangles, triangles):
        """Initialize Triangles.

        Args:
            pointset: PointSet instance.
            n_triangles: Number of triangles.
            triangles: List of triangle indices.

        """
        self.pointset = pointset
        self.n_triangles = n_triangles
        self.triangles = triangles

    def to_binary(self):
        """Convert Triangles to binary representation.

        Returns:
            Binary data or None if invalid.

        """
        pointset_binary = self.pointset.to_binary()
        if pointset_binary is None:
            return None

        # Validate indices
        for t in self.triangles:
            for idx in t:
                if idx >= self.pointset.n_points:
                    return None

        try:
            data = pointset_binary
            data += struct.pack('<I', self.n_triangles)
            for t in self.triangles:
                data += struct.pack('<III', t[0], t[1], t[2])
            return data
        except Exception:
            return None

    @staticmethod
    def from_binary(data):
        """Create Triangles from binary representation.

        Args:
            data: Binary data to parse.

        Returns:
            Triangles instance or None if invalid.

        """
        try:
            n_points = struct.unpack('<I', data[:4])[0]
            pointset_size = 4 + n_points * 8
            pointset_data = data[:pointset_size]
            pointset = PointSet.from_binary(pointset_data)

            if pointset is None:
                return None

            offset = pointset_size
            n_triangles = struct.unpack('<I', data[offset:offset + 4])[0]
            offset += 4
            triangles = []
            for _ in range(n_triangles):
                t = struct.unpack('<III', data[offset:offset + 12])
                triangles.append(list(t))
                offset += 12

            return Triangles(pointset, n_triangles, triangles)
        except Exception:
            return None

    def __eq__(self, other):
        """Check equality with another Triangles instance."""
        if not isinstance(other, Triangles):
            return False
        return (self.pointset.n_points == other.pointset.n_points and
                self.pointset.points == other.pointset.points and
                self.n_triangles == other.n_triangles and
                self.triangles == other.triangles)


class PointSetManager:
    """Manager for retrieving PointSet from remote service."""

    BASE_URL = "http://localhost:5000"  # Default, should be configurable

    @staticmethod
    def retrieve(point_set_id):
        """Retrieve a PointSet from the remote service.

        Args:
            point_set_id: The ID of the PointSet to retrieve.

        Returns:
            PointSet instance or None if not found.

        Raises:
            ConnectionError: If the service is unavailable.

        """
        try:
            response = requests.get(
                f"{PointSetManager.BASE_URL}/pointset/{point_set_id}"
            )
            if response.status_code == 200:
                return PointSet.from_binary(response.content)
            elif response.status_code == 404:
                return None
            else:
                msg = f"PointSetManager returned {response.status_code}"
                raise Exception(msg)
        except requests.RequestException as err:
            raise ConnectionError("PointSetManager unavailable") from err


class Triangulator:
    """Triangulator for computing Delaunay triangulation."""

    @staticmethod
    def triangulate(pointset):
        """Triangulate a set of points using Delaunay triangulation.

        Args:
            pointset: PointSet to triangulate.

        Returns:
            Triangles instance.

        """
        if pointset.n_points < 3:
            return Triangles(pointset, 0, [])

        try:
            import numpy as np
            from scipy.spatial import Delaunay
            points = np.array(pointset.points)
            tri = Delaunay(points)
            simplices = tri.simplices.tolist()
            return Triangles(pointset, len(simplices), simplices)
        except ImportError:
            return Triangles(pointset, 0, [])


def init():
    """Initialize Flask application.

    Returns:
        Flask app instance.

    """
    app = Flask(__name__)
    return app


app = init()


@app.route('/triangulation/<pointSetId>', methods=['GET'])
def triangulation(pointSetId):
    """Get triangulation for a PointSet.

    Args:
        pointSetId: UUID of the PointSet.

    Returns:
        Binary triangulation data or error response.

    """
    try:
        uuid.UUID(pointSetId)
    except ValueError:
        return (
            jsonify(
                {
                    "code": "INVALID_POINTSET_ID",
                    "message": "Invalid PointSet ID format",
                }
            ),
            400,
        )

    try:
        pointset = PointSetManager.retrieve(pointSetId)
    except ConnectionError:
        return (
            jsonify(
                {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "PointSetManager unavailable",
                }
            ),
            503,
        )
    except Exception as e:
        return jsonify({"code": "INTERNAL_ERROR", "message": str(e)}), 500

    if pointset is None:
        return (
            jsonify(
                {"code": "POINTSET_NOT_FOUND", "message": "PointSet not found"}
            ),
            404,
        )

    try:
        triangles = Triangulator.triangulate(pointset)
        return Response(triangles.to_binary(), mimetype='application/octet-stream')
    except Exception as e:
        return jsonify({"code": "TRIANGULATION_FAILED", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
