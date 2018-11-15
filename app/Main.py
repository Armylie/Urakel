import os
# TODO: from app import Trafo , wenn Lösung für bpy import gefunden

#print(Trafo.__file__)  --> im Idealfall verwenden als Trafopath

# Pfade welche vom User am Anfang abgefragt werden (oder bei Installation des Programms gesetzt werden)
blenderpath = "C:\\Program Files\\Blender Foundation\\Blender"
trafopath = "\"C:\\Users\\Sara\\Desktop\\Uni Marburg\\Jahresprojekt\\urakel_benny_sara\\app\\Trafo.py\""

# Pfad welcher vom User an passender Stelle (vor Transformation) abgefragt wird
inpath = "\"C:\\Users\\Sara\\Desktop\\Uni Marburg\\Jahresprojekt\\UStar.stl\""


# Reihenfolge der Übergebenen Argumente: inpath outpath numdiv numsmooth height
def trans(arguments):
    argument_string = ""
    for a in range(len(arguments)):
        argument_string += arguments[a] + " "
    print(argument_string)
    os.chdir(blenderpath)
    os.system("blender --background --python " + trafopath + " -- " + argument_string)

# zu Testzwecken, ab finaler Verwendung über Anwendung nicht mehr benötigt
if __name__ == "__main__":
    outpath = inpath.replace('.stl','_trans.stl')
    trans([inpath,outpath])