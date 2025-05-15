'''
Jose Luis Balcazar, balqui at GitHub
Mid Floreal 2025, cosmetic touches by late Floreal.
MIT License

Tight pairs with vertex weights.

Find tight paths in a directed, acyclic, vertex-weighted graph. 
Graphs are NetworkX DiGraphs read from edge lists (see tightpath.py).
Log-based edges assumed, so the algorithm is a simpler dfs.
'''

import networkx as nx

from time import time

EPS = 0.000001 # float precision issues

def tight_pairs(g, root, bound):
    '''
    All tight pairs under bound where the 
    first component is that root.
    '''
    cl_pred = float("inf")
    for u in g.predecessors(root):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, g[u][root]['cost'])
    ret_pairs = list()
    seen = set()
    stack = [ (root, 0) ]
    while stack:
        v, d = stack.pop()
        seen.add(v)
        mayextend = False
        for u in g.neighbors(v):
            if d + g[v][u]['cost'] <= bound + EPS:
                if u not in seen:
                    stack.append( (u, d + g[v][u]['cost']) )
                mayextend = True
        if not mayextend and cl_pred + d > bound - EPS:
            ret_pairs.append((root, v)) # THERE MAY BE REFLEXIVE PAIRS
    return ret_pairs

if __name__ == "__main__":

    fnm = input("Graph filename? (.list assumed) ")
    # ~ fnm = '../examples/' + input("Graph filename? (.list assumed) ")
    # ~ fnm = '../scaff/makegraphs/' + input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        "use -log(desired confidence) [minus some epsilon] as bound"
        tacc = 0
        for start_node in g:
            t = time()
            tps = tight_pairs(g, start_node, float(bound))
            tacc += time() - t
            for pair in tps: # tight_pairs(g, start_node, float(bound)):
                if pair[0] != pair[1]:
                    "1-vertex paths often not useful"
                    print(pair)
        input(f"Time: {tacc:7.4f}")
        bound = input("Bound? (<CR> to finish) ")
