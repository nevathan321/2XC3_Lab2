import matplotlib.pyplot as plt
from graph import Graph, MVC, approx1

def generate_all_graphs(n):
    # Bitmasks wooo !
    # Complex stuff
    all_edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    for mask in range(2 ** len(all_edges)):
        G = Graph(n)
        for i, (u, v) in enumerate(all_edges):
            if mask & (1 << i):
                G.add_edge(u, v)
        yield G

def run_exhaustive_analysis(n=5):
    ratios = []
    worst_ratio = 1.0
    worst_graph = None
    
    for G in generate_all_graphs(n):
        mvc_size = len(MVC(G))
        if mvc_size == 0:
            continue
        approx_size = len(approx1(G))
        ratio = approx_size / mvc_size
        ratios.append(ratio)
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_graph = G
    
    return ratios, worst_ratio, worst_graph

def plot_results(ratios, n):
    plt.figure(figsize=(8, 5))
    plt.hist(ratios, bins=20, edgecolor='black', alpha=0.7)
    plt.axvline(x=max(ratios), color='red', linestyle='--', label=f'Worst case: {max(ratios):.2f}')
    plt.xlabel('Performance Ratio (approx1 / MVC)')
    plt.ylabel('Number of Graphs')
    plt.title(f'Exhaustive Worst-Case Analysis of approx1 (all {len(ratios)} graphs with n={n})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('exp5_worst_case.png', dpi=150)
    print("Plot saved to exp5_worst_case.png")

def print_latex_summary(ratios, worst_ratio):
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total graphs tested: {len(ratios)}")
    print(f"Worst-case ratio: {worst_ratio:.2f}")
    print(f"Optimal (ratio=1.0): {sum(1 for r in ratios if r == 1.0)} graphs")
    print(f"Average ratio: {sum(ratios)/len(ratios):.3f}")

if __name__ == "__main__":
    N = 5
    print(f"Exhaustively testing approx1 on all graphs with n={N} vertices...")
    print(f"Total graphs: 2^(5 choose 2) = 2^10 = 1024\n")
    
    ratios, worst_ratio, worst_graph = run_exhaustive_analysis(N)
    plot_results(ratios, N)
    print_latex_summary(ratios, worst_ratio)
