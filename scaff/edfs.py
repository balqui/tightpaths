'''
Jose Luis Balcazar, balqui at GitHub
Early Floreal 2025
MIT License

Find tight pairs in a directed graph. 
Closely based on the function edge_dfs of the NetworkX package.

Graphs are NetworkX DiGraphs read from edge lists.
There, each edge is described by strings for the source 
and target vertices in this order, plus a dictionary with,
at least, the key 'cost' and a positive number as cost value.
'''

import networkx as nx

def simpl_edge_dfs(digraph):

    for start_node in digraph:

        print(" ... from ", start_node)
        visited_edges = set()
        visited_nodes = set()
        edges = {}

        stack = [start_node]
        while stack:
            current_node = stack[-1]
            if current_node not in visited_nodes:
                edges[current_node] = iter(digraph.edges(current_node))
                visited_nodes.add(current_node)

            try:
                edge = next(edges[current_node])
            except StopIteration:
                # No more edges from the current node.
                stack.pop()
            else:
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    stack.append(edge[1])
                    yield edge


if __name__ == "__main__":
    g = nx.read_edgelist("e1.elist", create_using = nx.DiGraph)
    print("dfs_edges:")
    for e in nx.dfs_edges(g): print(e)
    print("dfs_tree edges:")
    print(nx.dfs_tree(g).edges)
    print("edge_dfs from A:")
    for e in nx.edge_dfs(g, 'A'): print(e, "cost", g.edges[e]['cost'])

    print("simplified edge_dfs:")
    for e in simpl_edge_dfs(g): print(e, "cost", g.edges[e]['cost'])
