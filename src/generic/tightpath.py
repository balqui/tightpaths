'''
Jose Luis Balcazar, balqui at GitHub
Early Floreal 2025
MIT License

Find tight paths in a directed graph. 
Follows in part the function edge_dfs of the NetworkX package,
but simplified as we don't need dfs order on the edges.

Graphs are NetworkX DiGraphs read from edge lists.
There, each edge is described by strings for the source 
and target vertices in this order, plus a dictionary with,
at least, the key 'cost' and a positive number as cost value.
'''

import networkx as nx

from pathtree import PathTree

def tight_paths(g, v, bound):
    '''
    All tight paths from v under bound b.
    Vertex v expected to be a treenode.
    '''
    ret_paths = list()
    cl_pred = float("inf")
    for u in g.predecessors(v):
        "Find distance to closest predecessor, inf if no predecessor"
        cl_pred = min(cl_pred, g[u][v]['cost'])
    t = PathTree()
    root = t.treenode(v)
    t.add_node(root)
    stack = [ (root, 0) ]
    while stack:
        v, d = stack.pop()
        more = False
        for w in g.neighbors(v[0]):
            "v is now a treenode, and v[0] its graph vertex"
            if d + g[v[0]][w]['cost'] <= bound:
                "w becomes a treenode too"
                w = t.treenode(w) 
                t.add_edge(w, v)
                stack.append( (w, d + g[v[0]][w[0]]['cost']) )
                more = True
        if not more and cl_pred + d > bound:
            ret_paths.append(t.path(v)) # THERE MAY BE 0-EDGE PATHS
    return ret_paths

if __name__ == "__main__":

    fnm = input("Graph filename? (.list assumed) ")
    # ~ fnm = '../examples/' + input("Graph filename? (.list assumed) ")
    # ~ fnm = '../scaff/makegraphs/' + input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    nx.set_edge_attributes(g, 'above', 'elabel')
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        for start_node in g:
            for path in tight_paths(g, start_node, float(bound)):
                print(path)
        bound = input("Bound? (<CR> to finish) ")
