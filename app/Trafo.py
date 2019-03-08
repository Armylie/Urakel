# Verwaltet verschiedene Methoden zur Grundtransformation der .stl Datei

import bpy # Fehler kann erstmal ignoriert werden, löst sich zur Laufzeit
import sys

# Initialisierung -> klären der Arbeitsoberfläche und Laden der in inpath gespeicherten Datei
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# numdiv-Faches verfeinern des Gitters, numsmooth-Faches glätten
def smooth(numdiv, numsmooth):
    bpy.ops.object.editmode_toggle() # alle Punkte auswählen
    for i in range(numdiv):
        bpy.ops.mesh.subdivide()
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=numsmooth)

# erstellt Boden der Höhe height
def buildbase(height):
    bpy.ops.mesh.extrude_region_move()
    bpy.ops.transform.resize(value=(1, 1, 0))
    bpy.ops.transform.translate(value=(0, 0, -height))

# vollständige Transformation
def transform(inpath,outpath,numdiv = 2, numsmooth = 2, height = 5):
    initialize(inpath)
    smooth(numdiv,numsmooth)
    buildbase(height)
    bpy.ops.export_mesh.stl(filepath=outpath)


if __name__ == "__main__":
    transform(sys.argv[5],sys.argv[6],numdiv = int (sys.argv[7]))
