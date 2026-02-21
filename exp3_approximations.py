import matplotlib.pyplot as plt
from graph import create_random_graph, MVC, approx1, approx2, approx3

def run_experiment(n_nodes=8, runs_per_edge=1000):
    max_edges = n_nodes * (n_nodes - 1) // 2
    edge_counts = list(range(1, max_edges + 1, 2))
    
    ratios = {
        'approx1': [],
        'approx2': [],
        'approx3': []
    }
    
    for num_edges in edge_counts:
        print(f"Testing {num_edges} edges...")
        
        approx1_ratios = []
        approx2_ratios = []
        approx3_ratios = []
        
        for _ in range(runs_per_edge):
            G = create_random_graph(n_nodes, num_edges)
            
            mvc_size = len(MVC(G))
            
            if mvc_size == 0:
                continue
            
            a1_size = len(approx1(G))
            a2_size = len(approx2(G))
            a3_size = len(approx3(G))
            
            approx1_ratios.append(a1_size / mvc_size)
            approx2_ratios.append(a2_size / mvc_size)
            approx3_ratios.append(a3_size / mvc_size)
        
        ratios['approx1'].append(sum(approx1_ratios) / len(approx1_ratios) if approx1_ratios else 0)
        ratios['approx2'].append(sum(approx2_ratios) / len(approx2_ratios) if approx2_ratios else 0)
        ratios['approx3'].append(sum(approx3_ratios) / len(approx3_ratios) if approx3_ratios else 0)
    
    return edge_counts, ratios


def run_node_experiment(node_counts=[6, 8, 10], runs_per_config=500):
    results = {}
    
    for n in node_counts:
        print(f"\n=== Testing with {n} nodes ===")
        max_edges = n * (n - 1) // 2
        num_edges = max_edges // 2  # 50% density
        
        approx1_ratios = []
        approx2_ratios = []
        approx3_ratios = []
        
        for i in range(runs_per_config):
            if i % 100 == 0:
                print(f"  Run {i}/{runs_per_config}")
            
            G = create_random_graph(n, num_edges)
            mvc_size = len(MVC(G))
            
            if mvc_size == 0:
                continue
            
            approx1_ratios.append(len(approx1(G)) / mvc_size)
            approx2_ratios.append(len(approx2(G)) / mvc_size)
            approx3_ratios.append(len(approx3(G)) / mvc_size)
        
        results[n] = {
            'approx1': sum(approx1_ratios) / len(approx1_ratios),
            'approx2': sum(approx2_ratios) / len(approx2_ratios),
            'approx3': sum(approx3_ratios) / len(approx3_ratios)
        }
    
    return results


def plot_results(edge_counts, ratios, n_nodes):
    plt.figure(figsize=(10, 6))
    
    plt.plot(edge_counts, ratios['approx1'], 'b-o', label='approx1 (Greedy by Degree)', markersize=4)
    plt.plot(edge_counts, ratios['approx2'], 'r-s', label='approx2 (Random Vertex)', markersize=4)
    plt.plot(edge_counts, ratios['approx3'], 'g-^', label='approx3 (Random Edge)', markersize=4)
    
    plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Optimal (ratio = 1.0)')
    
    plt.xlabel('Number of Edges')
    plt.ylabel('Performance Ratio (Approx Size / MVC Size)')
    plt.title(f'Vertex Cover Approximation Performance ({n_nodes} nodes, 1000 runs per point)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('images/exp3_approx_comparison.png', dpi=150)
    print("\nPlot saved to images/exp3_approx_comparison.png")


def plot_node_results(node_results):
    node_counts = sorted(node_results.keys())
    
    plt.figure(figsize=(8, 5))
    
    approx1_vals = [node_results[n]['approx1'] for n in node_counts]
    approx2_vals = [node_results[n]['approx2'] for n in node_counts]
    approx3_vals = [node_results[n]['approx3'] for n in node_counts]
    
    x = range(len(node_counts))
    width = 0.25
    
    plt.bar([i - width for i in x], approx1_vals, width, label='approx1 (Greedy)', color='blue', alpha=0.7)
    plt.bar(x, approx2_vals, width, label='approx2 (Random Vertex)', color='red', alpha=0.7)
    plt.bar([i + width for i in x], approx3_vals, width, label='approx3 (Random Edge)', color='green', alpha=0.7)
    
    plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    
    plt.xlabel('Number of Nodes')
    plt.ylabel('Average Performance Ratio')
    plt.title('Approximation Performance vs. Graph Size (50% edge density)')
    plt.xticks(x, node_counts)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    plt.savefig('images/exp3_node_comparison.png', dpi=150)
    print("\nNode comparison plot saved to images/exp3_node_comparison.png")


def print_results_table(edge_counts, ratios):
    print("\n" + "="*70)
    print("RESULTS TABLE (late format because we love latex woo)")
    print("="*70)
    
    for i, edges in enumerate(edge_counts):
        print(f"{edges} & {ratios['approx1'][i]:.3f} & {ratios['approx2'][i]:.3f} & {ratios['approx3'][i]:.3f} \\\\")


if __name__ == "__main__":
    print("="*60)
    print("EXPERIMENT 3: Vertex Cover Approximation Comparison")
    print("="*60)
    
    N_NODES = 8
    RUNS = 1000
    
    print(f"\nParameters: n={N_NODES} nodes, {RUNS} runs per edge count")
    
    edge_counts, ratios = run_experiment(n_nodes=N_NODES, runs_per_edge=RUNS)
    plot_results(edge_counts, ratios, N_NODES)
    print_results_table(edge_counts, ratios)
    
    print("\n" + "="*60)
    print("SECONDARY EXPERIMENT: Varying Node Count")
    print("="*60)
    
    node_results = run_node_experiment(node_counts=[6, 8, 10], runs_per_config=500)
    plot_node_results(node_results)
    
    print("\n" + "="*60)
    print("NODE VARIATION RESULTS (LaTeX format !!!!)")
    print("="*60)
    for n, res in sorted(node_results.items()):
        print(f"{n} & {res['approx1']:.3f} & {res['approx2']:.3f} & {res['approx3']:.3f} \\\\")
