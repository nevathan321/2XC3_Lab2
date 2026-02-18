from collections import deque
import random
#Undirected graph using an adjacency list
class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)


    # FIX: Modify this since len() with no paramter will not work
    def number_of_nodes(self):
        return len(self.adj)
    
    # FIX: STARTER CODE DID NOT HAVE THIS, BUT IT IS NECESSARY TO GET THE SIZE OF THE GRAPH OR IT WILL ERROR 
    def get_size(self):
        return len(self.adj)


#Breadth First Search
def BFS(G, node1, node2):
    Q = deque([node1])
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False

# BFS2 WHAT I IMPLEMENTED
def BFS2(G, node1, node2):
    if node1 == node2:
        return [node1]

    Q = deque([node1])
    visited = set([node1])     # included start node
    pred = {}                  # new_path

    while Q:
        current_node = Q.popleft()
        for edge in G.adj[current_node]:
            if edge not in visited:
                visited.add(edge)
                pred[edge] = current_node

                if edge == node2:
                    path = [node2]
                    while path[-1] != node1:
                        path.append(pred[path[-1]])
                    path.reverse()
                    return path

                Q.append(edge)  # keep BFS going

    return []

def BFS3(G, start):
    Q = deque([start])
    visited = set([start])
    pred = {}  # child -> parent (predecessor)

    while Q:
        u = Q.popleft()
        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                pred[v] = u
                Q.append(v)

    return pred


#Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False

def DFS2(G, node1, node2):
    # Return a path from node1 to node2 using DFS; [] if none.
    if node1 == node2:
        return [node1]

    stack = [node1]
    visited = set([node1])
    pred = {}  # predecessor map: child -> parent

    while stack:
        current = stack.pop()

        if current == node2:
            # reconstruct
            path = [node2]
            while path[-1] != node1:
                path.append(pred[path[-1]])
            path.reverse()
            return path

        for nbr in G.adj[current]:
            if nbr not in visited:
                visited.add(nbr)
                pred[nbr] = current
                stack.append(nbr)

    return []


def DFS3(G, start):
    stack = [start]
    visited = set([start])
    pred = {}  # child -> parent (predecessor)

    while stack:
        u = stack.pop()
        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                pred[v] = u
                stack.append(v)

    return pred

def has_cycle(G):
    visited = set()

    def dfs(u, parent):
        visited.add(u)
        for v in G.adj[u]:
            if v not in visited:
                if dfs(v, u):
                    return True
            elif v != parent:
                # visited neighbor that isn't the node we came from => cycle
                return True
        return False

    # graph might be disconnected, so check each component
    for node in G.adj:
        if node not in visited:
            if dfs(node, None):
                return True

    return False

def is_connected(G):
    # An undirected graph is connected if every node is reachable from any start node.
    if len(G.adj) == 0:
        return True

    start = next(iter(G.adj))  # grab any node key
    Q = deque([start])
    visited = set([start])

    while Q:
        u = Q.popleft()
        for v in G.adj[u]:
            if v not in visited:
                visited.add(v)
                Q.append(v)

    return len(visited) == len(G.adj)

def create_random_graph(i, j):
    G = Graph(i)
    max_edges = i * (i - 1) // 2
    j = min(j, max_edges)

    edges = set()
    while len(edges) < j:
        u = random.randrange(i)
        v = random.randrange(i)
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in edges:
            continue
        edges.add((a, b))
        G.add_edge(a, b)
    return G

#Use the methods below to determine minimum vertex covers

def add_to_each(sets, element):
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy

def power_set(set):
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])

def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not(start in C or end in C):
                return False
    return True


def MVC(G):
    nodes = [i for i in range(G.get_size())]
    subsets = power_set(nodes)
    min_cover = nodes
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover


if __name__ == "__main__":
    G = Graph(3)
    print(G.number_of_nodes())  # 3
    print(G.get_size())         # 3
    G.add_edge(0, 1)
    print(G.adj)                # {0:[1], 1:[0], 2:[]}