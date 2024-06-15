import argparse
import json
import os
from plyfile import PlyData

from uniformTiles import UniformTiles

# Arguments
parser = argparse.ArgumentParser(description="Cuts a point cloud file into uniform tiles and optionnally generates their levels of details.")

parser.add_argument("file", help="The point cloud file to tile. Only PLY files (.ply) are supported (ASCII or binary).")
parser.add_argument("x_tiles", type=int, help="The number of tiles in the x axis.")
parser.add_argument("y_tiles", type=int, help="The number of tiles in the y axis. The y axis points up.")
parser.add_argument("z_tiles", type=int, help="The number of tiles in the z axis.")
parser.add_argument("directory", help="The directory where to save the tiles. The directory must exist as this script won't create it. The tiles are saved in a binary little endian PLY format. This does not affect the segment path in the manifest (see the tiles_prefix arg).")
parser.add_argument("manifest", help="The path where to save the JSON manifest.")
parser.add_argument("-p", "--tiles_prefix", default="", help="The prefix to use before the segment name in the manifest.")
parser.add_argument("-l", "--lod", nargs="+", help="One or more subsampling ratios for the level of details of each tile. E.g. a ratio of 2 will generate a LOD with half the points.")

args = parser.parse_args()

# Load the point cloud
cloud = PlyData.read(args.file)

# Cut the tiles
tiler = UniformTiles(cloud, args.x_tiles, args.y_tiles, args.z_tiles)
tiles = tiler.make_tiles()

# Build the manifest and save the tiles
i = 0
manifest = {"tiles": []}

for tile in tiles:
    file_path = os.path.join(args.directory, f"tile_{i}.ply")
    segment_path = os.path.join(args.tiles_prefix, f"tile_{i}.ply")
    
    tile.save(file_path, "<")
    manifest["tiles"].append(tile.manifest(segment_path))

    i += 1

# Save the manifest
with open(args.manifest, "w") as file:
    json.dump(manifest, file)
