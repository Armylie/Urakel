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
def create_mats():
    # Farben entstammen dem Farbschema tab10
    color = [(0.12, 0.47, 0.71), (1.0, 0.5, 0.05), (0.17, 0.63, 0.17), (0.84, 0.15, 0.16), (0.58, 0.40, 0.74),
             (0.89, 0.47, 0.76), (0.74, 0.74, 0.13),(0.09, 0.75, 0.81),(0.5,0.5,0.5)]

    for i in range(9):
        mat = bpy.data.materials.new('Material'+str(i))
        bpy.context.active_object.data.materials.append(mat)
        mat.diffuse_color = color[i]


#wenn island[x,y] zu Klasse c gehört, färbe zwischen Knoten x, x+1 und y,y+1
#wähle hier die Entsprechenden Polygone aus
# div = 1
def markPolygons(island,c,div):
    a = 0
    # ignoriere letzte Zeile/Spalte, da Mapping über Knoten, wir aber Knoten-1 vertexe haben
    for x in range(len(island)-1):
        for y in range(len(island[0])-1):
            if island[x,y] >= c: # erhalte sauberere (nicht blaue) Ränder durch Färben in Aufsteigender Reihenfolge
                # jeweils zwei Dreiecke pro Punkt in mapping
                bpy.context.active_object.data.polygons[a].select = True
                bpy.context.active_object.data.polygons[a+1].select = True
            a = a + 2
    if div > 1:
        a = markPolygons2(island,c,a)
    if div > 2:
        markPolygons3(island,c,a)


# div = 2
def markPolygons2(island,c,a):
    for x in range(len(island)-1,0,-1):
        for y in range(len(island[0])-1,0,-1):
            for i in range(3):
                if island[x, y] >= c:
                    bpy.context.active_object.data.polygons[a].select = True
                    bpy.context.active_object.data.polygons[a+1].select = True
                a = a + 2
    return a


# div = 3
def markPolygons3(island,c,a):
    for x in range(len(island)-1):
        for y in range(len(island[0])-1):
            for i in range(9):
                if island[x, y] >= c:
                    bpy.context.active_object.data.polygons[a].select = True
                    bpy.context.active_object.data.polygons[a + 1].select = True
                a = a + 2
    markPolygons2(island,c,a)


# Färbe Cluster i ein (Cluster 0 entspricht dem Rand)
def colorOne(island, i,div):
    markPolygons(island, i,div)
    bpy.ops.object.editmode_toggle()
    bpy.context.object.active_material_index = i
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.object.editmode_toggle()


def color(inpath,outpath,islandpath,div=1):
    island = np.genfromtxt(islandpath, dtype=int) # Textdatei als np array
    classes = findNumbers(island)
    initialize(inpath)
    create_mats()
    # färbe alle Klassen ein
    for i in classes:
       colorOne(island,i,div)
    # exportiere Dateien (hier kein image benötigt, nur .obj und .mtl, da keine Textur verwendet wird)
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')


def findNumbers (X):
    c = []
    for i in range(X.min(),X.max()+1):
        if X.__contains__(i):
            c.append(i)
    return c


if __name__ == "__main__":
    color(sys.argv[5],sys.argv[6],sys.argv[7],int(sys.argv[8]))









