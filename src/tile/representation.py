import io
import numpy
from plyfile import PlyData, PlyElement
import DracoPy

class Representation:
    """A representation for a tile of a point cloud"""

    def __init__(self, points:numpy.ndarray) -> None:
        self.points = points

    def save(self, format:str, file_path:str, text:bool = False, byte_order:str = "=") -> None:
        """Saves the representation to path as a PLY file.

        Args:
            format (str): The format in wich to save the tile. Use `ply` to save the tile in Polygon format. Use `drc` to compress the tile using Draco.
            file_path (str): The path where to save the tile
            text (bool, optional): Whether the resulting PLY file will be text (True) or binary (False). Defaults to False.
            byte_order (str, optional): `<` for little-endian, `>` for big-endian, or `=` for native. This is only relevant if text is False. Defaults to "=".
        """
        # Write the representation as a PLY file
        if format == "ply":
            element = PlyElement.describe(self.points, "vertex")
            
            PlyData([element], text=text, byte_order=byte_order).write(file_path)
        # Compress the data with Draco and save it
        elif format == "drc":
            points = numpy.dstack((self.points["x"], self.points["y"], self.points["z"]))[0]
            colors = numpy.dstack((self.points["red"], self.points["green"], self.points["blue"]))[0]

            model = DracoPy.encode(points, colors=colors)

            with open(file_path, "wb") as file:
                file.write(model)

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
