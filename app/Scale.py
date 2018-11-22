import bpy # Fehler kann erstmal ignoriert werden, löst sich zur Laufzeit
import csv
import sys

# Initialisierung -> klären der Arbeitsoberfläche und Laden der in inpath gespeicherten Datei
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)


def changeDim(X,Y,Z):
    bpy.context.object.dimensions[0] = X
    bpy.context.scene.update()
    bpy.context.object.dimensions[1] = Y
    bpy.context.scene.update()
    bpy.context.object.dimensions[2] = Z
    bpy.context.scene.update()

def changeHeight(Z):
    bpy.context.object.dimensions[2] = Z
    bpy.context.scene.update()

def changeScaled(X):
    oldX = bpy.context.object.dimensions[0]
    oldY = bpy.context.object.dimensions[1]
    bpy.context.object.dimensions[0] = X
    bpy.context.scene.update()
    bpy.context.object.dimension[1] = oldY/oldX * X
    bpy.context.scene.update()

def getValues():
    return [bpy.context.object.dimensions[0],bpy.context.object.dimensions[1],bpy.context.object.dimensions[2]]

if __name__ == "__main__":
    initialize(sys.argv[5])

    # TODO: anders Steuern welche Funktion ausgeführt wird
    if sys.argv[7] == '0':
        changeDim(float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10]))
    elif sys.argv[7] == '1':
        changeHeight(sys.argv[8])
    elif sys.argv[7] == '2':
        changeScaled(sys.argv[8])
    elif sys.argv[7] == '3':
        with open('C:\\Users\\Sara\\Desktop\\Upload\\dim.csv','w') as file:
            csv.writer(file).writerow(getValues())
    bpy.ops.export_mesh.stl(filepath=sys.argv[6])