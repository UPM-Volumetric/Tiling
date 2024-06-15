import numpy
from plyfile import PlyData, PlyElement

class Representation:
    """A representation for a tile of a point cloud"""

    def __init__(self, points:numpy.ndarray) -> None:
        self.points = points

    def save(self, file_path:str, text:bool = False, byte_order:str = "=") -> None:
        """Saves the representation to path as a PLY file.

        Args:
            file_path (str): The path where to save the tile
            text (bool, optional): Whether the resulting PLY file will be text (True) or binary (False). Defaults to False.
            byte_order (str, optional): `<` for little-endian, `>` for big-endian, or `=` for native. This is only relevant if text is False. Defaults to "=".
        """
        element = PlyElement.describe(self.points, "vertex")

        PlyData([element], text=text, byte_order=byte_order).write(file_path)

    def manifest(self, segment_path:str) -> dict:
        """Returns this object in JSON format to write in the manifest

        Args:
            segment_path (str): The path of the segment on the server

        Returns:
            dict: JSON data to write in the manifest
        """
        return {
            "points": len(self.points),
            "segment": segment_path
        }
