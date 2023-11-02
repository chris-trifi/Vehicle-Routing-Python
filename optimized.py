import matplotlib.pyplot as plt
import random
import math

random.seed(5)

def distance(old, new):
    old = data_dict[old]
    new = data_dict[new]
    dx = old[0] - new[0]
    dy = old[1] - new[1]
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist


def find_closest(current_node,available):
    min_dist = 200
    optimal_Node = -1
    if not available: return False, 0 
    for next_node in available:
        dist = distance(current_node, next_node)
        if dist < min_dist:
            min_dist = dist
            optimal_Node = next_node
    return optimal_Node, min_dist


# Specify the file path
file_path = 'instance.txt'

lines = []

with open(file_path, 'r') as file:
    for line in file:
        lines.append(line.strip()) 

        
fleet_size = int(lines[0][-2:])
capacity = int(lines[1][-3:])
customers = int(lines[2][-3:])

print('fleet size:', fleet_size)
print('capacity:', capacity)
print('customers:', customers)
starting_pos = 0

data_dict = {}

x_coordinates = []
y_coordinates = []


for i in range(5,len(lines)):
    component = lines[i].split(',')
    id = int(component[0])
    x, y = int(component[1]), int(component[2])
    x_coordinates.append(x)
    y_coordinates.append(y)
    demand = int(component[3])
    loading_time = int(component[4])
    data_dict[id] = [x,y,demand,loading_time]

'''
#visualize the grid
plt.scatter(x_coordinates, y_coordinates)
plt.show()
'''

min_cost = 100000
print("results in a few seconds...")
for round in range(3000):
    routes = [[0] for _ in range(fleet_size)]
    available =  [i for i in range(1,len(lines)-5)]
    distances = [[0] for _ in range(fleet_size)]
    ranked = [i for i in range(fleet_size)]
    while(True):
        if not available:
            break
        for i in range(fleet_size):
            #i = ranked[i]
            if(random.uniform(0,1) < 0.2):
                continue
            current_node = routes[i][-1]    
            next_node,min_dist = find_closest(current_node, available)
            if not next_node:
                break
            routes[i].append(next_node)
            distances[i].append(min_dist)
            available.remove(next_node)
        indexed_list = [(value, index) for index, value in enumerate(distances)]
        sorted_list = sorted(indexed_list, key=lambda x: x[0])
        ranked = [index for value, index in sorted_list]


    times = [0]*fleet_size
    i = 0
    for route in routes:
        time = 0    
        for step in range(1,len(route)):
            old = route[step-1]
            new = route[step]
            time += distance(old, new)
            times[i] += time
            time += 10
        i += 1

    cost = sum(times)
        
    if cost < min_cost:
        min_cost = cost
        optimal_routes = routes

print('cost:', min_cost)

file_path = 'optimized_solution.txt'

# Open the file in write mode ('w')
with open(file_path, 'w') as file:
    file.write("Cost: \n") 
    file.write(str(min_cost)+"\n")
    file.write("Routes: \n") 
    file.write("14 \n")
    for route in optimal_routes: 
        string = ','.join(str(x) for x in route)   
        string = string + '\n'
        file.write(string)




