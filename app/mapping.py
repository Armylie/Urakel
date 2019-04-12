from numpy import genfromtxt, zeros, savetxt
import numpy as np

# paths to the right files need to be changed by the user of this script

# contains datapoints and corresponding classes
clustering = genfromtxt('36DresdenAlldataMDSn106d40AUclusterung.cls', skip_header=2, dtype=int)
# contains datapoints and corresponding coordinates
points = genfromtxt('31DresdenAlldataMDSn106d40.bm', skip_header=2, dtype=int)
# contains representation of the island (island = 0)
island = genfromtxt('31DresdenAlldataMDSn106d40Island.imx', skip_header=1, dtype=int)

# generates a new multidimensional list of [datapoint, x coordinate, y coordinate, class]
def mergePointsAndCluster(points, clustering):
    res = zeros([len(points), 4])
    for i in range(len(points)):
        res[i] = [points[i, 0], points[i, 1], points[i, 2], clustering[i, 1]]
    return res

# generates new representation of the island (switch ones and zeros so the ones encode the island)
def switchIsland(island):
    for i in range(len(island)):
        for j in range(len(island[0])):
            island[i,j] = (island[i,j]==0)


# substitute ones (island) by classes (+1 to prevent conflicts with the ones that encode the island)
def clusterIsland(cluster, island):
    x_length = int(len(island)/2)
    y_length = int(len(island[0])/2)
    # for each datapoint find the point in one of the quadrants that belongs to the island
    for p in cluster:
        x,y = int(p[1]) -1, int(p[2]) -1
        if island[x, y] == 1:
            island[x, y] = p[3] +1
        elif island[x_length + x, y] == 1:
            island[x_length + x, y] = p[3] +1
        elif island[x, y_length +y] == 1:
            island[x, y_length + y] = p[3] +1
        elif island[x_length + x, y_length + y] == 1:
            island[x_length + x, y_length + y] = p[3] +1
        else: # just in case of error
            print(p)
            print(x_length + x, y_length + y)

# delete border area (-> so only the island remains)
def cutIsland(island):
    deleter,deletec = [],[]
    tisland = island.transpose()
    # mark rows of zeros
    for x in range(len(island)):
        if np.count_nonzero(island[x]) == 0:
            deleter.append(x)
    # mark columns of zeros
    for x in range(len(tisland)):
        if np.count_nonzero(tisland[x]) == 0:
            deletec.append(x)
    # delete marked rows and columns
    island = np.delete(island, deleter, axis=0)
    island = np.delete(island, deletec, axis=1)
    return island

# fill the sparse island with classes
def fillCluster(island):
    island2 = island.copy()
    # classify a direct circle around each classified datapoint -> leads to a better connection between classes
    for x in range(len(island)):
        for y in range(len(island[0])):
            if island[x,y] > 1:
                for i in [max(0,x-1),x,min(x+1,len(island)-1)]:
                    for j in [max(0,y-1),y,min(y+1,len(island[0])-1)]:
                        island2[i,j] = island[x,y]
    c = 1
    island = island2
    # fill to the right
    for x in range(len(island)):
        for y in range(len(island[0])):
            c = fill(island, x, y, c)
    # fill down
    for y in range(len(island[0])):
        for x in range(len(island)):
            c = fill(island, x, y, c)
    # fill to the left
    for x in range(len(island)):
        for y in range(len(island[0]) - 1, -1, -1):
            c = fill(island, x, y, c)
    # fill up
    for y in range(len(island[0])):
        for x in range(len(island)-1,-1,-1):
            c = fill(island,x,y,c)
    return island

# changes point at (x,y) in island in the correct way for class c
def fill(island,x,y,c):
    if island[x, y] == 1: # set class
        island[x, y] = c
    elif island[x, y] == 0: # space between the island resets the class
        c = 1
    elif island[x, y] > 0: # update class
        c = island[x, y]
    return c


switchIsland(island)
res = mergePointsAndCluster(points, clustering)
clusterIsland(res, island)
island = cutIsland(island)
island = fillCluster(island)


# save mapping as textfile
savetxt('island.txt', island, fmt='%d')



