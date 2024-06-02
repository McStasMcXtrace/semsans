import pygad

# Define the fitness function
def fitness_func(ga_instance, solution, solution_idx):
    return sum(solution)

# Define the constraint function
def apply_constraints(ga_instance):
    for chromosome_idx in range(ga_instance.population.shape[0]):
        ga_instance.population[chromosome_idx] = [
            max(0, min(3, gene)) for gene in ga_instance.population[chromosome_idx]
        ]

# Create a callback function that applies the constraints
def on_generation(ga_instance):
    apply_constraints(ga_instance)
    print(f"Generation {ga_instance.generations_completed}: Best Fitness = {ga_instance.best_solution()[1]}")

# Number of genes in each solution
num_genes = 10

# Initialize the GA instance
ga_instance = pygad.GA(
    num_generations=1000,
    num_parents_mating=2,
    fitness_func=fitness_func,
    sol_per_pop=200,
    num_genes=num_genes,
    on_generation=on_generation,
)

# Run the GA
ga_instance.run()

# Retrieve and print the best solution
best_solution, best_fitness, best_solution_idx = ga_instance.best_solution()
print(f"Best solution: {best_solution}\nBest fitness: {best_fitness}")