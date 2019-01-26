# in
import numpy as np
import bpy

outpath = "C:\\Users\\Sara\\Desktop\\Jahresprojekt\\04UmatrixDresden\\UTrans.obj"
islandpath = 'C:\\Users\\Sara\\Desktop\\Jahresprojekt\\04UmatrixDresden\\island.txt'


# import stl
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# Erstellung der Materialien für insgesamt 8 mögliche Klassen (+ Randfarbe)
# TODO: schönere Farben auswählen
def create_mats(obj):
    color = [(0,0,1),(0,1,0),(1,0,0),(1,1,0),(1,0,1),(0,1,1),(1,1,0.5),(1,0.5,1),(0.5,1,1)]

    for i in range(9):
        mat = bpy.data.materials.new('Material'+str(i))
        obj.data.materials.append(mat)
        mat.diffuse_color = color[i]


#wenn island[x,y] zu Klasse c gehört, färbe zwischen Knoten x, x+1 und y,y+1
#wähle hier die Entsprechenden Polygone aus
def markPolygons(island,c,obj):
    a = 0
    # ignoriere letzte Zeile/Spalte, da Mapping über Knoten, wir aber Knoten-1 vertexe haben
    for x in range(len(island)-1):
        for y in range(len(island[0])-1):
            if island[x,y] == c:
                obj.data.polygons[a].select = True
                obj.data.polygons[a+1].select = True
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
def colorAll(island,classes):
    color(island,0)
    for i in range(2,classes+2): # Beispiel: es gibt 4 Klassen -> range(2,6) = 2,3,4,5
        color(island,i)


def color(inpath,outpath,islandpath):
    island = np.genfromtxt(islandpath, dtype=int)
    classes = 4 # TODO: calculate Klassenanzahl aus island (oder frage vom Nutzer ab)
    obj = bpy.context.active_object
    initialize(inpath)
    create_mats(obj)
    colorAll(island,classes,obj)
    # exportiere Dateien (hier kein image benötigt, nur .obj und .mtl, da keine Textur verwendet wird)
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')








