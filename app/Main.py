import os
import csv
# TODO: from app import Trafo , wenn Lösung für bpy import gefunden

#print(Trafo.__file__)  --> im Idealfall verwenden als Trafopath damit kein absoluter Pfad mehr übergeben werden muss

# Pfade welche vom User am Anfang abgefragt werden (oder bei Installation des Programms gesetzt werden)
blenderpath = "C:\\Program Files\\Blender Foundation\\Blender"
trafopath = "\"C:\\Users\\Sara\\Desktop\\Neuer Ordner\\Urakel\\app\\Trafo.py\""
scalepath = "\"C:\\Users\\Sara\\Desktop\\Neuer Ordner\\Urakel\\app\\Scale.py\""

# Pfad welcher vom User auf erster Maske abgefragt wird
# steht hier nur zum einfacheren testen (ohne UI)
inpath = "\"C:\\Users\\Sara\\Desktop\\Upload\\UStar.stl\""


# Reihenfolge der Übergebenen Argumente: inpath outpath numdiv numsmooth height
# TODO: Nope inpath outpath quality -> numdiv und numsmooth für verschiedene Qualitäten festlegen
def trans(arguments):
    argument_string = ""
    for a in range(len(arguments)):
        argument_string += arguments[a] + " "
    os.chdir(blenderpath)
    os.system("blender --background --python " + trafopath + " -- " + argument_string)

# Reihenfolge der Übergebenen Argumente: inpath, outpath, Modus, Koordinaten (X,Y,Z / Z / X)
# Modi: 0 - alle Dimensionen ; 1 - nur Höhe ; 2 - Boden ändern, skaliert ; 3 - Rückgabe der aktuellen Dimension
def scale(arguments):
    open('C:\\Users\\Sara\\Desktop\\Upload\\dim.csv', 'w').close()  # Datei erzeugen/leeren um X,Y,Z Werte speichern zu können
    argument_string = ""
    for a in range(len(arguments)):
        argument_string += arguments[a] + " "
    os.chdir(blenderpath)
    os.system("blender --background --python " + scalepath + " -- " + argument_string)
    with open('C:\\Users\\Sara\\Desktop\\Upload\\dim.csv','r') as file:
        for row in csv.reader(file): # es gibt nur eine row
            return [float(x) for x in row]
            # -> Rückgabe der neuen Größe

# zu Testzwecken, ab finaler Verwendung über Anwendung nicht mehr benötigt
if __name__ == "__main__":
    outpath = inpath.replace('.stl','_trans.stl')
    #trans([inpath,outpath])
    print(scale([inpath, outpath,'3','5','5','5']))