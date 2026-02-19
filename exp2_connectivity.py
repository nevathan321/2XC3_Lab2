"""
Experiment 2: Connectivity Probability vs Number of Edges
COMPSCI 2XC3 - Lab 2

Question: With i nodes and j edges, what is the probability a random graph is connected?

Setup:
  - Fixed nodes: 100
  - Edge range: 0 to 500, step 25
  - Runs per edge count: 100
"""

import time
import functools
import matplotlib.pyplot as plt
from graph import create_random_graph, is_connected


def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__!r} in {time.perf_counter() - start:.4f} seconds")
        return result
    return wrapper


@timer_decorator
def run_connectivity_experiment(num_nodes, edge_values, num_runs):
    """
    For each edge count in edge_values, generates num_runs random graphs
    and returns the proportion that are connected.
    """
    probabilities = []

    for j in edge_values:
        connected_count = sum(
            1 for _ in range(num_runs)
            if is_connected(create_random_graph(num_nodes, j))
        )
        prob = connected_count / num_runs
        probabilities.append(prob)
        print(f"  nodes={num_nodes}, edges={j:>4},  P(connected) = {prob:.2f}")

    return probabilities


def plot_single_curve(edge_values, probabilities, num_nodes, num_runs):
    plt.figure(figsize=(9, 5))
    plt.plot(edge_values, probabilities, marker='o', color='steelblue', linewidth=2, markersize=6)
    plt.xlabel("Number of Edges", fontsize=12)
    plt.ylabel("P(graph is connected)", fontsize=12)
    plt.title(
        f"Experiment 2: Connectivity Probability vs Number of Edges\n"
        f"({num_nodes} nodes, {num_runs} runs per data point)", fontsize=13
    )
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("exp2_connectivity_probability.png", dpi=150)
    plt.show()


if __name__ == "__main__":

    NUM_RUNS = 100

    print("=" * 50)
    print("Experiment 2: Connectivity (100 nodes)")
    print("=" * 50)

    NODES = 100
    EDGE_VALUES = list(range(0, 501, 25))

    probs = run_connectivity_experiment(NODES, EDGE_VALUES, NUM_RUNS)
    plot_single_curve(EDGE_VALUES, probs, NODES, NUM_RUNS)

    print("\nDone.")