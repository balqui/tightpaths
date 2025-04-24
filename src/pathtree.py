'''
Jose Luis Balcazar, balqui at GitHub
Early Floreal 2025
MIT License

Data structure PathTree, useful for the general case in
finding tight pairs in a directed graph.
Input graphs will be NetworkX DiGraphs read from edge lists.
The tree is also a NetworkX DiGraph where the single successor
of each node is its parent, except the root that has no successors.

The same vertex from the input graph may appear several times
in the path tree as different tight paths may exist; they are
distinguished with different values of cnt.
'''

import networkx as nx

class PathTree(nx.DiGraph):
    '''
    Tree of paths in input graph that start at a given vertex,
    from which tight paths from that vertex are recovered.
    '''

    cnt = 0 # to distinguish among vertex surrogates

    def treenode(self, u):
        self.cnt += 1
        return u, self.cnt

    def path(self, vv, w_cnt = False):
        'there is a tight path from tree root to vv, reconstruct it'
        
        def vx(v, w_cnt):
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
        '''
        Easy recursive version, fills the tree with all paths from v.
        Graph expected acyclic, o/w please set a path length bound.
        '''
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
        Iterative version with stack,
        keeping track of the intermediate iterators
        as in the NX source code for edge_dfs.
        '''
        t = PathTree()
        root = t.treenode(v)
        t.add_node(root)
        stack = [ root ]
        neigh = dict() # maps vertices to half-traversed neighbor iterators
        while stack:
            u = stack[-1] # top of stack, not popped yet
            if u[0] not in neigh:
                "first visit of graph vertex u[0]"
                neigh[u[0]] = iter(g.neighbors(u[0]))
            try:
                "did we exhaust all neighbors of u?"
                v = t.treenode(next(neigh[u[0]]))
            except StopIteration:
                "neighbors traversed, pop the stack, avoid copying it"
                stack.pop()
            else:
                t.add_edge(v, u)
                stack.append(v)
        return t

    def filltree_all_paths_my_way(g, v):
        '''
        All paths from v again. Iterative version with stack,
        not keeping track of the intermediate iterators
        but just pushing neighbors (hence order is not dfs).
        '''
        t = PathTree()
        root = t.treenode(v)
        t.add_node(root)
        stack = [ (root, 0) ]
        while stack:
            v, d = stack.pop()
            for w in g.neighbors(v[0]):
                w = t.treenode(w)
                t.add_edge(w, v)
                stack.append( (w, d) )
        return t

    g = nx.read_edgelist("e1.elist", create_using = nx.DiGraph)
    # g = nx.read_edgelist("e2.elist", create_using = nx.DiGraph) # CAREFUL, LOOPY
    # g = nx.read_edgelist("e3.elist", create_using = nx.DiGraph) # CAREFUL, LOOPY
    # g = nx.read_edgelist("e4.elist", create_using = nx.DiGraph) # CAREFUL, ZEROLOOPY

# All paths in the graph using the iterative version, my way
    for start_node in g:
        t = filltree_all_paths_my_way(g, start_node)
        for v in t:
            print(t.path(v, True))

# All paths in the graph using the iterative version, nx-like
    for start_node in g:
        t = filltree_nx_like(g, start_node)
        for v in t:
            print(t.path(v))

# All paths in the graph using the recursive version
    for start_node in g:
        t = PathTree()
        root = t.treenode(start_node)
        t.add_node(root)
        filltree_r(g, t, root)

