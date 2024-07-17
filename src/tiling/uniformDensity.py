import numpy
from plyfile import PlyData

from tiling.Tiling import Tiling
from tile.representation import Representation
from tile.tile import Tile

class UniformDensity(Tiling):
    """Cuts a point cloud into uniform density tiles"""

    def __init__(self, cloud:PlyData, max_points:int) -> None:
        """Constructor

        Args:
            cloud (PlyData): The point cloud to tile
            max_points (int): The maximum number of points in each tile
        """
        self.cloud = cloud
        self.set_max_points(max_points)
        self.tiles = list[Tile]()

    def make_tiles(self) -> list[Tile]:
        vertex = self.cloud["vertex"]

        if (len(vertex) > self.max_points):
            self.iterate(vertex)

        return self.tiles

    def iterate(self, vertex:PlyData) -> None:
        """Recursively cuts a point cloud into eight tiles using an octree, until the tiles have at most `max_points`.

        Args:
            vertex (PlyData): The point cloud
        """
        # Find the bounding box of the point cloud
        x_min = vertex["x"].min()
        x_max = vertex["x"].max()
        y_min = vertex["y"].min()
        y_max = vertex["y"].max()
        z_min = vertex["z"].min()
        z_max = vertex["z"].max()

        # Get the size of the tiles for each axis
        x_size = (x_max - x_min) / 2
        y_size = (y_max - y_min) / 2
        z_size = (z_max - z_min) / 2

        # Divide the space in 8 tiles (octree)
        # Compute the index where each point goes
        x = numpy.floor((vertex["x"] - x_min) / x_size)
        # The points that are at the edge of the last bin are included in the last bin
        x = numpy.clip(x, None, 1)

        y = numpy.floor((vertex["y"] - y_min) / y_size)
        y = numpy.clip(y, None, 1)

        z = numpy.floor((vertex["z"] - z_min) / z_size)
        z = numpy.clip(z, None, 1)

        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    # Get the index of the points for this tile
                    indices = numpy.where((x == i) & (y == j) & (z == k))
                    # Get the points for this tile
                    points = vertex[indices]

                    # Subdivide the tiles if there are too many points
                    if (len(points) > self.max_points):
                        self.iterate(points)
                    elif len(points) != 0:
                        # Get the center of the tile
                        cx = (i * x_size) + (x_size / 2) + x_min
                        cy = (j * y_size) + (y_size / 2) + y_min
                        cz = (k * z_size) + (z_size / 2) + z_min
                        
                        representation = Representation(points)

                        tile = Tile([representation], cx, cy, cz, x_size, y_size, z_size)
                        self.tiles.append(tile)

    def set_max_points(self, max_points:int) -> None:
        """Sets the maximum number of points in each tile

        Args:
            max_points (int): The maximum number of points in each tile

        Raises:
            ValueError: When max_points is lower than 1
        """
        if max_points <= 0:
            raise ValueError("There must be at least one point in each tile.")
        
        self.max_points = max_points
