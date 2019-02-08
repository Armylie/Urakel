import numpy as np
import bpy
import sys

# import stl
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# Erstellung der Materialien für insgesamt 8 mögliche Klassen (+ Randfarbe)
# TODO: schönere Farben auswählen
def create_mats():
    color = [(0,0,1),(0,1,0),(1,0,0),(1,1,0),(1,0,1),(0,1,1),(1,1,0.5),(1,0.5,1),(0.5,1,1)]

    for i in range(9):
        mat = bpy.data.materials.new('Material'+str(i))
        bpy.context.active_object.data.materials.append(mat)
        mat.diffuse_color = color[i]


#wenn island[x,y] zu Klasse c gehört, färbe zwischen Knoten x, x+1 und y,y+1
#wähle hier die Entsprechenden Polygone aus
def markPolygons(island,c):
    a = 0
    # ignoriere letzte Zeile/Spalte, da Mapping über Knoten, wir aber Knoten-1 vertexe haben
    for x in range(len(island)-1):
        for y in range(len(island[0])-1):
            # TODO: Umwandlung bei mehr divides
            if island[x,y] == c:
                bpy.context.active_object.data.polygons[a].select = True
                bpy.context.active_object.data.polygons[a+1].select = True
            a = a + 2

# Färbe ein Cluster i ein (Cluster 0 entspricht dem Rand)
def colorOne(island, i):
    markPolygons(island, i)
    bpy.ops.object.editmode_toggle()
    bpy.context.object.active_material_index = i
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.object.editmode_toggle()

# Färbe die Cluster ein
# TODO: Methode für andere(unbekannte) Clusterzahlen
def colorAll(island,classes,):
    colorOne(island,0)
    for i in range(2,classes+2): # Beispiel: es gibt 4 Klassen -> range(2,6) = 2,3,4,5
        colorOne(island,i)


def color(inpath,outpath,islandpath):
    island = np.genfromtxt(islandpath, dtype=int)
    print(island)
    classes = 4 # TODO: calculate Klassenanzahl aus island (oder frage vom Nutzer ab)
    initialize(inpath)
    create_mats()
    colorAll(island,classes)
    # exportiere Dateien (hier kein image benötigt, nur .obj und .mtl, da keine Textur verwendet wird)
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')


if __name__ == "__main__":
    color(sys.argv[5],sys.argv[6],sys.argv[7])









