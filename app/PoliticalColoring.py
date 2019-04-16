import numpy as np
import bpy
import sys
import os

# clear workspace and import .stl (from inpath)
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    #bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

# generate materials for 8 potential classes (+ bordercolor)
def create_mats():
    # colors from the cholor scheme tab10
    color = [(0.12, 0.47, 0.71), (1.0, 0.5, 0.05), (0.17, 0.63, 0.17), (0.84, 0.15, 0.16), (0.58, 0.40, 0.74),
             (0.89, 0.47, 0.76), (0.74, 0.74, 0.13),(0.09, 0.75, 0.81),(0.5,0.5,0.5)]

    for i in range(9):
        mat = bpy.data.materials.new('Material'+str(i))
        bpy.context.active_object.data.materials.append(mat)
        mat.diffuse_color = color[i]


# if island[x,y] belongs to class c, color polygons between node x, x+1 and y,y+1
# this function marks the polygons for class c
# div = 1
def markPolygons(island,c,div):
    a = 0
    # ignore last column/row, (mapping given von x nodes, we have x-1 vertexes)
    for x in range(len(island)-1):
        for y in range(len(island[0])-1):
            if island[x,y] >= c: # get clean (not blue) edges by coloring in ascending order
                # two triangles for each datapoint in mapping
                bpy.context.active_object.data.polygons[a].select = True
                bpy.context.active_object.data.polygons[a+1].select = True
            a = a + 2
    if div > 1: # more subdivisions lead to more polygons and a more complicated marking
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


# color cluster i of island (with div times subdivision) (cluster 0 corresponds to the border)
def colorOne(island, i,div):
    markPolygons(island, i,div)
    bpy.ops.object.editmode_toggle()
    # choose and assign the right material
    bpy.context.object.active_material_index = i
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='TOGGLE') # deselect all polygons
    bpy.ops.object.editmode_toggle() # for marking further polygons we need to be outside of the editmode


# complete coloring of the matrix at inpath with a mapping from islandpath (saving at outpath)
# div corresponds to the number of subdivisions
def color(inpath,outpath,islandpath,div=1):
    island = np.genfromtxt(islandpath, dtype=int) # textfile as np array
    classes = findNumbers(island)
    initialize(inpath)
    create_mats()
    # color all classes
    for i in classes:
       colorOne(island,i,div)
    # render image of colored matrix to be displayed at UI
    bpy.data.scenes['Scene'].render.filepath = __file__.replace('PoliticalColoring.py', os.path.join('static', ''))
    bpy.ops.render.render(animation=True)
    # export files (no image needed, oly .obj and .mtl, because no use of texture)
    bpy.ops.export_scene.obj(filepath = outpath,path_mode='ABSOLUTE')


# find all numbers in X (X is list of lists of ints)
def findNumbers (X):
    c = []
    for i in range(X.min(),X.max()+1):
        if X.__contains__(i):
            c.append(i)
    return c


if __name__ == "__main__":
    color(sys.argv[6],sys.argv[7],sys.argv[8],int(sys.argv[9]))









