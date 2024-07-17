from abc import abstractmethod

from tile import Tile

class Tiling:

    @abstractmethod
    def make_tiles(self) -> list[Tile]:
        """Cuts a point cloud into tiles according to the chosen strategy
        
        Returns:
            list[Tile]: The tiles
        """
        raise NotImplementedError()
