import numpy
from tile import Tile

class LevelsOfDetails:
    """Generates levels of details of a tile"""
    def make_lod(self, tile:Tile, subsampling_ratio:float) -> Tile:
        """Generate a level of details of a tile using uniform subsampling

        Args:
            tile (Tile): The tile to process
            subsampling_ratio (float): The ratio of points to remove (e.g. 2 removes half the points)

        Raises:
            ValueError: If subsampling_ratio is lower than 1

        Returns:
            Tile: The level of detail
        """
        if (subsampling_ratio < 1):
            raise ValueError("The subsampling ratio must be at least 1.")

        numPoints = len(tile.points)
        numFinalPoints = round(numPoints / subsampling_ratio)

        tile.points.sort()

        finalPoints = list()

        for i in range(0, numFinalPoints):
            index = round(i * subsampling_ratio)

            finalPoints.append(tile.points[index])

        # TODO Be more efficient
        return Tile(numpy.array(finalPoints), tile.x, tile.y, tile.z, tile.x_size, tile.y_size, tile.z_size)
