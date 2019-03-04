# Verwaltung von verschiedenen Skalierungsfunktionen

import bpy # Fehler kann erstmal ignoriert werden, löst sich zur Laufzeit
import csv
import sys


# Initialisierung -> klären der Arbeitsoberfläche und Laden der in inpath gespeicherten Datei
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# ändert alle drei übergebenen Dimensionen
def changeDim(X,Y,Z):
    bpy.context.object.dimensions[0] = X
    bpy.context.scene.update()
    bpy.context.object.dimensions[1] = Y
    bpy.context.scene.update()
    bpy.context.object.dimensions[2] = Z
    bpy.context.scene.update()

# Rückgabe der aktuellen Werte für Breite, Tiefe, Höhe
def getValues():
    return [bpy.context.object.dimensions[0],bpy.context.object.dimensions[1],bpy.context.object.dimensions[2]]


# Ausführung einer der obigen Funktionen (je nach übergebenem Parameter an stelle sys.argv[7]
if __name__ == "__main__":
    initialize(sys.argv[5])

    if sys.argv[7] == '0':
        changeDim(float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10]))
    elif sys.argv[7] == '1':
        # Speichern der X,Y,Z Werte in csv Datei zur späteren Weiterverarbeitung
        with open(__file__.replace('Scale.py','Temp\\dim.csv'),'w') as file:
            csv.writer(file).writerow(getValues())
    # Speichern der geänderten Datei
    bpy.ops.export_mesh.stl(filepath=sys.argv[6])