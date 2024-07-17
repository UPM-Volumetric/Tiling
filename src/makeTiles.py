import argparse
import json
import os
import typing
from plyfile import PlyData
from timeit import default_timer as timer

from tiling.Tiling import Tiling
from tiling.uniformDensity import UniformDensity
from tiling.uniformSize import UniformSize
from tiling.levelsOfDetails import LevelsOfDetails

# Common arguments
parser = argparse.ArgumentParser(description="Cuts a point cloud file into tiles and optionnally generates their levels of details using uniform subsampling.")
subparsers = parser.add_subparsers(dest="tile_strategy")

parser.add_argument("file", help="The point cloud file to tile. Only PLY files (.ply) are supported (ASCII or binary).")
parser.add_argument("directory", help="The directory where to save the tiles. The directory must exist as this script won't create it. The tiles are saved in a binary little endian PLY format. This does not affect the segment path in the manifest (see the tiles_prefix arg).")
parser.add_argument("manifest", help="The path where to save the JSON manifest.")
parser.add_argument("-p", "--tiles_prefix", default="", help="The prefix to use before the segment name in the manifest.")
parser.add_argument("-l", "--lod", type=float, action="append", default=[1.0], help="One or more subsampling ratios for the level of details of each tile. E.g. a ratio of 2 will generate a LOD with half the points.")

# Arguments for uniform size tiling
parser_uniform_size = subparsers.add_parser("uniform_size", description="Cuts the point cloud into uniform size tiles.")

parser_uniform_size.add_argument("x_tiles", type=int, help="The number of tiles in the x axis.")
parser_uniform_size.add_argument("y_tiles", type=int, help="The number of tiles in the y axis. The y axis points up.")
parser_uniform_size.add_argument("z_tiles", type=int, help="The number of tiles in the z axis.")

# Arguments for uniform density tiling
parser_uniform_density = subparsers.add_parser("uniform_density", description="Cuts the point cloud into uniform density tiles using an octree.")

parser_uniform_density.add_argument("max_points", type=int, help="The maximum number of points per tile.")

args = parser.parse_args()

start = timer()

# Load the point cloud
cloud = PlyData.read(args.file)

# Cut the tiles
tiler:Tiling

if args.tile_strategy == "uniform_size":
    tiler = UniformSize(cloud, args.x_tiles, args.y_tiles, args.z_tiles)
else:
    tiler = UniformDensity(cloud, args.max_points)

tiles = tiler.make_tiles()

# Make the levels of details
lod = LevelsOfDetails()
lods = []

for tile in tiles:
    lods.append(lod.make_lods(tile, args.lod))

# Build the manifest and save the tiles
i = 0
manifest:dict[str, typing.Any] = {"tiles": []}

for tile in lods:
    file_path = os.path.join(args.directory, f"tile_{i}")
    segment_path = os.path.join(args.tiles_prefix, f"tile_{i}")
    
    tile.save(file_path, byte_order="<")
    manifest["tiles"].append(tile.manifest(segment_path))

    i += 1

# Save the manifest
with open(args.manifest, "w") as file:
    json.dump(manifest, file)

end = timer()
print("Time elapsed:", end - start)
