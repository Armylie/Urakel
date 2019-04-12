# Verwaltung von verschiedenen Skalierungsfunktionen

import bpy # Fehler kann erstmal ignoriert werden, löst sich zur Laufzeit
import csv
import sys


# clear workspace and import .stl (from inpath)
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# change all three Dimensions X,Y,Z
def changeDim(X,Y,Z):
    bpy.context.object.dimensions[0] = X
    bpy.context.scene.update()
    bpy.context.object.dimensions[1] = Y
    bpy.context.scene.update()
    bpy.context.object.dimensions[2] = Z
    bpy.context.scene.update()

# get the current values for width, depth, height
def getValues():
    return [bpy.context.object.dimensions[0],bpy.context.object.dimensions[1],bpy.context.object.dimensions[2]]


# execute one of the functions above (depending on parameter at sys.argv[7])
if __name__ == "__main__":
    initialize(sys.argv[5])

    if sys.argv[7] == '0':
        changeDim(float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10]))
    elif sys.argv[7] == '1':
        # save the X,Y,Z values in a .csv file for further processing
        with open(__file__.replace('Scale.py','Temp\\dim.csv'),'w') as file:
            csv.writer(file).writerow(getValues())
    # save the new file
    bpy.ops.export_mesh.stl(filepath=sys.argv[6])