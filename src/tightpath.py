'''
Jose Luis Balcazar, balqui at GitHub
Early Floreal 2025, cosmetic touches by mid and late Floreal.
MIT License

Find tight paths in a directed graph. 
Follows in part the ideas in the function edge_dfs 
of the NetworkX package, but simplified as we don't 
need strict dfs order on the edges.

Graphs are NetworkX DiGraphs read from edge lists.
There, each edge is described by strings for the 
source and target vertices in this order, plus a 
dictionary with, at least, the key 'cost' and a 
positive number as cost value.
'''

from time import time

import networkx as nx

from pathtree import PathTree

def tight_paths(g, root, bound):
    '''
    All tight paths starting at root under bound.
    Could be made an iterator, but want now to compute running time.
    '''
    cl_pred = float("inf")
    for u in g.predecessors(root):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, g[u][root]['cost'])
    ret_paths = list()
    t = PathTree()
    root = t.treenode(root)
    t.add_node(root)
    stack = [ (root, 0) ]
    while stack:
        v, d = stack.pop()
        mayextend = False
        for u in g.neighbors(v[0]):
            "v is now a treenode, and v[0] its graph vertex"
            if d + g[v[0]][u]['cost'] <= bound:
                "u becomes a treenode too"
                u = t.treenode(u) 
                t.add_edge(u, v)
                stack.append( (u, d + g[v[0]][u[0]]['cost']) )
                mayextend = True
        if not mayextend and cl_pred + d > bound:
            ret_paths.append(t.path(v)) # THERE MAY BE 0-EDGE PATHS
    return ret_paths

if __name__ == "__main__":

    fnm = input("Graph filename? (.elist assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        tacc = 0 # accumulated time
        for start_node in g:
            t = time()
            tps = tight_paths(g, start_node, float(bound))
            tacc += time() - t
            for path in tps:
                if len(path) > 1:
                    "1-vertex paths often not useful"
                    print(path)
        input(f"Time: {tacc:7.4f}")
        bound = input("Bound? (<CR> to finish) ")
