import matplotlib.pyplot as plt
from graph import Graph, create_random_graph, MVC, MIS

def run_experiment(n_nodes=8, runs_per_edge=100):
    max_edges = n_nodes * (n_nodes - 1) // 2
    edge_counts = list(range(0, max_edges + 1, 2))
    
    mvc_sizes = []
    mis_sizes = []
    sums = []
    
    for num_edges in edge_counts:
        print(f"Testing {num_edges} edges...")
        
        mvc_sum = 0
        mis_sum = 0
        
        for _ in range(runs_per_edge):
            G = create_random_graph(n_nodes, num_edges)
            
            mvc_size = len(MVC(G))
            mis_size = len(MIS(G))
            
            mvc_sum += mvc_size
            mis_sum += mis_size
            
            # assertions !!
            assert mvc_size + mis_size == n_nodes, \
                f"Relationship violated: MVC={mvc_size}, MIS={mis_size}, sum={mvc_size+mis_size}, n={n_nodes}"
        
        mvc_sizes.append(mvc_sum / runs_per_edge)
        mis_sizes.append(mis_sum / runs_per_edge)
        sums.append((mvc_sum + mis_sum) / runs_per_edge)
    
    return edge_counts, mvc_sizes, mis_sizes, sums


def plot_results(edge_counts, mvc_sizes, mis_sizes, sums, n_nodes):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left plot: MVC and MIS sizes vs edges
    ax1.plot(edge_counts, mvc_sizes, 'b-o', label='|MVC| (Minimum Vertex Cover)', markersize=4)
    ax1.plot(edge_counts, mis_sizes, 'r-s', label='|MIS| (Maximum Independent Set)', markersize=4)
    ax1.axhline(y=n_nodes/2, color='gray', linestyle='--', alpha=0.3)
    
    ax1.set_xlabel('Number of Edges')
    ax1.set_ylabel('Set Size')
    ax1.set_title(f'MVC and MIS Sizes vs. Edge Count ({n_nodes} nodes)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right plot: Sum verification
    ax2.plot(edge_counts, sums, 'g-^', label='|MVC| + |MIS|', markersize=4)
    ax2.axhline(y=n_nodes, color='black', linestyle='-', linewidth=2, label=f'n = {n_nodes}')
    
    ax2.set_xlabel('Number of Edges')
    ax2.set_ylabel('|MVC| + |MIS|')
    ax2.set_title(f'Verification: |MVC| + |MIS| = n ({n_nodes} nodes)')
    ax2.set_ylim(n_nodes - 1, n_nodes + 1)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plt.savefig('exp4_mis_mvc_relationship.png', dpi=150)
    print("\nPlot saved to exp4_mis_mvc_relationship.png")


def print_results_table(edge_counts, mvc_sizes, mis_sizes, sums, n_nodes):
    print("\n" + "="*60)
    print(f"RESULTS TABLE (n = {n_nodes} nodes, easy copy and paste functionality because we love latex)")
    print("="*60)
    
    for i, edges in enumerate(edge_counts):
        print(f"{edges} & {mvc_sizes[i]:.2f} & {mis_sizes[i]:.2f} & {sums[i]:.2f} \\\\")


if __name__ == "__main__":
    print("="*60)
    print("EXPERIMENT 4: MIS vs MVC Relationship")
    print("="*60)
    
    N_NODES = 8
    RUNS = 100
    
    print(f"\nParameters: n={N_NODES} nodes, {RUNS} runs per edge count")
    print("Asserting: |MVC| + |MIS| = n\n")
    
    edge_counts, mvc_sizes, mis_sizes, sums = run_experiment(n_nodes=N_NODES, runs_per_edge=RUNS)
    plot_results(edge_counts, mvc_sizes, mis_sizes, sums, N_NODES)
    print_results_table(edge_counts, mvc_sizes, mis_sizes, sums, N_NODES)
