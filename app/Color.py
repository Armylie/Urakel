#--------------------------------------------------------------------
# Allgemein: ob = bpy.data.objects.get("UStar")  statt bpy.context.object
#--------------------------------------------------------------------
import sys
import bpy


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
    image = bpy.data.images.new(name="Matrix", width=10000, height=10000)
    for uv_face in bpy.data.objects.get("Matrix").data.uv_textures.active.data:
        uv_face.image = image
    bpy.data.materials["newMaterial"].use_shadeless = True
    # Rückkehr in Editmode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT') # Notwendig?
    #bake
    bpy.ops.object.bake_image()
    # save image
    bpy.data.images['Matrix'].filepath_raw = __file__.replace('Color.py','Temp\\Matrix.png')
    bpy.data.images['Matrix'].file_format = 'PNG'
    bpy.data.images['Matrix'].save()
    # save object
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')


# vollständige Färbung
def color(inpath,outpath,texName,size,offset):
    initialize(inpath)
    initColor(texName)
    setSizeAndOffset(size,offset)
    mapAndExport(outpath)


if __name__ == "__main__":
    color(sys.argv[6],sys.argv[7],sys.argv[8],float(sys.argv[9]),float(sys.argv[10]))
