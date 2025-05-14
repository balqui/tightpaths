'''
Jose Luis Balcazar, balqui at GitHub
Mid Floreal 2025
MIT License

Tight pairs with vertex weights, again.

Find tight paths in a directed, acyclic, vertex-weighted graph. 
Graphs are NetworkX DiGraphs read from edge lists (see tightpath.py).
Log-based edges assumed, so the algorithm is a simpler dfs.
However, instead of adding up costs of paths, we set up the
weights on the vertices so as to compute directly the distances.
If graph comes from a closure space, vertex weights will be 
sign-changed base 2 logarithms of the normalized supports.
If the graph encoding can bring this quantity precomputed, then
the setweights call is to be replaced by the corresponding reading.
'''

import networkx as nx

def setweights(g, u):
    "dfs scheme to set up weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = g.nodes[u]['weight'] + g[u][v]['cost']
            setweights(g, v)

def pathcost(g, u, v):
    return g.nodes[v]['weight'] - g.nodes[u]['weight']

def tight_pairs(g, u, bound):
    '''
    All tight pairs from u under bound b.
    Could be made an iterator.
    '''
    ret_pairs = list()
    cl_pred = float("inf")
    for v in g.predecessors(u):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, pathcost(g, v, u))
    stack = [ u ]
    seen = set()
    while stack:
        v = stack.pop()
        seen.add(v)
        ext = False
        for w in g.neighbors(v):
            if pathcost(g, u, w) <= bound:
                if w not in seen:
                    stack.append( w )
                ext = True
        if not ext and cl_pred + pathcost(g, u, v) > bound:
            ret_pairs.append((u, v)) # THERE MAY BE REFLEXIVE PAIRS
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
        for start_node in g:
            for pair in tight_pairs(g, start_node, float(bound)):
                if pair[0] != pair[1]:
                    "1-vertex paths often not useful"
                    print(pair)
        bound = input("Bound? (<CR> to finish) ")
