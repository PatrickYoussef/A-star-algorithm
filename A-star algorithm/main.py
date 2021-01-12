import math
from collections import defaultdict
from datetime import time

import shapefile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time



# ----------------------------------------------------
# Assignment 1
# Written by Patrick Youssef 40098029
# For COMP 472 Section - Summer 2020
# ----------------------------------------------------


# read our file
sf = shapefile.Reader("Shape/crime_dt", encoding="ISO-8859-1")

# set the boundaries of our section
x1 = sf.bbox[0]
x2 = sf.bbox[2]
y1 = sf.bbox[1]
y2 = sf.bbox[3]
print("x coordinate of starting point: " + str(x1))
print("y coordinate of starting point: " + str(x2))
print("x coordinate of end point: " + str(y1))
print("y coordinate of end point: " + str(y2))

#  prompt the user
threshold = float(input("What is the threshold? (Enter a value from 1 - 100): "))
size = float(input("What is the size? ex: 0.002: "))
start_point_X = float(input("What is the x coordinate of your starting point?"))
start_point_Y = float(input("What is the y coordinate of your starting point?"))
end_point_X = float(input("What is the x coordinate of your end point?"))
end_point_Y = float(input("What is the y coordinate of your end point?"))
beginningPoint = [start_point_X, start_point_Y]
finishPoint = [end_point_X, end_point_Y]

start_time = time.time()

# read the records and coordinates of each crime
coordinates = []  # all records read by the fil
records = []  # name of the crimes
xPoints = []
yPoints = []
crimeData = dict()  # hash map of the number of crimes at each coordinates

shapeRecords = sf.shapeRecords()
shapes = sf.shapes()

#  create arrays that holds all the points, x and y of the crimes data
for i in range(len(shapeRecords)):
    coordinates.append(shapes[i].points[0])
    xPoints.append(shapes[i].points[0][0])
    yPoints.append(shapes[i].points[0][1])

#  create a new array that holds the crime points only ome time
newCoordinates = []
for i in coordinates:
    if i not in newCoordinates:
        newCoordinates.append(i)

for i in range(len(newCoordinates)):
    count = 0
    for j in range(len(coordinates)):
        if newCoordinates[i] == coordinates[j]:
            count = count + 1
    crimeData[str(newCoordinates[i])] = count

rows, cols = (int(np.ceil((x2 - x1) / size)), int(np.ceil((y2 - y1) / size)))
crimes = np.array([[0] * rows] * cols)
xStart = x1
yStart = y1
max_num_of_crimes = 0
#  setCrimes = []

for i in range(len(coordinates)):
    x = int(np.floor((xPoints[i] - xStart) / size))
    y = int(np.floor((yPoints[i] - yStart) / size))

    crimes[x, y] += 1
    if crimes[x][y] > max_num_of_crimes:
        max_num_of_crimes = crimes[x][y]

# calculate total count, mean, standard deviation, median
totalCount = len(coordinates)
median = np.median(crimes)
standard_dev = np.std(crimes)
mean = np.mean(crimes)

#  create a new array that shows which grids are below the median, and which one are not
medianCheck = np.array([[0] * rows] * cols)
percentile = np.percentile(crimes, threshold)
for i in range(0, len(medianCheck)):
    for j in range(0, len(medianCheck)):
        if crimes[i][j] >= percentile:
            medianCheck[i][j] = 1  # yellow
        else:
            medianCheck[i][j] = 0  # purple


#  get all the neighbors he can go to
def getNeighbors(point):
    neighbors = []

    x = point[0]
    y = point[1]

    up = y + 1
    down = y - 1
    left = x - 1
    right = x + 1

    if x == y == 0:  # node in the corner has 3 neighbors
        if medianCheck[x][y] == 0:
            neighbors.append((right, up))

    elif x == (rows - 1) and y == 0:
        if medianCheck[left][x] == 0:
            neighbors.append((left, up))

    elif x == 0 and y == (cols - 1):
        if medianCheck[x][down] == 0:
            neighbors.append((right, down))

    elif x == (rows - 1) and y == (cols - 1):
        if medianCheck[left, down] == 0:
            neighbors.append((left, down))

    elif (0 < x < (rows - 1)) and y == 0:
        if medianCheck[left][x] == 0:
            neighbors.append((left, up))
        if medianCheck[x][y] * medianCheck[left][y] == 0:
            neighbors.append((x, up))
        if medianCheck[x][y] == 0:
            neighbors.append((right, up))

    elif (0 < x < (rows - 1)) and y == (cols - 1):
        if medianCheck[left, down] == 0:
            neighbors.append((left, down))
        if medianCheck[x][down] * medianCheck[left][down] == 0:
            neighbors.append((x, down))
        if medianCheck[x][down] == 0:
            neighbors.append((right, down))

    elif x == 0 and (0 < y < (cols - 1)):
        if medianCheck[x][y] == 0:
            neighbors.append((right, up))
        if medianCheck[x][y] * medianCheck[x][down] == 0:
            neighbors.append((right, y))
        if medianCheck[x][down] == 0:
            neighbors.append((right, down))

    elif x == (rows - 1) and (0 < y < (cols - 1)):
        if medianCheck[left][x] == 0:
            neighbors.append((left, up))
        if medianCheck[left, y] * medianCheck[left, down] == 0:
            neighbors.append((left, y))
        if medianCheck[left, down] == 0:
            neighbors.append((left, down))
        #  neighbors = [(x, up), (left, up), (left, y), (left, down), (x, down)]

    else:
        if medianCheck[x][y] * medianCheck[left][y] == 0:
            neighbors.append((x, up))
        if medianCheck[x][y] == 0:
            neighbors.append((right, up))
        if medianCheck[x][y] * medianCheck[x][down] == 0:
            neighbors.append((right, y))
        if medianCheck[x][down] == 0:
            neighbors.append((right, down))
        if medianCheck[x][down] * medianCheck[left][down] == 0:
            neighbors.append((x, down))
        if medianCheck[left, down] == 0:
            neighbors.append((left, down))
        if medianCheck[left, y] * medianCheck[left, down] == 0:
            neighbors.append((left, y))
        if medianCheck[left][y] == 0:
            neighbors.append((left, up))
        #  neighbors = [(x, up), (right, up), (right, y), (right, down), (x, down), (left, down), (left, y),(left, up)]
    return neighbors


left_start_x = int(np.floor((start_point_X - xStart) / size))
left_start_y = int(np.floor((start_point_Y - yStart) / size))
left_end_x = int(np.floor((end_point_X - xStart) / size))
left_end_y = int(np.floor((end_point_Y - yStart) / size))


#  get the cost of a move
def getCost(point, final):
    x_start = point[0]
    y_start = point[1]
    x_end = final[0]
    y_end = final[1]

    if np.abs(x_start - x_end) == 1 and np.abs(y_start - y_end) == 1:
        return 1.5

    if x_start == x_end and y_end - y_start == 1:
        if medianCheck[x_start][y_start] == 1:
            return 1.3
        else:
            if medianCheck[x_start - 1][y_start] == 1:
                return 1.3
            else:
                return 1

    if x_start == x_end and y_start - y_end == 1:
        if medianCheck[x_end][y_end] == 1:
            return 1.3
        else:
            if medianCheck[x_start - 1][y_start - 1] == 1:
                return 1.3
            else:
                return 1

    if y_start == y_end and x_start - x_end == 1:
        if medianCheck[x_end][y_end] == 1:
            return 1.3
        else:
            if medianCheck[x_end][y_end - 1] == 1:
                return 1.3
            else:
                return 1

    if y_start == y_end and x_end - x_start == 1:
        if medianCheck[x_start][y_start] == 1:
            return 1.3
        else:
            if medianCheck[x_start][y_start - 1] == 1:
                return 1.3
            else:
                return 1


#  A star algorithm
def Astar(beginning, finish):
    g = defaultdict(lambda: float("inf"))
    g[beginning] = 0

    def h(n):
        return np.sqrt(np.power(np.absolute(finish[0] - n[0]), 2) + np.power(np.absolute(finish[1] - n[1]), 2))

    f = defaultdict(lambda: float("inf"))
    f[beginning] = h(beginning)

    open_list = [beginning]

    ancestors = {}

    while open_list:
        bestF = math.inf
        node = None
        for point in open_list:
            if f[point] < bestF:
                bestF = f[point]
                node = point

        if node == finish:
            return build(ancestors, node)

        open_list.remove(node)
        neighbor = getNeighbors(node)

        for neigh in neighbor:
            start_node = getCost(node, neigh) + g[node]

            if start_node < g[neigh]:

                ancestors[neigh] = node
                g[neigh] = start_node
                f[neigh] = g[neigh] + h(neigh)

                if neigh not in open_list:
                    open_list.append(neigh)
    return None


#  creates an array that returns the path
def build(ancestors, node):
    route = [node]
    while node in ancestors.keys():
        node = ancestors[node]
        route.insert(0, node)
    return route


#  get the path according to the A* algo
path = Astar((left_start_x, left_start_y), (left_end_x, left_end_y))

#   PLOT THE GRAPH
fig, ax = plt.subplots()
plt.setp(ax.get_xticklabels(), rotation=30, horizontalAlignment="right")

extent = [x1, x2, y1, y2]
if threshold == 100:
    colors = mcolors.ListedColormap(['purple', 'purple'])
else:
    colors = mcolors.ListedColormap(['purple', 'yellow'])
norm = mcolors.BoundaryNorm([0, np.percentile(crimes, threshold), max_num_of_crimes], colors.N)
im = ax.imshow(crimes.transpose(), aspect="auto", origin="lower", cmap=colors, norm=norm, extent=extent)

plt.title("Threshold: " + str(threshold) + "%\n" + "Median: " + str(median) + " - Standard deviation: "
          + str(standard_dev) + " - Mean: " + str(mean))


#  write the number of crimes in each cases
jump_x = (x2 - x1) / (2.0 * rows)
jump_y = (y2 - y1) / (2.0 * rows)
x_positions = np.linspace(start=x1, stop=x2, num=rows, endpoint=False)
y_positions = np.linspace(start=y1, stop=y2, num=rows, endpoint=False)

for x_index, x in enumerate(x_positions):
    for y_index, y in enumerate(y_positions):
        label = crimes[x_index, y_index]
        text_x = x + jump_x
        text_y = y + jump_y
        ax.text(text_x, text_y, label, color='black', fontsize=7, ha='center', va='center')
fig.colorbar(im)

#  check if a path exists and print if it does
if path is None:
    print("There is no path, try again")
else:
    cost = 0
    for i in range(0, len(path) - 1):
        cost = cost + getCost(path[i], path[i + 1])

    graph_path = []
    x_path = []
    y_path = []
    x_scatter = []
    y_scatter = []
    for i in path:
        graph_path.append((round(i[0] * size + x1, 3), round(i[1] * size + y1, 3)))
        x_path.append(round(i[0] * size + x1, 3))
        y_path.append(round(i[1] * size + y1, 3))

    print("Path: ", graph_path)
    print("Grid path is: ", path)
    print("Path cost: ", cost)
    print("Total time is: ", (time.time() - start_time))

    plt.plot(x_path, y_path, color="red", linewidth=4)

    x_scatter.append(graph_path[0][0])
    x_scatter.append(graph_path[len(path) - 1][0])
    y_scatter.append(graph_path[0][1])
    y_scatter.append(graph_path[len(path) - 1][1])

    plt.scatter(x_scatter, y_scatter, color="red")

plt.show()

print("The program has ended. Thank you")
