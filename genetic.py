import matplotlib.pyplot as plt
import random
import math

#random.seed(1)

def distance(old, new):
    old = data_dict[old]
    new = data_dict[new]
    dx = old[0] - new[0]
    dy = old[1] - new[1]
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist

# Specify the file path
file_path = 'instance.txt'

lines = []

with open(file_path, 'r') as file:
    for line in file:
        lines.append(line.strip()) 

        
fleet_size = int(lines[0][-2:])
capacity = int(lines[1][-3:])
customers = int(lines[2][-3:])

print(fleet_size)
print(capacity)
print(customers)
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


def generateRandom():
    routes = [[0] for _ in range(fleet_size)]
    available =  [i for i in range(1,len(lines)-5)]
    while(True):
        if not available:
            break
        for i in range(fleet_size):
            try:    
                next_node = random.choice(available)
            except:
                break
            routes[i].append(next_node)
            available.remove(next_node)
    return routes

def get_greedy():
    sol_lines = []
    routes = []
    with open('solution.txt', 'r') as file:
        for line in file:
            sol_lines.append(line.strip())
    for i in range(4,len(sol_lines)):
        routes.append(sol_lines[i].split(','))
    for i in range(len(routes)):
        routes[i] = [int(x) for x in routes[i]]
    return routes


def calculate_score(routes):
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
    return cost


class solution():
    def __init__(self, routes, score = 0):
        self.routes = routes
        self.score = score
    def mutate(self, amount):
        for _ in range(amount):
            first = random.randint(0,13)
            second = random.randint(0,13)
            gene_1 = random.randint(0,len(self.routes[first])-1)
            gene_2 = random.randint(0,len(self.routes[second])-1)
            temp = self.routes[first][gene_1]
            self.routes[first][gene_1] = self.routes[second][gene_2]
            self.routes[second][gene_2] = temp
    def sequence_mutate(self, amount):    #swap an element with on in the same depth of another vehicles route
        for _ in range(amount):
            first = random.randint(0,13)
            while True:
                second = random.randint(0, 13)  # Generate a random integer in the range [0, 12]
                if second != first:
                    break
            min_depth = min(len(self.routes[first]),len(self.routes[second]))
            depth = random.randint(0,min_depth-1)
            temp = self.routes[first][depth:]
            self.routes[first][depth:] = self.routes[second][depth:]
            self.routes[second][depth:] = temp
    def two_opt(self, amount):    #swap an element with on in the same depth of another vehicles route
        for i in range(amount):
            if amount == 1:
                choice = random.randint(0,13)
            else:
                choice = i
            max_depth = len(self.routes[choice])
            depth = random.randint(1,max_depth-2)
            temp = self.routes[choice][depth+1]
            self.routes[choice][depth+1] = self.routes[choice][depth]
            self.routes[choice][depth] = temp

 
    def calculate_score(self):
        self.score = calculate_score(self.routes)
    def copy(self):
        return solution(self.routes)


def fitness_proportional_selection(solutions, select_num):
    scores = []
    for sol in solutions:
        scores.append(sol.score)

    max_score = max(scores)
    min_score = min(scores)
    idx = scores.index(min_score)

    for i in range(len(scores)):
        #scores[i] = max_score - scores[i]
        #scores[i] = scores[i] / 10 
        scores[i] = scores[i]
    total_score = sum(scores)
    normalized_scores = [score / total_score for score in scores]
    selected_candidates = []

    for selections in range(select_num):
        if selections == 1:
            selected_candidates.append(solutions[idx])
            continue
        # Select a candidate using roulette wheel selection
        rand_value = random.uniform(0, 1)
        cumulative_prob = 0

        for i in range(len(solutions)):
            cumulative_prob += normalized_scores[i]
            if cumulative_prob >= rand_value:
                selected_candidates.append(solutions[i])
                break
    return selected_candidates


solutions = []
scores = []
population = 5000

routes = get_greedy()


#CREATE INITIAL CANDIDATE SOLUTIONS
for i in range(population):
    #routes = generateRandom()
    sol = solution(routes)
    sol.calculate_score()
    solutions.append(sol)

wop = 0
reproduction_rate = 4
generations = 2000
for gen in range(generations):
    min_score = 100000
    select_num = int(population / (1 + reproduction_rate))
    selection = fitness_proportional_selection(solutions, select_num)
    population = len(selection)
    for i in range(population):
        selected = selection[i]
        for copy in range(reproduction_rate):
            copy = selected.copy()
            if(random.uniform(0, 1) < 0.999):
                copy.two_opt(1)
            elif(random.uniform(0, 1) < 0.1):
                copy.two_opt(13)
            copy.calculate_score()
            if copy.score < min_score:
                min_score = copy.score               
            selection.append(copy)
        #print(copy.score)
        if selected.score < min_score:
            min_score = selected.score 
    population = len(selection)
    solutions = selection.copy()
    wop += 1
    if wop == 10:
        print(min_score)
        wop = 1





