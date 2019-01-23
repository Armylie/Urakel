# in
import numpy as np
import bpy

# Pfad zum Mapping (später als Variable übergeben)
island = np.genfromtxt('C:\\Users\\Sara\\Desktop\\Jahresprojekt\\04UmatrixDresden\\island.txt', dtype=int)

obj = bpy.context.active_object

# Erstellung der Materialien für jede Klasse
#TODO: automatisierte Materialerstellung (in Schleife)
mat1 = bpy.data.materials.new("Material1")
obj.data.materials.append(mat1)
mat1.diffuse_color = (1,0,0)

mat2 = bpy.data.materials.new("Material2")
obj.data.materials.append(mat2)
mat2.diffuse_color = (0,1,0)

mat3 = bpy.data.materials.new("Material3")
obj.data.materials.append(mat3)
mat3.diffuse_color = (0,0,1)

mat4 = bpy.data.materials.new("Material4")
obj.data.materials.append(mat4)
mat4.diffuse_color = (0,1,1)

mat5 = bpy.data.materials.new("Material5")
obj.data.materials.append(mat5)
mat5.diffuse_color = (1,1,0)

mat6 = bpy.data.materials.new("Material6")
obj.data.materials.append(mat6)
mat6.diffuse_color = (1,0,1)


#wenn island[x,y] zu Klasse c gehört, färbe zwischen Knoten x, x+1 und y,y+1
#wähle hier die Entsprechenden vertices aus
def color(island,c):
    a = 0
    # ignoriere letzte Zeile/Spalte, da Mapping über Knoten, wir aber Knoten-1 vertexe haben
    for x in range(len(island)-1):
        for y in range(len(island[0])-1):
            if island[x,y] == c:
                obj.data.polygons[a].select = True
                obj.data.polygons[a+1].select = True
            a = a + 2

# Färbe die Cluster ein
# TODO: Methode für andere(unbekannte) Clusterzahlen
for i in [0,2,3,4,5]:
    color(island,i)
    bpy.ops.object.editmode_toggle()
    bpy.context.object.active_material_index = i
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.object.editmode_toggle()

# exportiere Dateien (hier kein image benötigt, nur .obj und .mtl, da keine Textur verwendet wird)
bpy.ops.export_scene.obj(filepath = "C:\\Users\\Sara\\Desktop\\Jahresprojekt\\04UmatrixDresden\\UTrans.obj",path_mode='ABSOLUTE')








