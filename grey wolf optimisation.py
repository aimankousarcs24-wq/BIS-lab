
import random
import tkinter as tk


# Step 1: Objective function - Sphere function
def objective_function(x):
    return sum(value ** 2 for value in x)


# Step 2: Initialize parameters
num_wolves = 5
num_dimensions = 2
num_iterations = 30
lb = -10
ub = 10


# Step 3: Initialize wolf positions
wolves = [
    [random.uniform(lb, ub) for _ in range(num_dimensions)]
    for _ in range(num_wolves)
]


alpha_pos = [0.0] * num_dimensions
beta_pos = [0.0] * num_dimensions
delta_pos = [0.0] * num_dimensions

alpha_score = float("inf")
beta_score = float("inf")
delta_score = float("inf")

alpha_score_history = []


# Step 4: Evaluate fitness and identify alpha, beta, delta
def evaluate_fitness():
    global alpha_pos, beta_pos, delta_pos
    global alpha_score, beta_score, delta_score

    ranked_wolves = sorted(
        wolves, key=objective_function
    )

    alpha_pos = ranked_wolves[0][:]
    beta_pos = ranked_wolves[1][:]
    delta_pos = ranked_wolves[2][:]

    alpha_score = objective_function(alpha_pos)
    beta_score = objective_function(beta_pos)
    delta_score = objective_function(delta_pos)


# Step 5: Update wolf positions
def update_positions(iteration):
    a = 2 - 2 * iteration / num_iterations

    for i in range(num_wolves):
        for j in range(num_dimensions):

            r1 = random.random()
            r2 = random.random()
            A1 = 2 * a * r1 - a
            C1 = 2 * r2
            D_alpha = abs(C1 * alpha_pos[j] - wolves[i][j])
            X1 = alpha_pos[j] - A1 * D_alpha

            r1 = random.random()
            r2 = random.random()
            A2 = 2 * a * r1 - a
            C2 = 2 * r2
            D_beta = abs(C2 * beta_pos[j] - wolves[i][j])
            X2 = beta_pos[j] - A2 * D_beta

            r1 = random.random()
            r2 = random.random()
            A3 = 2 * a * r1 - a
            C3 = 2 * r2
            D_delta = abs(C3 * delta_pos[j] - wolves[i][j])
            X3 = delta_pos[j] - A3 * D_delta

            wolves[i][j] = (X1 + X2 + X3) / 3
            wolves[i][j] = max(
                lb, min(ub, wolves[i][j])
            )


# Step 6: Run the optimization
for iteration in range(num_iterations):
    evaluate_fitness()
    alpha_score_history.append(alpha_score)
    update_positions(iteration)

# Evaluate final positions
evaluate_fitness()
alpha_score_history.append(alpha_score)


# Step 7: Display final results
print("Grey Wolf Optimizer Results")
print("Best Solution:", [round(x, 6) for x in alpha_pos])
print("Best Solution Fitness:", round(alpha_score, 8))


# Step 8: Plot convergence graph using Tkinter
def plot_graph(history):
    root = tk.Tk()
    root.title("Grey Wolf Optimizer - Convergence")

    width = 700
    height = 400
    canvas = tk.Canvas(
        root, width=width, height=height, bg="white"
    )
    canvas.pack()

    canvas.create_text(
        width // 2, 20,
        text="Convergence of Grey Wolf Optimizer",
        font=("Arial", 14, "bold")
    )

    left, right = 65, width - 25
    top, bottom = 50, height - 55

    canvas.create_line(left, top, left, bottom, width=2)
    canvas.create_line(left, bottom, right, bottom, width=2)

    canvas.create_text(
        18, height // 2, text="Alpha Fitness", angle=90
    )
    canvas.create_text(
        width // 2, height - 20, text="Iteration"
    )

    max_value = max(history) if max(history) > 0 else 1
    points = []

    for i, value in enumerate(history):
        x = left + i * (right - left) / max(1, len(history) - 1)
        y = bottom - (value / max_value) * (bottom - top)
        points.extend([x, y])

    if len(points) >= 4:
        canvas.create_line(*points, fill="blue", width=2)

    root.mainloop()


plot_graph(alpha_score_history)
