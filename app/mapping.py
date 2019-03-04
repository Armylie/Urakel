from numpy import genfromtxt, zeros, savetxt
import numpy as np

# enthält Datenpunkte und zugehörige Klasse
clustering = genfromtxt('36DresdenAlldataMDSn106d40AUclusterung.cls', skip_header=2, dtype=int)
# enthält Datenpunkte und Koordinaten
points = genfromtxt('31DresdenAlldataMDSn106d40.bm', skip_header=2, dtype=int)
# enthält Darstellung der Insel
island = genfromtxt('31DresdenAlldataMDSn106d40Island.imx', skip_header=1, dtype=int)

# erstelle ein neues Array: Datenpunkt, x Koordinate, y Koordinate, Klasse
def mergePointsAndCluster(points, clustering):
    res = zeros([len(points), 4])
    for i in range(len(points)):
        res[i] = [points[i, 0], points[i, 1], points[i, 2], clustering[i, 1]]
    return res

# stelle Insel durch 1en, Rand duch 0en dar
def switchIsland(island):
    for i in range(len(island)):
        for j in range(len(island[0])):
            island[i,j] = (island[i,j]==0)


# ersetze 1 (Insel) durch Klassenbezeichnung (+1 da sonst Konflikte mit Inseldarstellung durch 1
def clusterIsland(cluster, island):
    x_length = int(len(island)/2)
    y_length = int(len(island[0])/2)
    for p in cluster:
        x,y = int(p[1]) -1, int(p[2]) -1 # Indizierung in Tabelle beginnt bei 1
        if island[x, y] == 1:
            island[x, y] = p[3] +1
        elif island[x_length + x, y] == 1:
            island[x_length + x, y] = p[3] +1
        elif island[x, y_length +y] == 1:
            island[x, y_length + y] = p[3] +1
        elif island[x_length + x, y_length + y] == 1:
            island[x_length + x, y_length + y] = p[3] +1
        else:
            print(p)
            print(x_length + x, y_length + y)

# entferne reine Außenbereiche (-> erhalte zugeschnittene Insel)
def cutIsland(island):
    deleter,deletec = [],[]
    tisland = island.transpose()
    # Nullzeilen löschen
    for x in range(len(island)):
        if np.count_nonzero(island[x]) == 0:
            deleter.append(x)
    # Nullzeilen löschen
    for x in range(len(tisland)):
        if np.count_nonzero(tisland[x]) == 0:
            deletec.append(x)
    island = np.delete(island, deleter, axis=0)
    island = np.delete(island, deletec, axis=1)
    return island

# fülle die Insel mit Klassenbezeichnungen auf
def fillCluster(island):
    island2 = island.copy()
    # klassifiziere direkten Kreis um klassifizierten Punkt -> für bessere Verbundenheit von Klassen
    for x in range(len(island)):
        for y in range(len(island[0])):
            if island[x,y] > 1:
                for i in [max(0,x-1),x,min(x+1,len(island)-1)]:
                    for j in [max(0,y-1),y,min(y+1,len(island[0])-1)]:
                        island2[i,j] = island[x,y]
    c = 1
    island = island2
    # fülle Werte nach rechts auf
    for x in range(len(island)):
        for y in range(len(island[0])):
            c = fill(island, x, y, c)
    # fülle Werte nach unten auf
    for y in range(len(island[0])):
        for x in range(len(island)):
            c = fill(island, x, y, c)
    # fülle Werte nach links auf
    for x in range(len(island)):
        for y in range(len(island[0]) - 1, -1, -1):
            c = fill(island, x, y, c)
    # fülle Werte nach oben auf
    for y in range(len(island[0])):
        for x in range(len(island)-1,-1,-1):
            c = fill(island,x,y,c)
    return island

# Hilfsfunktion -> ändert Zahl in Mapping entsprechend der Klasse/ ändert aktuelle Klasse c
def fill(island,x,y,c):
    if island[x, y] == 1:
        island[x, y] = c
    elif island[x, y] == 0:
        c = 1
    elif island[x, y] > 0:
        c = island[x, y]
    return c



res = mergePointsAndCluster(points, clustering)
switchIsland(island)
clusterIsland(res, island)
island = cutIsland(island)
island = fillCluster(island)

# speichere Mapping in Textdatei
savetxt('island.txt', island, fmt='%d')



