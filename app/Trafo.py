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
def buildbase(height,dimz):
    bpy.ops.mesh.extrude_region_move() # kopieren aller Punkte
    bpy.ops.transform.resize(value=(1, 1, 0)) # verschieben der Kopien auf eine Ebene
    bpy.ops.transform.translate(value=(0,0,-dimz/2)) # verschieben auf z = 0
    bpy.ops.transform.translate(value=(0, 0, -height)) # erstellen des Bodens der Höhe height

# vollständige Transformation
# TODO: height anpassen -> welches Verhältnis zur Gesamthöhe? (bei Veränderung auch size und offset ändern)
def transform(inpath,outpath,numdiv = 2, numsmooth = 2):
    initialize(inpath)
    dimz = bpy.context.object.dimensions[2]
    smooth(numdiv,numsmooth)
    buildbase(dimz/4,dimz)
    bpy.ops.export_mesh.stl(filepath=outpath)


if __name__ == "__main__":
    transform(sys.argv[5],sys.argv[6],numdiv = int (sys.argv[7]))
