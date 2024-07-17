import numpy

from tile.representation import Representation
from tile.tile import Tile

class LevelsOfDetails:
    """Generates levels of details of a tile"""
    
    def make_lods(self, tile:Tile, subsampling_ratios:list[float]) -> Tile:
        """Generates the levels of details of a tile

        Args:
            tile (Tile): The tile to process
            subsampling_ratios (list[float]): The subsampling ratios of the levels of details

        Returns:
            Tile: The tile with its levels of details
        """
        representations = []
        points = tile.representations[0].points
        points.sort()

        for subsampling_ratio in subsampling_ratios:
            representation = self.make_lod(points, subsampling_ratio)
            representations.append(representation)

        return Tile(representations, tile.x, tile.y, tile.z, tile.x_size, tile.y_size, tile.z_size)

    def make_lod(self, points:numpy.ndarray, subsampling_ratio:float) -> Representation:
        """Generate a level of details of a tile using uniform subsampling

        Args:
            points (numpy.ndarray): The points to process. For performance reason, we assume that the points are already sorted by x, then by y, then by z coordinates.
            subsampling_ratio (float): The ratio of points to remove (e.g. 2 removes half the points)

        Raises:
            ValueError: If subsampling_ratio is lower than 1

        Returns:
            Representation: The level of detail
        """
        if subsampling_ratio == 1:
            return Representation(points)
        
        if (subsampling_ratio < 1):
            raise ValueError("The subsampling ratio must be at least 1.")

        numPoints = len(points)
        numFinalPoints = round(numPoints / subsampling_ratio)

        # TODO Make sure that the index is unique so we dont have the same point twice or more in the file
        indices = subsampling_ratio * numpy.arange(numFinalPoints)
        indices = indices.round().astype(int)

        finalPoints = points[indices]

        return Representation(finalPoints)
