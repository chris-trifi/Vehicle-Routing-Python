# Vehicle-Routing-Python
Solving the VRP with a greedy, an optimised and a genetic algorithm.

The simple greedy algorithm is implemented by the greedy.py file and gets stored in the file named greedy_solution.txt. 

To optimize the solution a 'dropout chance' i.e. the probability that some vehicles are not selected in each round was applied. This enables more variants of the greedy solution to be tested. By iteratively running this program we can select the optimal solution. The cost is reduced by about 6% with this technique (for a dropout chance of 20%).  

The genetic algorithm that is implemented in the genetic.py file, uses multiple random swaps (mutations).

Note that a number of random swaps between nodes in the solutions were also tried without succeeding in reducing the cost even slightly. A possible interpretation is that the greedy algorithm is too 'close' to the optimal solution compared to a random solution.
