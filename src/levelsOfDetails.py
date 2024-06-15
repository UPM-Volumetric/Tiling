import numpy

from representation import Representation
from tile import Tile

class LevelsOfDetails:
    """Generates levels of details of a tile"""
    def make_lods(self, tile:Tile, subsampling_ratios:list[float]) -> Tile:
        representations = []
        points = tile.representations[0].points

        for ratio in subsampling_ratios:
            representation = self.make_lod(points, ratio)
            representations.append(representation)

        return Tile(representations, tile.x, tile.y, tile.z, tile.x_size, tile.y_size, tile.z_size)

    def make_lod(self, points:numpy.ndarray, subsampling_ratio:float) -> Representation:
        """Generate a level of details of a tile using uniform subsampling

        Args:
            points (numpy.ndarray): The points to process
            subsampling_ratio (float): The ratio of points to remove (e.g. 2 removes half the points)

        Raises:
            ValueError: If subsampling_ratio is lower than 1

        Returns:
            Representation: The level of detail
        """
        if (subsampling_ratio < 1):
            raise ValueError("The subsampling ratio must be at least 1.")

        numPoints = len(points)
        numFinalPoints = round(numPoints / subsampling_ratio)

        points.sort()

        finalPoints = list()

        for i in range(0, numFinalPoints):
            # TODO Make sure that the index is unique so we dont have the same point twice or more in the file
            index = round(i * subsampling_ratio)

            finalPoints.append(points[index])

        return Representation(numpy.array(finalPoints))
