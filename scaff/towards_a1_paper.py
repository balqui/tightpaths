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

class MyTree(nx.DiGraph):
    '''
    Tree of paths in input graph that start at a given vertex,
    from which tight paths from that vertex are recovered.
    '''

    cnt = 0 # to distinguish among vertex surrogates

    def treenode(self, u):
        self.cnt += 1
        return u, self.cnt

    def path(self, vv, w_cnt = False):
        'a tight path from tree root to vv has been found'
        
        def vx(v, w_cnt = False):
            "whether to show the counter in the output"
            if w_cnt:
                return v
            else:
                return v[0]

        ret_path = [ vx(vv, w_cnt) ]
        while parent := list(self.neighbors(vv)):
            'vv has exactly one parent in tree except if root'
            ret_path.append(vx(parent[0], w_cnt)) # discard counter
            vv = parent[0]
        return list(reversed(ret_path))




if __name__ == "__main__":

    def filltree_r(g, t, v):
        "Easy recursive version, all paths from v"
        p = t.path(v)
        print(p)
        # if len(p) < 10: # for loopy graphs
        if True:
            vg = v[0]
            for ug in g.neighbors(vg):
                u = t.treenode(ug)
                t.add_edge(u, v)
                filltree_r(g, t, u)

    def filltree_nx_like(g, v):
        '''
        All paths from v again.
        Iterative version with stack towards alg a1,
        keeping track of the intermediate iterators
        as in the NX source code for edge_dfs.
        '''
        t = MyTree()
        root = t.treenode(v)
        t.add_node(root)
        stack = [ root ]
        neigh = dict() # maps vertices to half-traversed neighbor iterators
        while stack:
            u = stack[-1] # top of stack
            if u[0] not in neigh:
                "first visit of graph vertex u[0]"
                neigh[u[0]] = iter(g.neighbors(u[0]))
            try:
                "did we exhaust all neighbors of u?"
                v = t.treenode(next(neigh[u[0]]))
            except StopIteration:
                "neighbors traversed, pop the stack, avoid copying it"
                del stack[-1]
            else:
                t.add_edge(v, u)
                stack.append(v)
        return t

    def filltree_all_paths_my_way(g, v):
        '''
        All paths from v again.
        Iterative version with stack towards alg a1,
        not keeping track of the intermediate iterators
        but just pushing neighbors as in the alg in the paper.
        '''
        t = MyTree()
        root = t.treenode(v)
        t.add_node(root)
        stack = [ (root, 0) ]
        while stack:
            v, d = stack[-1] # top of stack
            del stack[-1]    # pop the stack, avoid copying it
            more = False     # dead end until proven not to be
            for w in g.neighbors(v[0]):
                w = t.treenode(w)
                t.add_edge(w, v)
                stack.append( (w, d) )
                more = True
            # ~ if not more:
                # ~ print("Must test length of path from", root, "to", v)
        return t

    def tight_paths(g, v, bound):
        '''
        All tight paths from v under bound b.
        '''
        ret_paths = list()
        cl_pred = float("inf")
        for u in g.predecessors(v[0]):
            cl_pred = min(cl_pred, g[u][v[0]]['cost'])
        t = MyTree()
        root = t.treenode(v)
        t.add_node(root)
        stack = [ (root, 0) ]
        while stack:
            v, d = stack.pop()
            more = False
            for w in g.neighbors(v[0]):
                if d + g[v[0]][w]['cost'] <= bound:
                    w = t.treenode(w)
                    t.add_edge(w, v)
                    stack.append( (w, d + g[v[0]][w[0]]['cost']) )
                    more = True
            if not more and cl_pred + d > bound:
                ret_paths.append(t.path(v)) # THERE MAY BE 0-EDGE PATHS
        return ret_paths

    g = nx.read_edgelist("e1.elist", create_using = nx.DiGraph)
    # g = nx.read_edgelist("e2.elist", create_using = nx.DiGraph) # CAREFUL, LOOPY
    # g = nx.read_edgelist("e3.elist", create_using = nx.DiGraph) # CAREFUL, LOOPY
    # g = nx.read_edgelist("e4.elist", create_using = nx.DiGraph) # CAREFUL, ZEROLOOPY

# Tight paths in the graph
    bound = input("Bound? ")
    while bound:
        for start_node in g:
            for path in tight_paths(g, start_node, float(bound)):
                print(path)
        bound = input("Bound? ")

# All paths in the graph using the iterative version, my way
    # ~ for start_node in g:
        # ~ t = filltree_all_paths_my_way(g, start_node)
        # ~ for v in t:
            # ~ print(t.path(v, True))

# All paths in the graph using the iterative version, nx-like
    # ~ for start_node in g:
        # ~ t = filltree_nx_like(g, start_node)
        # ~ for v in t:
            # ~ print(t.path(v))

# All paths in the graph using the recursive version
    # ~ for start_node in g:
        # ~ t = MyTree()
        # ~ root = t.treenode(start_node)
        # ~ t.add_node(root)
        # ~ filltree_r(g, t, root)

# ~ def simpl_edge_dfs(digraph):

    # ~ for start_node in digraph:

        # ~ print(" ... from ", start_node)
        # ~ visited_edges = set()
        # ~ visited_nodes = set()
        # ~ edges = {}

        # ~ stack = [start_node]
        # ~ while stack:
            # ~ current_node = stack[-1]
            # ~ if current_node not in visited_nodes:
                # ~ edges[current_node] = iter(digraph.edges(current_node))
                # ~ visited_nodes.add(current_node)

            # ~ try:
                # ~ edge = next(edges[current_node])
            # ~ except StopIteration:
                # ~ # No more edges from the current node.
                # ~ stack.pop()
            # ~ else:
                # ~ if edge not in visited_edges:
                    # ~ visited_edges.add(edge)
                    # ~ stack.append(edge[1])
                    # ~ yield edge

    # ~ g = nx.read_edgelist("e1.elist", create_using = nx.DiGraph)
    # ~ print("dfs_edges:")
    # ~ for e in nx.dfs_edges(g): print(e)
    # ~ print("dfs_tree edges:")
    # ~ print(nx.dfs_tree(g).edges)
    # ~ print("edge_dfs from A:")
    # ~ for e in nx.edge_dfs(g, 'A'): print(e, "cost", g.edges[e]['cost'])

    # ~ print("simplified edge_dfs:")
    # ~ for e in simpl_edge_dfs(g): print(e, "cost", g.edges[e]['cost'])
