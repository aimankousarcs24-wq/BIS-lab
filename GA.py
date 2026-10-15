import random
POPULATION_SIZE = 10
CHROMOSOME_LENGTH = 5
GENERATIONS = 30
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
# Create a random chromosome
def create_chromosome():
    return [random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)]
# Convert binary chromosome to decimal value
def decode(chromosome):
    return int("".join(map(str, chromosome)), 2)
# Fitness function: maximize x^2
def fitness(chromosome):
    x = decode(chromosome)
    return x ** 2
# Roulette Wheel Selection
def roulette_selection(population):
    total_fitness = sum(fitness(c) for c in population)
    if total_fitness == 0:
        return random.choice(population)[:]
    probabilities = [
        fitness(c) / total_fitness
        for c in population
    ]
    return random.choices(
        population,
        weights=probabilities,
        k=1
    )[0][:]
# Rank Selection
def rank_selection(population):
    ranked = sorted(population, key=fitness)
    ranks = list(range(1, len(ranked) + 1))
    return random.choices(
        ranked,
        weights=ranks,
        k=1
    )[0][:]
# Tournament Selection
def tournament_selection(population):
    tournament = random.sample(population, 3)
    return max(
        tournament,
        key=fitness
    )[:]
# Crossover
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(
            1,
            CHROMOSOME_LENGTH - 1
        )
        child1 = (
            parent1[:point] +
            parent2[point:]
        )
        child2 = (
            parent2[:point] +
            parent1[point:]
        )
        return child1, child2
    return parent1[:], parent2[:]
# Mutation
def mutation(chromosome):
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]
    return chromosome
# Genetic Algorithm
def genetic_algorithm(selection_method):
    population = [
        create_chromosome()
        for _ in range(POPULATION_SIZE)
    ]
    best_history = []
    for generation in range(GENERATIONS):
        # Find best chromosome
        best = max(
            population,
            key=fitness
        )
        best_history.append(
            fitness(best)
        )
        # Create new population
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            # Selection
            parent1 = selection_method(population)
            parent2 = selection_method(population)
            # Crossover
            child1, child2 = crossover(
                parent1,
                parent2
            )
            # Mutation
            child1 = mutation(child1)
            child2 = mutation(child2)
            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)
        population = new_population
    # Final best solution
    best = max(
        population,
        key=fitness
    )
    return (
        decode(best),
        fitness(best),
        best_history
    )
# Run Roulette Selection
x1, f1, history1 = genetic_algorithm(
    roulette_selection
)
# Run Rank Selection
x2, f2, history2 = genetic_algorithm(
    rank_selection
)
# Run Tournament Selection
x3, f3, history3 = genetic_algorithm(
    tournament_selection
)
# Display final results
print("\n========================================")
print("     GENETIC ALGORITHM RESULTS")
print("========================================")
print("\nOptimization Function:")
print("f(x) = x^2")
print("\nSearch Range:")
print("0 <= x <= 31")
print("\nPopulation Size:", POPULATION_SIZE)
print("Number of Generations:", GENERATIONS)
print("Mutation Rate:", MUTATION_RATE)
print("Crossover Rate:", CROSSOVER_RATE)
print("\n----------------------------------------")
print("Selection Method       Best x    Fitness")
print("----------------------------------------")
print(
    "Roulette Selection    ",
    x1,
    "       ",
    f1
)
print(
    "Rank Selection        ",
    x2,
    "       ",
    f2
)
print(
    "Tournament Selection  ",
    x3,
    "       ",
    f3
)
print("----------------------------------------")
# Print convergence history
print("\n\nCONVERGENCE RESULTS")
print("===================")
print("\nGeneration | Roulette | Rank | Tournament")
print("-------------------------------------------")
for i in range(GENERATIONS):
    print(
        f"{i + 1:^10} | "
        f"{history1[i]:^8} | "
        f"{history2[i]:^4} | "
        f"{history3[i]:^10}"
    )
# Find overall best
results = [
    ("Roulette Selection", x1, f1),
    ("Rank Selection", x2, f2),
    ("Tournament Selection", x3, f3)
]
best_result = max(
    results,
    key=lambda item: item[2]
)
print("\n\n========================================")
print("           OVERALL BEST RESULT")
print("========================================")
print("Selection Method :", best_result[0])
print("Best Solution    :", best_result[1])
print("Best Fitness     :", best_result[2])
print("\nProgram completed successfully.")
