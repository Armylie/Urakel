def changeDim(X,Y,Z):
    bpy.context.object.dimensions[0] = X
    bpy.context.object.dimensions[1] = Y
    bpy.context.object.dimensions[2] = Z

def changeHeight(Z):
    bpy.context.object.dimensions[2] = Z
    
def changeScaled(X):
    bpy.context.object.dimensions[0] = X
    # TODO: get oldX Dimension, get oldY Dimension
    # Y = oldY/oldX * X
    bpy.context.object.dimension[1] = Y