import os
import csv

# öffnen der 'Datenbank'
# TODO: öffnen über relativen Pfad
with open('C:\\Users\\Sara\\Desktop\\Neuer Ordner\\Urakel\\app\\paths.txt') as file:
    data = eval(file.read())

# Pfade welche vom User am Anfang abgefragt werden (oder bei Installation des Programms gesetzt werden)
blenderpath = data.get('BLENDERPATH')
texpath = data.get('TEXTUREPATH')
savepath = data.get('SAVEPATH')

# Pfade für entsprechende Pythondateien öffnen, in richtigem Format um durch Blender genutzt zu werden
trafopath = "\"" + __file__.replace('Main', 'Trafo').replace('/', '\\') + "\""
scalepath = "\"" + __file__.replace('Main', 'Scale').replace('/', '\\') + "\""
colorpath = "\"" + __file__.replace('Main', 'Color').replace('/', '\\') + "\""
pcolorpath = "\"" + __file__.replace('Main', 'political_coloring').replace('/', '\\') + "\""


# Pfade welcher vom User auf erster Maske abgefragt wird
# stehen hier nur zum einfacheren testen (ohne UI)
# inpath = "\"C:\\Users\\Sara\\Desktop\\Upload\\UStar.stl\""
# islandpath = "\"C:\\Users\\Sara\\Desktop\\Upload\\island.txt\""


# Reihenfolge der Übergebenen Argumente: inpath outpath quality
def trans(arguments):
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background --python " + trafopath + " -- " + argument_string)


# Reihenfolge der Übergebenen Argumente: inpath, outpath, Modus, Koordinaten (X,Y,Z / Z / X)
# Modi: 0 - alle Dimensionen ; 1 - Rückgabe der aktuellen Dimension
def scale(arguments):
    open(savepath + '\\dim.csv', 'w').close()  # Datei erzeugen/leeren um X,Y,Z Werte speichern zu können
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background --python " + scalepath + " -- " + argument_string)
    with open(savepath + '\\dim.csv', 'r') as file:
        for row in csv.reader(file):  # es gibt nur eine row
            return [float(x) for x in row]
            # -> Rückgabe der neuen Größe


# Reihenfolge der Übergebenen Argumente: inpath outpath texName mode size offset
# mode: 0 - Färben ohne size und offset, 1 - mit Parametern
# wichtig: outpath = inpath.replace('.stl', '_trans.obj')
def color_geographic(arguments):
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background " + texpath + " --python " + colorpath + " -- " + argument_string)


# Reihenfolge der Übergebenen Argumente: inpath outpath islandpath
# wichtig: outpath = inpath.replace('.stl', '_trans.obj')
def color_political(arguments):
    argument_string = " ".join(arguments)
    os.chdir(blenderpath)
    os.system("blender --background --python " + pcolorpath + " -- " + argument_string)


