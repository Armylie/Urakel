import os
import csv

# open 'database'
with open(__file__.replace('Main.py','paths.txt')) as file:
    data = eval(file.read())

# path of the users Blender version (needs to be written in 'paths.txt' at installation)
blenderpath = data.get('BLENDERPATH')
# path to environment for texturing
texpath = __file__.replace('Main.py','Texturierungsumgebung.blend')

# paths for different pythonfiles to be opened in Blender
trafopath = "\"" + __file__.replace('Main', 'Trafo').replace('/', '\\') + "\""
scalepath = "\"" + __file__.replace('Main', 'Scale').replace('/', '\\') + "\""
colorpath = "\"" + __file__.replace('Main', 'Color').replace('/', '\\') + "\""
pcolorpath = "\"" + __file__.replace('Main', 'political_coloring').replace('/', '\\') + "\""


# order of submitted arguments: [inpath, outpath, quality]
def trans(arguments):
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background --python " + trafopath + " -- " + argument_string)


# order of submitted arguments: [inpath, outpath, modus, X, Y, Z]
# Modi: 0 - change all dimensions ; 1 - return current dimensions
def scale(arguments):
    open(__file__.replace('Main.py', 'Temp\\dim.csv'), 'w').close()  # generate/clear file for saving X,Y,Z values
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background --python " + scalepath + " -- " + argument_string)
    with open(__file__.replace('Main.py', 'Temp\\dim.csv'), 'r') as file:
        for row in csv.reader(file):  # only one row
            return [float(x) for x in row]
            # -> return new dimensions


# order of submitted arguments: [inpath, outpath, texName, size, offset]
# important: outpath needs to be .obj
def color_geographic(arguments):
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background " + texpath + " --python " + colorpath + " -- " + argument_string)


# order of submitted arguments: [inpath, outpath, islandpath, div]
# important outpath needs to be .obj
def color_political(arguments):
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background --python " + pcolorpath + " -- " + argument_string)


