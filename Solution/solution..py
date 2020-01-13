import pandas as pd
import statistics
import matplotlib.pyplot as plt
import math


# an object to store geo data
class geo_data:
    def __init__(self, row):
        self.time = row[1]
        self.prov = row[3]
        self.city = row[4]
        self.lat = row[5]
        self.long = row[6]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


# read csv files and store them to a list of objects
def csv_to_pandas(filename):
    data_df = pd.read_csv(filename)

    geo_set = []

    for index, row in data_df.iterrows():
        geo_obj = geo_data(row)

        # only add geo_data that is not the same to the added data
        if geo_obj not in geo_set:
            geo_set.append(geo_obj)

    return geo_set


# assign data points to their closest point of interest
def data_label(filename, data_set):
    data_df = pd.read_csv(filename)
    poi = []
    group = {}
    distances = {}
    centers = []
    centers_data = {}

    # read and store values for each POI
    for index, row in data_df.iterrows():
        group[row[0]] = []
        distances[row[0]] = []
        centers.append(row[0])
        poi.append((row[1], row[2]))
        centers_data[row[0]] = [row[1], row[2]]

    # label the data to it's closest POI
    for data in data_set:
        distance = []

        # calculate the distance from the request to each POI
        for center in poi:
            distance.append(((center[0] - data.lat) ** 2 + (center[1] - data.long) ** 2) ** 0.5)

        # label the data to the POI with the minimum distance
        closest = distance.index(min(distance))
        group[centers[closest]].append(data)
        distances[centers[closest]].append(min(distance))

    return group, distances, centers_data


# calculate avg and std deviation of distances for each group
def calculate_avg_distance(distances):
    avg_distances = []
    std_distances = []

    print("Part 3-1")

    for key in distances:
        if len(distances[key]) > 0:
            avg_dis = sum(distances[key]) / len(distances[key])
            std_dis = statistics.stdev(distances[key])

            avg_distances.append(avg_dis)
            std_distances.append(std_dis)

            print("avg distance to " + key + " is " + str(avg_dis))
            print("std deviation to " + key + " is " + str(std_dis))

    return avg_distances, std_distances


# calculate density
def calcualte_density(name, radius, points):
    print("")
    print("Part 3-2")
    area = radius ** 2 * math.pi

    if area == 0:
        density = 0
    else:
        density = points / area

    print(name + "'s density is " + str(density))


# output points on a circle for each group
def form_circle(data_group, centers, distances):
    i = 1

    for group in data_group:

        # set radius to 0 if the group is empty
        if len(distances[group]) == 0:
            radius = 0
        else:
            radius = max(distances[group])

        # build x and y coordinates in arrays for plot purposes
        x = []
        y = []
        for point in data_group[group]:
            x.append(point.lat)
            y.append(point.long)

        calcualte_density(group, radius, len(x))

        fig, ax = plt.subplots()

        # set x and y limit
        plt.xlim(centers[group][0] - radius - 1, centers[group][0] + radius + 1)
        plt.ylim(centers[group][1] - radius - 1, centers[group][1] + radius + 1)

        # plot the circle with the max distance
        circle = plt.Circle(centers[group], radius=radius, color='y')
        ax.add_artist(circle)

        # plot all the datapoints in red and POI point in blue
        plt.plot(x, y, 'ro')
        plt.plot(centers[group][0], centers[group][1], 'bo')

        plt.title('plot for ' + group + " and it's requests")

        plt.show()

        i += 1


# read the file and build a reversed graph
def build_graph(filename):

    file = open(filename, "r")
    lines = file.readlines()

    edges = {}

    for line in lines:
        line = line.strip('\n')
        points = line.split("->")

        # add edges to the the corresponding nodes
        if int(points[1]) in edges:
            edges[int(points[1])].append(int(points[0]))
        else:
            edges[int(points[1])] = [int(points[0])]

    file.close()
    return edges


# perform topological sort
# start is a list of starting points
# there is only one "end" point
def top_sort(edges, start, end):
    stack = []
    visited = []

    # topological sort from the final point
    stack, visited = sort_until(edges, end, stack, visited, start)

    print("")
    print("Part 4-2")
    print(str(stack)[1:-1])

    return stack


# perform topological sort
def sort_until(edges, node, stack, visited, start):
    visited.append(node)
    stack.insert(0,node)

    # stop searching when hit the starting points
    if node in start or node not in edges:
        return stack, visited

    # DFS for all the nodes
    for edge in edges[node]:
        if edge not in visited:
            stack, visited = sort_until(edges, edge, stack, visited, start)

    return stack, visited


# main function to call functions to solve each part
def main():
    # part 1
    data_set = csv_to_pandas("../ws-data-spark-master/data/DataSample.csv")

    # part 2
    data_group, data_distance, centers = data_label("../ws-data-spark-master/data/POIList.csv", data_set)

    # part 3-1
    avg_distances, std_distances = calculate_avg_distance(data_distance)

    # part 3-2
    form_circle(data_group, centers, data_distance)

    # part 4-2
    # no need of task_ids.txt as we can node with no edges
    edges = build_graph("../ws-data-spark-master/data/relations.txt")
    stack = top_sort(edges, [73], 36)


if __name__ == '__main__':
    main()
