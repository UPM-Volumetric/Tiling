import argparse
from argparse import RawTextHelpFormatter
import json
import math
import numpy
import os
from plyfile import PlyData, PlyElement

from ranged_type import ranged_type

parser = argparse.ArgumentParser(description="Generates levels of details (LODs) for the tiles of a point cloud.", formatter_class=RawTextHelpFormatter)

parser.add_argument("file", help="The point cloud file to tile. Only PLY files (.ply) are supported (ASCII or binary).")
parser.add_argument("levels", type=ranged_type(int, 2), help="The number of LODs to generate for each tile. Must be at least 2.")
parser.add_argument("mode", choices=["progressive", "cummulative"], help="Progressive : The LODs are to be combined to reconstruct the tile. Saves storage space and offers more flexibility at cost of increased complexity. \nCummulative : The better quality LODs contains the points of the lower quality LODs. Only one LOD has to be loaded per tile. Reduces complexity at the cost of more storage size and decreased flexibility.")
parser.add_argument("directory", help="The directory where to save the LODs. The directory must exist as this script won't create it. The LODs are saved in a binary little endian PLY format.")
parser.add_argument("manifest", help="The path where to save the JSON manifest.")

args = parser.parse_args()

# Load the tile
cloud = PlyData.read(args.file)