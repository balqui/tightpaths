'''
Jose Luis Balcazar, balqui at GitHub
Late Floreal 2025
MIT License

Tight pairs with vertex weights via the old slatt approach of tightening.

Find tight paths in a directed, acyclic, vertex-weighted graph. 
Graphs are NetworkX DiGraphs read from edge lists (see tightpath.py).
Edge costs expected to be the log of support quotients, "_logsupp.elists" 
files, needs the dataset size to recover the supports.
'''

import networkx as nx

from time import time

class corr(dict):
    "right-tightening, we do left-tightening in minants"

    def __init__(self):
        dict.__init__(self)

    def tighten(self):
        for e in self.keys():
            valids = []
            for g in self[e]:
                for ee in self.keys():
                    if e < ee and g in self[ee]:
                        break
                else:
                    valids.append(g)
            self[e] = valids


def minants(clspace, closure, thr):
    """
    finds in preds of closure min thr-antecedents.
    """
    yesants = [] # nearly enough predecessors
    for m in clspace.pred[closure]:
        "discards far-away predecessors"
        if clspace.supp[closure] >= thr * clspace.supp[m]:
            yesants.append(m)
    minants = []
    for m in yesants:
        "keeps jut the minimal closures"
        for mm in yesants:
            if mm < m:
                break
        else:
            minants.append(m)
    return minants

def tpairs(clspace, threshold):
    "slatt approach, clspace obtained from graph for now"
    pairs = corr()
    t = time()
    for closure in clspace.pred:
        pairs[closure] = minants(clspace, closure, threshold)
    tm = time()
    pairs.tighten()
    input(f"Time: {time() - t:7.4f}, of which {tm - t:7.4f} before tightening.")
    return pairs

def setweights(g, u):
    "dfs scheme to set up weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = round(g.nodes[u]['weight'] / 2**g[u][v]['cost'])
            print("Weight:", v, g.nodes[v]['weight'])
            setweights(g, v)

def unpack(u):
    return frozenset([ e for e in u.strip('_').split('_') if e ])

def repack(uu):
    return '_' + '_'.join(e for e in sorted(uu)) + '_'

class ClSpace:

    def __init__(self, g):

        def revdfs(g, seen, u, outlist):
            for v in g.predecessors(u):
                if v not in seen:
                    outlist.append(unpack(v))
                    seen.add(v)
                    revdfs(g, seen, v, outlist)

        self.pred = dict()
        self.supp = dict()
        for u in g:
            uu = unpack(u)
            self.pred[uu] = list()
            self.supp[uu] = g.nodes[u]['weight']
            seen = set()
            revdfs(g, seen, u, self.pred[uu])

if __name__ == "__main__":

    fnm = input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    g.nodes['__']['weight'] = int(input("Dataset length? "))
    setweights(g, '__')
    clspace = ClSpace(g)
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        pairs = tpairs(clspace, float(bound))
        for v in pairs:
            for u in pairs[v]:
                print(repack(u), repack(v), clspace.supp[u], clspace.supp[v],
                    f"{clspace.supp[v] / clspace.supp[u]:6.4f}")
        bound = input("Bound? (<CR> to finish) ")

