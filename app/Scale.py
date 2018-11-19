import bpy # Fehler kann erstmal ignoriert werden, löst sich zur Laufzeit
import sys

# Initialisierung -> klären der Arbeitsoberfläche und Laden der in inpath gespeicherten Datei
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# TODO: Funkioniert scheinbar nur bei direkt eingabe, nicht über Python Skript im Blind Modus :o

def changeDim(X,Y,Z):
    bpy.context.object.dimensions[0] = X
    bpy.context.object.dimensions[1] = Y
    bpy.context.object.dimensions[2] = Z

def changeHeight(Z):
    bpy.context.object.dimensions[2] = Z

def changeScaled(X):
    oldX = bpy.context.object.dimensions[0]
    oldY = bpy.context.object.dimensions[1]
    bpy.context.object.dimensions[0] = X
    bpy.context.object.dimension[1] = oldY/oldX * X

def getValues():
    return [bpy.context.object.dimensions[0],bpy.context.object.dimensions[1],bpy.context.object.dimensions[2]]

if __name__ == "__main__":
    initialize(sys.argv[9])

    # TODO: anders Steuern welche Funktion ausgeführt wird
    if sys.argv[5] == '0':
        print(0)
        changeDim(int(sys.argv[6]),int(sys.argv[7]),int(sys.argv[8]))
    elif sys.argv[5] == 1:
        changeHeight(sys.argv[6])
    elif sys.argv[5] == 2:
        changeScaled(sys.argv[6])
    elif sys.argv[6] == 3:
        getValues() # TODO: geht das mit Returns so? Vermutlich nicht, da Aufruf in Blender -> wie bekommen wir die Werte da raus?
        # TODO: brauchen wir die Werte überhaupt? (damit Nutzer die sehen kanne!, Alternative: jede Matrix direkt auf nen Defailt skalieren den wir kennen?)
    bpy.ops.export_mesh.stl(filepath=sys.argv[10])