import numpy as np
import pandas as pd
import math
import imageio

def getRedPoints(cluster_distance = 25, path = "I:/Code/SWP/Raycasts/data/redpoints_walls.jpg", red_min_value = 200):
    """
    Given a Path, this function will return a list of points in the form of tuples (x, y).
    The points are read from the picture in a way such that points that exceed the red_min_value will be taken and only one will be considered in the range of cluster_distance.
    """
    im = imageio.imread(path)
    point_cluster_center = []
    add_new = True
    for i in range(0, im.shape[0]):
        for j in range(0, im.shape[1]):
            add_new = True
            if im[i, j, 0] > red_min_value:
                for k in range(0, len(point_cluster_center)):
                    if getDistance(point_cluster_center[k][0], point_cluster_center[k][1], j, i) < cluster_distance:
                        add_new = False
                if add_new:
                    point_cluster_center.append((j,i))
    return point_cluster_center

def defineLines(points):
    """
    Given a list of points (in a circle-like strucuture), this function will return a list of lines in the form of tuples (x1, y1, x2, y2).
    Points given have to be sorted by x or y (ascending or descending) in order for this to work correctly, if given unsorted this might return wrong values.
    """
    lines_list = []
    #First of we choose a point to look at, then we search for the nearest nearest other point (from our pot) to that one and remove the chosen point from our pot.
    while len(points) > 1:
        current_point = points[0]
        points.pop(0)
        cur_min_index = 0
        cur_min_dist = getDistance(current_point[0], current_point[1], points[0][0], points[0][1])
        for  i in range(1, len(points)):
            temp = getDistance(current_point[0], current_point[1], points[i][0], points[i][1])
            if temp < cur_min_dist:
                cur_min_dist = temp
                cur_min_index = i
        lines_list.append((current_point[0], current_point[1], points[cur_min_index][0], points[cur_min_index][1]))

    #For our last line to be computed correctly, we take the 2 points that were only used once for now and define a line between them.
    temp = []
    lines_list_single_points = [(elem[0], elem[1]) for elem in lines_list] + [(elem[2], elem[3]) for elem in lines_list]
    count_points = {x:lines_list_single_points.count(x) for x in lines_list_single_points}
    for elem in count_points.items():
        if elem[1] == 1:
            temp.append(elem[0])
    lines_list.append((temp[0][0], temp[0][1], temp[1][0], temp[1][1]))
    return lines_list

def getDistance(x1, y1, x2, y2):
    """
    Computes distance between 2 given points.
    """
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def get_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    Code taken from: https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)