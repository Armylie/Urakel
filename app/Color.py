#--------------------------------------------------------------------
# Allgemein: ob = bpy.data.objects.get("UStar")  statt bpy.context.object
#--------------------------------------------------------------------

# kopiere folgenden Code in die Blender Python Konsole um die Matrix einzufärben

inpath = "C:\\Users\\Sara\\Desktop\\Upload\\UStar.stl"

# import stl

bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_mesh.stl(filepath=inpath)
	
# choose texture
mat = bpy.data.materials.new("newMaterial")
bpy.context.object.active_material = mat
tex = bpy.data.textures.get('UmatrixTexture')
bpy.context.object.active_material.active_texture = tex

# richtig Positionieren
bpy.context.object.active_material.texture_slots[0].texture_coords = 'ORCO'
bpy.context.object.active_material.texture_slots[0].mapping_x = 'Z'
bpy.context.object.active_material.texture_slots[0].mapping_y = 'Z'

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
bpy.ops.export_scene.obj(filepath = "C:\\Users\\Sara\\Desktop\\Upload\\UTrans.obj",path_mode='ABSOLUTE')
