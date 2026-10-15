import random
# 1. Define the objective function
def objective_function(position):
    return sum(x ** 2 for x in position)
# 2. Initialize PSO parameters
num_particles = 30
dimensions = 2
max_iterations = 100
w = 0.7
c1 = 1.5
c2 = 1.5
lower_bound = -10
upper_bound = 10
# 3. Initialize particles
positions = [
    [random.uniform(lower_bound, upper_bound) for _ in range(dimensions)]
    for _ in range(num_particles)
]
velocities = [
    [random.uniform(-1, 1) for _ in range(dimensions)]
    for _ in range(num_particles)
]
personal_best_positions = [p[:] for p in positions]
personal_best_scores = [objective_function(p) for p in positions]
best_index = personal_best_scores.index(min(personal_best_scores))
global_best_position = personal_best_positions[best_index][:]
global_best_score = personal_best_scores[best_index]
# 4-6. Run PSO
for iteration in range(max_iterations):
    for i in range(num_particles):
        fitness = objective_function(positions[i])
        if fitness < personal_best_scores[i]:
            personal_best_scores[i] = fitness
            personal_best_positions[i] = positions[i][:]
        if fitness < global_best_score:
            global_best_score = fitness
            global_best_position = positions[i][:]
    for i in range(num_particles):
        for d in range(dimensions):
            r1 = random.random()
            r2 = random.random()
            velocities[i][d] = (
                w * velocities[i][d]
                + c1 * r1 * (personal_best_positions[i][d] - positions[i][d])
                + c2 * r2 * (global_best_position[d] - positions[i][d])
            )
            positions[i][d] += velocities[i][d]
            positions[i][d] = max(lower_bound, min(upper_bound, positions[i][d]))
    if (iteration + 1) % 10 == 0:
        print(f"Iteration {iteration + 1}: Best fitness = {global_best_score:.6f}")
# 7. Output the best solution
print("\nOptimization completed!")
print("Best position:", global_best_position)
print("Minimum function value:", global_best_score)
