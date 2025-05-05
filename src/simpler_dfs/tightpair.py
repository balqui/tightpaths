'''
Jose Luis Balcazar, balqui at GitHub
Mid Floreal 2025
MIT License

Tight pairs with vertex weights.

Find tight paths in a directed, acyclic, vertex-weighted graph. 
Graphs are NetworkX DiGraphs read from edge lists (see tightpath.py).
Log-based edges assumed, so the algorithm is a simpler dfs.
'''

import networkx as nx

def tight_pairs(g, u, bound):
    '''
    All tight pairs from u under bound b.
    Could be made an iterator.
    '''
    ret_pairs = list()
    cl_pred = float("inf")
    for v in g.predecessors(u):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, g[v][u]['cost'])
    stack = [ (u, 0) ]
    seen = set()
    while stack:
        v, d = stack.pop()
        seen.add(v)
        ext = False
        for w in g.neighbors(v):
            if d + g[v][w]['cost'] <= bound:
                if w not in seen:
                    stack.append( (w, d + g[v][w]['cost']) )
                ext = True
        if not ext and cl_pred + d > bound:
            ret_pairs.append((u, v)) # THERE MAY BE REFLEXIVE PAIRS
    return ret_pairs

if __name__ == "__main__":

    fnm = input("Graph filename? (.list assumed) ")
    # ~ fnm = '../examples/' + input("Graph filename? (.list assumed) ")
    # ~ fnm = '../scaff/makegraphs/' + input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        "use -log(desired confidence) [minus some epsilon] as bound"
        for start_node in g:
            for pair in tight_pairs(g, start_node, float(bound)):
                if pair[0] != pair[1]:
                    "1-vertex paths often not useful"
                    print(pair)
        bound = input("Bound? (<CR> to finish) ")
