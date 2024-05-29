import argparse
import json
import math
import numpy
import os
from plyfile import PlyData, PlyElement

# Arguments
parser = argparse.ArgumentParser(description="Cuts a point cloud file into uniform tiles.")

parser.add_argument("file", help="The point cloud file to tile. Only PLY files (.ply) are supported.")
parser.add_argument("x_tiles", type=int, help="The number of tiles in the x axis.")
parser.add_argument("y_tiles", type=int, help="The number of tiles in the y axis.")
parser.add_argument("z_tiles", type=int, help="The number of tiles in the z axis.")
parser.add_argument("directory", help="The directory where to save the tiles and the manifest. The directory must exist as this script won't create it.")
parser.add_argument("manifest", help="The path where to save the JSON manifest.")

args = parser.parse_args()

# Load the point cloud
cloud = PlyData.read(args.file)

# Find the min and the max of the point cloud
x_min = min(cloud["vertex"]["x"])
x_max = max(cloud["vertex"]["x"])
y_min = min(cloud["vertex"]["y"])
y_max = max(cloud["vertex"]["y"])
z_min = min(cloud["vertex"]["z"])
z_max = max(cloud["vertex"]["z"])

# Get the size of the tiles for each axis
x_size = (x_max - x_min) / args.x_tiles
y_size = (y_max - y_min) / args.y_tiles
z_size = (z_max - z_min) / args.z_tiles

# Create the tiles
tiles = numpy.empty((args.x_tiles, args.y_tiles, args.z_tiles), list)

# Assign the points to the corresponding tile
for point in cloud["vertex"]:
    x = math.floor((point["x"] - x_min) / x_size)
    y = math.floor((point["y"] - y_min) / y_size)
    z = math.floor((point["z"] - z_min) / z_size)

    # The points that are at the edge of the last bin are included in the last bin
    x = min(x, args.x_tiles - 1)
    y = min(y, args.y_tiles - 1)
    z = min(z, args.z_tiles - 1)

    if tiles[x, y, z] == None:
        tiles[x, y, z] = list()
    
    tiles[x, y, z].append(point)

# Save the tiles
i = 0
manifest = {"tiles": []}

for x in range(0, args.x_tiles):
    for y in range(0, args.y_tiles):
        for z in range(0, args.z_tiles):
            tile = tiles[x, y, z]

            if tile != None:
                # Save the PLY
                element = PlyElement.describe(numpy.array(tile), "vertex")

                path = os.path.join(args.directory, f"tile_{i}.ply")
                
                PlyData([element]).write(path)

                i += 1

                # Update the manifest

                # Get the center of the tiles
                xx = (x * x_size) + (x_size / 2)
                yy = (y * y_size) + (y_size / 2)
                zz = (z * z_size) + (z_size / 2)

                manifest["tiles"].append({
                    "x": xx,
                    "y": yy,
                    "z": zz,
                    "width": x_size,
                    "height": y_size,
                    "depth": z_size,
                    "segment": path,
                })

# Export the manifest
with open(args.manifest, "w") as file:
    json.dump(manifest, file)
