from tile.representation import Representation

class Tile:
    """A tile of a point cloud"""

    def __init__(self, representations:list[Representation], x:float, y:float, z:float, x_size:float, y_size:float, z_size:float) -> None:
        """Constructor

        Args:
            representations (list[Representation]): The representations of this tile (i.e. its levels of details)
            x (float): The tile's center x coordinate
            y (float): The tile's center y coordinate
            z (float): The tile's center z coordinate
            x_size (float): The size of the x-axis of the tile
            y_size (float): The size of the y-axis of the tile
            z_size (float): The size of the z-axis of the tile
        """
        self.representations = representations
        self.x = x
        self.y = y
        self.z = z
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size

    def save(self, format:str, path_prefix:str, text:bool = False, byte_order:str = "=") -> None:
        """Saves the representations of the tile as PLY files. The representations will have the following name `<path_prefix>_{i}.ply`.

        Args:
            format (str): The format in wich to save the tile. Use `ply` to save the tile in Polygon format. Use `drc` to compress the tile using Draco.
            path_prefix (str): The path where to save the tile without the extension
            text (bool, optional): Whether the resulting PLY file will be text (True) or binary (False). Defaults to False.
            byte_order (str, optional): `<` for little-endian, `>` for big-endian, or `=` for native. This is only relevant if text is False. Defaults to "=".
        """
        self.format = format

        for i in range(0, len(self.representations)):
            representation = self.representations[i]
            file_path = path_prefix + f"_{i}.{format}"

            representation.save(format, file_path, text, byte_order)

    def manifest(self, segment_prefix:str) -> dict:
        """Returns the manifest representation of the tile

        Args:
            segment_prefix (str): The prefix to use before the segment name in the manifest.

        Returns:
            dict: The manifest representation of the tile
        """
        representations = []

        for i in range(0, len(self.representations)):
            representation = self.representations[i]
            segment_path = segment_prefix + f"_{i}.{self.format}"

            representations.append(representation.manifest(segment_path))

        return {
            "position": {
                "x": self.x,
                "y": self.y,
                "z": self.z,
            },
            "width": self.x_size,
            "height": self.y_size,
            "depth": self.z_size,
            "representations": representations,
        }
