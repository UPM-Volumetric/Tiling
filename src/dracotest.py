import DracoPy
import numpy

with open("/home/obr/Documents/repos/UPM-Volumetrics/BrowserViewer/data/redandblack/tile_0_0.drc", "rb") as file:
    mesh = DracoPy.decode(file.read())

print(mesh.colors)

alpha = numpy.full((len(mesh.colors), 1), 128)
myColors = numpy.hstack((mesh.colors, alpha))

# print(myColors)

model = DracoPy.encode(mesh.points, colors=myColors.astype("uint8"))

with open("/home/obr/Documents/repos/UPM-Volumetrics/BrowserViewer/data/redandblackdraco/tile_0_0.drc", "wb") as file:
    file.write(model)
