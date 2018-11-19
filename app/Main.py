import os
# TODO: from app import Trafo , wenn Lösung für bpy import gefunden

#print(Trafo.__file__)  --> im Idealfall verwenden als Trafopath

# Pfade welche vom User am Anfang abgefragt werden (oder bei Installation des Programms gesetzt werden)
blenderpath = "C:\\Program Files\\Blender Foundation\\Blender"
trafopath = "\"C:\\Users\\Sara\\Desktop\\Urakel\\app\\Trafo.py\""
scalepath = "\"C:\\Users\\Sara\\Desktop\\Urakel\\app\\Scale.py\""

# Pfad welcher vom User an passender Stelle (vor Transformation) abgefragt wird
inpath = "\"C:\\Users\\Sara\\Desktop\\Upload\\UStar.stl\""


# Reihenfolge der Übergebenen Argumente: inpath outpath numdiv numsmooth height
def trans(arguments):
    argument_string = ""
    for a in range(len(arguments)):
        argument_string += arguments[a] + " "
    os.chdir(blenderpath)
    os.system("blender --background --python " + trafopath + " -- " + argument_string)

def scale(arguments):
    argument_string = ""
    for a in range(len(arguments)):
        argument_string += arguments[a] + " "
    os.chdir(blenderpath)
    os.system("blender --background --python " + scalepath + " -- " + argument_string)

# zu Testzwecken, ab finaler Verwendung über Anwendung nicht mehr benötigt
if __name__ == "__main__":
    outpath = inpath.replace('.stl','_trans.stl')
    #trans([inpath,outpath])
    scale(['0','5','5','5',inpath,outpath])