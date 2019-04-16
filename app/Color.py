#--------------------------------------------------------------------
# Allgemein: ob = bpy.data.objects.get("UStar")  statt bpy.context.object
#--------------------------------------------------------------------
import sys
import os
import bpy


# clear workspace and import .stl (from inpath)
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    #bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)
	
# choose texture, texName = 'UmatrixTexture' or 'Pmatrix Texture'
def initColor(texName):
    mat = bpy.data.materials.new("newMaterial")
    bpy.context.object.active_material = mat
    tex = bpy.data.textures.get(texName)
    bpy.context.object.active_material.active_texture = tex

    # find right position
    bpy.context.object.active_material.texture_slots[0].texture_coords = 'ORCO'
    bpy.context.object.active_material.texture_slots[0].mapping_x = 'Z'
    bpy.context.object.active_material.texture_slots[0].mapping_y = 'Z'


# adjust coloring of the ground
def setSizeAndOffset (size,offset):
    bpy.context.object.active_material.texture_slots[0].scale[1] = size
    bpy.context.object.active_material.texture_slots[0].offset[1] = offset



def mapAndExport(outpath,resolution = 10000):
    # generate UV-mapping
    bpy.ops.uv.smart_project(island_margin=1)
    # ensure mode != EDIT
    bpy.ops.object.mode_set(mode='OBJECT')
    # generate and link image
    # resolution (here 10000x10000) may be changed
    image = bpy.data.images.new(name="Matrix", width=resolution, height=resolution)
    for uv_face in bpy.data.objects.get("Matrix").data.uv_textures.active.data:
        uv_face.image = image
    bpy.data.materials["newMaterial"].use_shadeless = True
    # return to editmode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT') # Notwendig?
    #bake
    bpy.ops.object.bake_image()
    # save image
    bpy.data.images['Matrix'].filepath_raw = __file__.replace('Color.py', os.path.join('Temp','Matrix.png'))
    bpy.data.images['Matrix'].file_format = 'PNG'
    bpy.data.images['Matrix'].save()
    # render image of colored matrix to be displayed at UI
    bpy.data.scenes['Scene'].render.filepath = __file__.replace('Color.py', os.path.join('static',''))
    bpy.ops.render.render(animation=True)
    # save object
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')


# complete coloring
def color(inpath,outpath,texName,size,offset,div):
    initialize(inpath)
    initColor(texName)
    setSizeAndOffset(size,offset)
    resolution = [2000,2000,2000]
    mapAndExport(outpath,resolution[div-1])


if __name__ == "__main__":
    color(sys.argv[6],sys.argv[7],sys.argv[8],float(sys.argv[9]),float(sys.argv[10]),int(sys.argv[11]))
