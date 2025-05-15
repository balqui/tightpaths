'''
Jose Luis Balcazar, balqui at GitHub
Mid Floreal 2025, cosmetic touches by late Floreal.
MIT License

Tight pairs with vertex weights, again.

Find tight paths in a directed, acyclic, vertex-weighted graph. 
Graphs are NetworkX DiGraphs read from edge lists (see tightpath.py).
Log-based edges assumed, so the algorithm is a simpler dfs.
However, instead of adding up costs of paths, we set up the
weights on the vertices so as to compute directly the distances.
If graph comes from a closure space, vertex weights will be 
sign-changed base 2 logarithms (they are negative!) of the 
normalized supports. If the graph encoding can bring this 
quantity precomputed, then the setweights call is to be 
replaced by the corresponding reading (not done yet).
'''

import networkx as nx

from time import time

EPS = 0.000001 # float precision issues

def setweights(g, u):
    "dfs scheme to set up weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = g.nodes[u]['weight'] + g[u][v]['cost']
            setweights(g, v)

def pathcost(g, u, v):
    return g.nodes[v]['weight'] - g.nodes[u]['weight']

def tight_pairs(g, root, bound):
    '''
    All tight pairs under bound where the 
    first component is that root.
    '''
    cl_pred = float("inf")
    for u in g.predecessors(root):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, pathcost(g, u, root))
    ret_pairs = list()
    seen = set()
    stack = [ root ]
    while stack:
        v = stack.pop()
        seen.add(v)
        mayextend = False
        for u in g.neighbors(v):
            if pathcost(g, root, u) <= bound + EPS:
                if u not in seen:
                    stack.append( u )
                mayextend = True
        if not mayextend and cl_pred + pathcost(g, root, v) > bound - EPS:
            ret_pairs.append((root, v)) # THERE MAY BE REFLEXIVE PAIRS
    return ret_pairs

if __name__ == "__main__":

    fnm = input("Graph filename? (.list assumed) ")
    # ~ fnm = '../examples/' + input("Graph filename? (.list assumed) ")
    # ~ fnm = '../scaff/makegraphs/' + input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    g.nodes['__']['weight'] = 0 # log(int(input("Dataset length? ")), 2)
    setweights(g, '__')
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        "use -log(desired confidence) [minus some epsilon] as bound"
        tacc = 0
        for start_node in g:
            t = time()
            tps = tight_pairs(g, start_node, float(bound))
            tacc += time() - t
            for pair in tps:
                if pair[0] != pair[1]:
                    "1-vertex paths often not useful"
                    print(pair)
        input(f"Time: {tacc:7.4f}")
        bound = input("Bound? (<CR> to finish) ")
