#--------------------------------------------------------------------
# Allgemein: ob = bpy.data.objects.get("UStar")  statt bpy.context.object
#--------------------------------------------------------------------
import sys

inpath = "C:\\Users\\Sara\\Desktop\\Upload\\UStar.stl"
outpath = "C:\\Users\\Sara\\Desktop\\Upload\\UTrans.obj"

# import stl
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)
	
# choose texture, texName = 'UmatrixTexture' oder 'Pmatrix Texture'
def initColor(texName):
    mat = bpy.data.materials.new("newMaterial")
    bpy.context.object.active_material = mat
    tex = bpy.data.textures.get(texName)
    bpy.context.object.active_material.active_texture = tex

    # richtig Positionieren
    bpy.context.object.active_material.texture_slots[0].texture_coords = 'ORCO'
    bpy.context.object.active_material.texture_slots[0].mapping_x = 'Z'
    bpy.context.object.active_material.texture_slots[0].mapping_y = 'Z'


# TODO: size = new size - old size?
# Bodenfärbung anpassen
def setSizeAndOffset (size,offset):
    bpy.context.object.active_material.texture_slots[0].scale[1] = size
    bpy.context.object.active_material.texture_slots[0].offset[1] = offset


def mapAndExport(outpath):
    # UV Mapping erstellen
    bpy.ops.uv.smart_project(island_margin=1)
    # stelle sicher, dass nicht in Editmode
    bpy.ops.object.mode_set(mode='OBJECT')
    # erstelle und verlinke image (-> später höhere Auflösung?)
    image = bpy.data.images.new(name="UTrans", width=1000, height=1000)
    for uv_face in bpy.data.objects.get("UStar").data.uv_textures.active.data:
        uv_face.image = image
    # Rückkehr in Editmode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT') # Notwendig?
    #bake
    bpy.ops.object.bake_image()
    # save image
    bpy.data.images['UTrans'].filepath_raw = "C:\\Users\\Sara\\Desktop\\Upload\\UTrans.png"
    bpy.data.images['UTrans'].file_format = 'PNG'
    bpy.data.images['UTrans'].save()
    # save object
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')


# vollständige Färbung
def color(inpath,outpath,texName,mode,size = 1.63, offset = 0.15):
    initialize(inpath)
    initColor(texName)
    setSizeAndOffset(size,offset)
    mapAndExport(outpath)


if __name__ == "__main__":
    if sys.argv[8] == 0: # Färben ohne size und offset
        color(sys.argv[5],sys.argv[6],sys.argv[7])
    else:
        color(sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[9],sys.argv[10])
