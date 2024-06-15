import math
import numpy
from plyfile import PlyData

from representation import Representation
from tile import Tile

class UniformTiles:
    """Cuts a point cloud into uniform tiles"""

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
        x_min = min(vertex["x"])
        x_max = max(vertex["x"])
        y_min = min(vertex["y"])
        y_max = max(vertex["y"])
        z_min = min(vertex["z"])
        z_max = max(vertex["z"])

        # Get the size of the tiles for each axis
        x_size = (x_max - x_min) / self.x_tiles
        y_size = (y_max - y_min) / self.y_tiles
        z_size = (z_max - z_min) / self.z_tiles

        # Create the tiles
        tilesPoints = numpy.empty((self.x_tiles, self.y_tiles, self.z_tiles), list)

        # Assign the points to the corresponding tile
        for point in vertex:
            x = math.floor((point["x"] - x_min) / x_size)
            y = math.floor((point["y"] - y_min) / y_size)
            z = math.floor((point["z"] - z_min) / z_size)

            # The points that are at the edge of the last bin are included in the last bin
            x = min(x, self.x_tiles - 1)
            y = min(y, self.y_tiles - 1)
            z = min(z, self.z_tiles - 1)

            if tilesPoints[x, y, z] == None:
                tilesPoints[x, y, z] = list()
            
            tilesPoints[x, y, z].append(point)

        tiles = list()

        # Turn the list points into tiles
        for i in range(0, self.x_tiles):
            for j in range(0, self.y_tiles):
                for k in range(0, self.z_tiles):
                    points = tilesPoints[i, j, k]

                    # If there are points in the tile
                    if points != None:
                        # Get the center of the tile
                        x = (i * x_size) + (x_size / 2) + x_min
                        y = (j * y_size) + (y_size / 2) + y_min
                        z = (k * z_size) + (z_size / 2) + z_min

                        representation = Representation(numpy.array(points))
                        tile = Tile([representation], x, y, z, x_size, y_size, z_size)

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
