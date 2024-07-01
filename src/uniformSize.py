import numpy
from plyfile import PlyData

from Tiling import Tiling
from representation import Representation
from tile import Tile

class UniformSize(Tiling):
    """Cuts a point cloud into uniform size tiles"""

    def __init__(self, cloud:PlyData, x_tiles:int, y_tiles:int, z_tiles:int) -> None:
        """Constructor

        Args:
            cloud (PlyData): The point cloud to tile
            x_tiles (int): The number of tiles for the x axis
            y_tiles (int): The number of tiles for the y axis. The y axis points up.
            z_tiles (int): The number of tiles for the z axis.
        """
        self.cloud = cloud
        self.set_x_tiles(x_tiles)
        self.set_y_tiles(y_tiles)
        self.set_z_tiles(z_tiles)

    def make_tiles(self) -> list[Tile]:
        vertex = self.cloud["vertex"]

        # Find the min and the max of the point cloud
        x_min = vertex["x"].min()
        x_max = vertex["x"].max()
        y_min = vertex["y"].min()
        y_max = vertex["y"].max()
        z_min = vertex["z"].min()
        z_max = vertex["z"].max()

        # Get the size of the tiles for each axis
        x_size = (x_max - x_min) / self.x_tiles
        y_size = (y_max - y_min) / self.y_tiles
        z_size = (z_max - z_min) / self.z_tiles

        # Create the tiles
        tiles = list()

        # Assign the points to the corresponding tile
        x = numpy.floor((vertex["x"] - x_min) / x_size)
        # The points that are at the edge of the last bin are included in the last bin
        x = numpy.clip(x, None, self.x_tiles - 1)

        y = numpy.floor((vertex["y"] - y_min) / y_size)
        y = numpy.clip(y, None, self.y_tiles - 1)

        z = numpy.floor((vertex["z"] - z_min) / z_size)
        z = numpy.clip(z, None, self.z_tiles - 1)

        for i in range(0, self.x_tiles):
            for j in range(0, self.y_tiles):
                for k in range(0, self.z_tiles):
                    # Get the index of the points for this tile
                    indices = numpy.where((x == i) & (y == j) & (z == k))
                    # Get the points for this tile
                    points = vertex[indices]

                    # If there are points in the tile
                    if len(points) != 0:
                        # Get the center of the tile
                        cx = (i * x_size) + (x_size / 2) + x_min
                        cy = (j * y_size) + (y_size / 2) + y_min
                        cz = (k * z_size) + (z_size / 2) + z_min
                        
                        representation = Representation(points)

                        tile = Tile([representation], cx, cy, cz, x_size, y_size, z_size)
                        tiles.append(tile)

        return tiles

    def set_x_tiles(self, x_tiles:int):
        """Sets the number of tiles for the x axis

        Args:
            x_tiles (int): The number of tiles for the x axis

        Raises:
            ValueError: When x_axis is lower than 1
        """
        if x_tiles < 1:
            raise ValueError("There must be at least 1 tile for the x axis.")
        
        self.x_tiles = x_tiles
    
    def set_y_tiles(self, y_tiles:int):
        """Sets the number of tiles for the y axis

        Args:
            y_tiles (int): The number of tiles for the y axis

        Raises:
            ValueError: When y_axis is lower than 1
        """
        if y_tiles < 1:
            raise ValueError("There must be at least 1 tile for the y axis.")
        
        self.y_tiles = y_tiles

    def set_z_tiles(self, z_tiles:int):
        """Sets the number of tiles for the z axis

        Args:
            z_tiles (int): The number of tiles for the z axis

        Raises:
            ValueError: When z_axis is lower than 1
        """
        if z_tiles < 1:
            raise ValueError("There must be at least 1 tile for the z axis.")
        
        self.z_tiles = z_tiles
