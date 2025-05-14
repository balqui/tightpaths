'''
Jose Luis Balcazar, balqui at GitHub
Mid Floreal 2025
MIT License

Find tight pairs in a directed graph with vertex weights. 
Follows the dfs scheme.

First I have to make it work, then take out the excessive
relevance on edgecost.

Graphs are NetworkX DiGraphs read from edge lists where
the edge costs are right now the differences of the
weights of the end
'''

import networkx as nx

# ~ from pathtree import PathTree

def setweights(g, u):
    "dfs scheme to set up weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            # ~ print(f"Setting cost of {v} to {g.nodes[u]['weight'] - g[u][v]['cost']}")
            g.nodes[v]['weight'] = g.nodes[u]['weight'] - g[u][v]['cost']
            setweights(g, v)

def edgecost(g, u, v):
    c = g.nodes[u]['weight'] / g.nodes[v]['weight']
    assert c >= 1, \
      f"for {u} and {v}, {g.nodes[u]['weight']} / {g.nodes[v]['weight']} < 1"
    return c

def tight_pairs(g, u, bound):
    '''
    All tight pairs from u under bound b.
    '''
    ret_pairs = list()
    cl_pred = float("inf")
    for v in g.predecessors(u):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, edgecost(g, v, u))
    # ~ t = PathTree()
    # ~ root = t.treenode(v)
    # ~ t.add_node(root)
    stack = [ (u, 0) ]
    seen = set()
    while stack:
        v, d = stack.pop()
        seen.add(v)
        more = False
        for w in g.neighbors(v):
            if w not in seen and d + edgecost(g, u, v) <= bound:
                # ~ w = t.treenode(w) 
                # ~ t.add_edge(w, v)
                stack.append( (w, d + edgecost(g, u, v)) )
                more = True
        if not more and cl_pred + d > bound:
            ret_pairs.append((u, v)) # THERE MAY BE REFLEXIVE PAIRS
    return ret_pairs

if __name__ == "__main__":

    from math import log

    # g = nx.read_edgelist("e1.elist", create_using = nx.DiGraph)
    # g = nx.read_edgelist("e1b.elist", create_using = nx.DiGraph)
    # g = nx.read_edgelist("e2.elist", create_using = nx.DiGraph) # CAREFUL, LOOPY
    # g = nx.read_edgelist("e3.elist", create_using = nx.DiGraph) # CAREFUL, LOOPY
    # g = nx.read_edgelist("e4.elist", create_using = nx.DiGraph) # CAREFUL, ZEROLOOPY

    fnm = '../examples/' + input("Graph filename? (.list assumed) ")
    # ~ fnm = '../scaff/makegraphs/' + input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    nx.set_edge_attributes(g, 'above', 'elabel')
    # ~ if input(f"Write LaTex drawing {fnm}.tex? "):
        # ~ 'create a TikZ diagram - BAD CHOICE, WRONG LAYOUT'
        # ~ nx.write_latex(g, fnm + ".tex", 
                       # ~ edge_label = 'cost',
                       # ~ edge_label_options = 'elabel') 
        # ~ # ADD as_document = False FOR INCLUSION IN A LARGER TEXT
    dslen = input("Dataset length? ")
    bound = float(input("Bound? (<RET> to finish) "))
    print(f"Base 2 log of {bound} is {log(bound, 2)}")

    # ~ print("neigh __:", list(g.neighbors("__")))
    # ~ print("neigh _-none_:", list(g.neighbors("_-none_")))
    # ~ exit()

    g.nodes['__']['weight'] = int(dslen)
    setweights(g, '__')
    while bound:
        for start_node in g:
            for pair in tight_pairs(g, start_node, bound):
                print(pair)
        bound = float(input("Bound? (<CR> to finish) "))
