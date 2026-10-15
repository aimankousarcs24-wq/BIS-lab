import math
import random
# Step 1: Get city details from the user
n = int(input("Enter the number of cities: "))
cities = []
for i in range(n):
    x, y = map(float, input(
        f"Enter x and y coordinates of city {i + 1}: "
    ).split())
    cities.append((x, y))
# Step 2: Get ACO parameters
num_ants = int(input("Enter number of ants: "))
alpha = float(input("Enter alpha (pheromone importance): "))
beta = float(input("Enter beta (distance importance): "))
rho = float(input("Enter evaporation rate (0 to 1): "))
Q = float(input("Enter pheromone deposit constant Q: "))
iterations = int(input("Enter number of iterations: "))
# Step 3: Calculate distances
distance = [[0.0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        x1, y1 = cities[i]
        x2, y2 = cities[j]
        distance[i][j] = math.hypot(x1 - x2, y1 - y2)
# Initialize pheromone trails
pheromone = [[1.0] * n for _ in range(n)]
best_route = None
best_distance = float("inf")
# Select next city probabilistically
def select_next_city(current, unvisited):
    weights = []
    for city in unvisited:
        tau = pheromone[current][city] ** alpha
        eta = (1.0 / distance[current][city]) ** beta
        weights.append(tau * eta)
    return random.choices(
        unvisited, weights=weights, k=1
    )[0]
# Step 4: Run the ACO algorithm
for iteration in range(iterations):
    all_routes = []
    for ant in range(num_ants):
        start = random.randrange(n)
        route = [start]
        unvisited = [i for i in range(n) if i != start]
        while unvisited:
            current = route[-1]
            next_city = select_next_city(current, unvisited)
            route.append(next_city)
            unvisited.remove(next_city)
        # Calculate tour distance, including return to start
        total_distance = sum(
            distance[route[i]][route[i + 1]]
            for i in range(n - 1)
        )
        total_distance += distance[route[-1]][route[0]]
        all_routes.append((route, total_distance))
        if total_distance < best_distance:
            best_distance = total_distance
            best_route = route[:]
    # Evaporate pheromones
    for i in range(n):
        for j in range(n):
            pheromone[i][j] *= (1 - rho)
    # Deposit pheromones on each ant's route
    for route, length in all_routes:
        deposit = Q / length if length > 0 else 0
        for i in range(n):
            a = route[i]
            b = route[(i + 1) % n]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit
# Step 5: Display the result
print("\n--- ACO Result ---")
print("Best Route:", " -> ".join(
    str(city + 1) for city in best_route
), "->", best_route[0] + 1)
print("Shortest Distance:", round(best_distance, 3))
