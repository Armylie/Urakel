# Verwaltet verschiedene Methoden zur Grundtransformation der .stl Datei

import bpy # Fehler kann erstmal ignoriert werden, löst sich zur Laufzeit
import sys

# clear workspace and import .stl (from inpath)
def initialize(inpath):
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_mesh.stl(filepath=inpath)

def center(dimx,dimy):
    bpy.context.object.location[0] = -dimx/2
    bpy.context.object.location[1] = -dimy/2

# subdivide the mesh numdiv times, and smooth the mesh numsmooth times
def smooth(numdiv, numsmooth):
    bpy.ops.object.editmode_toggle() # choose all points
    for i in range(numdiv):
        bpy.ops.mesh.subdivide()
    bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=numsmooth)

# generate base of the height given in height, dimz needs to be the height without base
def buildbase(height,dimz):
    bpy.ops.mesh.extrude_region_move() # copy all points
    bpy.ops.transform.resize(value=(1, 1, 0)) # move to one level
    bpy.ops.transform.translate(value=(0,0,-dimz/2)) # move to z = 0
    bpy.ops.transform.translate(value=(0, 0, -height)) # generate base of the height height (below z = 0)

# complete transformation
def transform(inpath,outpath,numdiv = 2, numsmooth = 2):
    initialize(inpath)
    dims =  bpy.context.object.dimensions # [x,y,z] dimension
    #center(dims[0],dims[1])
    smooth(numdiv,numsmooth)
    buildbase(dims[2]/4,dims[2]) # ratio of total height and base can be changed (in consequence offset and layerwidth need to be adjusted)
    bpy.ops.export_mesh.stl(filepath=outpath)


if __name__ == "__main__":
    transform(sys.argv[5],sys.argv[6],numdiv = int (sys.argv[7]))
