
import random
import math
import tkinter as tk


# Objective function: Sphere function
def objective_function(x):
    return sum(value ** 2 for value in x)


# Levy flight function
def levy_flight(Lambda):
    sigma_u = (
        math.gamma(1 + Lambda) * math.sin(math.pi * Lambda / 2)
        / (
            math.gamma((1 + Lambda) / 2)
            * Lambda
            * 2 ** ((Lambda - 1) / 2)
        )
    ) ** (1 / Lambda)

    u = random.gauss(0, sigma_u)
    v = random.gauss(0, 1)

    return u / (abs(v) ** (1 / Lambda) + 1e-10)


# Cuckoo Search algorithm
def cuckoo_search(
    num_nests=30,
    num_iterations=30,
    discovery_rate=0.25,
    dim=10,
    lower_bound=-5,
    upper_bound=5
):
    nests = [
        [random.uniform(lower_bound, upper_bound)
         for _ in range(dim)]
        for _ in range(num_nests)
    ]

    fitness = [objective_function(nest) for nest in nests]

    best_index = fitness.index(min(fitness))
    best_nest = nests[best_index][:]
    best_fitness = fitness[best_index]

    Lambda = 1.5
    fitness_history = []

    for iteration in range(num_iterations):

        for i in range(num_nests):
            step_size = levy_flight(Lambda)

            new_solution = [
                nests[i][j] + step_size *
                (nests[i][j] - best_nest[j])
                for j in range(dim)
            ]

            new_solution = [
                max(lower_bound, min(upper_bound, value))
                for value in new_solution
            ]

            new_fitness = objective_function(new_solution)

            if new_fitness < fitness[i]:
                nests[i] = new_solution
                fitness[i] = new_fitness

        count = max(1, int(discovery_rate * num_nests))
        random_nests = random.sample(range(num_nests), count)

        for index in random_nests:
            nests[index] = [
                random.uniform(lower_bound, upper_bound)
                for _ in range(dim)
            ]
            fitness[index] = objective_function(nests[index])

        current_best = fitness.index(min(fitness))

        if fitness[current_best] < best_fitness:
            best_fitness = fitness[current_best]
            best_nest = nests[current_best][:]

        fitness_history.append(best_fitness)

    return best_nest, best_fitness, fitness_history


# Draw convergence graph using Tkinter
def plot_graph(history):
    root = tk.Tk()
    root.title("Cuckoo Search - Fitness Convergence")

    width, height = 700, 400
    canvas = tk.Canvas(root, width=width, height=height,
                       bg="white")
    canvas.pack()

    canvas.create_text(
        width // 2, 20,
        text="Fitness Convergence Over Iterations",
        font=("Arial", 14, "bold")
    )

    left, right = 60, width - 25
    top, bottom = 50, height - 50

    canvas.create_line(left, top, left, bottom, width=2)
    canvas.create_line(left, bottom, right, bottom, width=2)

    canvas.create_text(18, height // 2,
                       text="Best Fitness", angle=90)
    canvas.create_text(width // 2, height - 15,
                       text="Iteration")

    max_value = max(history) if max(history) > 0 else 1
    points = []

    for i, value in enumerate(history):
        x = left + i * (right - left) / max(1, len(history) - 1)
        y = bottom - (value / max_value) * (bottom - top)
        points.extend([x, y])

    if len(points) >= 4:
        canvas.create_line(*points, fill="blue", width=2)

    root.mainloop()


# Run algorithm
best_nest, best_fitness, history = cuckoo_search()

print("Best Solution:", [round(x, 6) for x in best_nest])
print("Best Fitness:", round(best_fitness, 8))

plot_graph(history)
