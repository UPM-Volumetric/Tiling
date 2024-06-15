import numpy
from plyfile import PlyData, PlyElement

class Tile:
    """A tile of a point cloud"""

    def __init__(self, points:numpy.ndarray, x:float, y:float, z:float, x_size:float, y_size:float, z_size:float) -> None:
        """Constructor

        Args:
            points (numpy.ndarray): The points of the tile
            x (float): The tile's center x coordinate
            y (float): The tile's center y coordinate
            z (float): The tile's center z coordinate
            x_size (float): The size of the x-axis of the tile
            y_size (float): The size of the y-axis of the tile
            z_size (float): The size of the z-axis of the tile
        """
        self.points = points
        self.x = x
        self.y = y
        self.z = z
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

    def save(self, file_path:str, text:bool = False, byte_order:str = "=") -> None:
        """Saves the tile to path as a PLY file.

        Args:
            file_path (str): The path where to save the tile
            text (bool, optional): Whether the resulting PLY file will be text (True) or binary (False). Defaults to False.
            byte_order (str, optional): `<` for little-endian, `>` for big-endian, or `=` for native. This is only relevant if text is False. Defaults to "=".
        """
        element = PlyElement.describe(self.points, "vertex")

        PlyData([element], text=text, byte_order=byte_order).write(file_path)

    def manifest(self, segment_path:str = "") -> dict:
        """Returns the manifest representation of the tile

        Args:
            segment_path (str): The prefix to use before the segment name in the manifest.

        Returns:
            dict: The manifest representation of the tile
        """
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "width": self.x_size,
            "height": self.y_size,
            "depth": self.z_size,
            "segment": segment_path,
        }
