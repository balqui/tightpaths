import networkx as nx

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
    yesants = [] # nearly predecessors
    # ~ notants = [] # far away predecessors, unnecesary today
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
    # ~ maxnonants = []
    # ~ for m in notants:
        # ~ "keep only maximal nonantecedents"
        # ~ for mm in notants:
            # ~ if m < mm:
                # ~ break
        # ~ else:
            # ~ maxnonants.append(m)
	# ~ return (minants,maxnonants)

def tpairs(clspace, threshold):
    "slatt approach, clspace obtained from graph for now"
    pairs = corr()
    for closure in clspace.pred:
        pairs[closure] = minants(clspace, closure, threshold)
    pairs.tighten()
    return pairs

def setweights(g, u):
    "dfs scheme to set up weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = g.nodes[u]['weight'] - g[u][v]['cost']
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
                    # ~ print("  ..  Just appended and call revdfs for", v, "seen", seen)
                    revdfs(g, seen, v, outlist)

        self.pred = dict()
        self.supp = dict()
        for u in g:
            uu = unpack(u)
            self.pred[uu] = list()
            self.supp[uu] = g.nodes[u]['weight']
            seen = set()
            # ~ print("  ..  Call revdfs for", uu)
            revdfs(g, seen, u, self.pred[uu])

if __name__ == "__main__":

    fnm = input("Graph filename? (.list assumed) ")
    g = nx.read_edgelist(fnm + ".elist", create_using = nx.DiGraph)
    g.nodes['__']['weight'] = int(input("Dataset length? "))
    setweights(g, '__')
    clspace = ClSpace(g)
    # ~ for cl in clspace.pred: 
        # ~ print(cl, clspace.supp[cl])
        # ~ for pred in clspace.pred[cl]:
            # ~ print("   ", pred)
    bound = input("Bound? (<RET> to finish) ")
    while bound:
        pairs = tpairs(clspace, float(bound))
        for v in pairs:
            for u in pairs[v]:
                print(repack(u), repack(v), clspace.supp[u], clspace.supp[v],
                    f"{clspace.supp[v] / clspace.supp[u]:6.4f}")
        # ~ for start_node in g:
            # ~ for pair in tight_pairs(g, start_node, float(bound)):
                # ~ if pair[0] != pair[1]:
                    # ~ "1-vertex paths often not useful"
                    # ~ print(pair)
        bound = input("Bound? (<CR> to finish) ")

# SLATT:
# assume we have self.preds: dict mapping closures to their lists 
# of all predecessors = closed proper subsets

# set cuts, pos and neg border, corr dicts

# ~ cpos = corr()
# ~ cneg = corr()
# ~ for nod in self.closeds:
	# ~ if nod.supp >= high_enough:
		# ~ pos, neg = self._cut(nod,sccthr) 
		# ~ cpos[nod] = pos
		# ~ cneg[nod] = neg
# ~ # return cpos, cneg

# ~ def _cut(self,node,thr):
    # ~ """
    # ~ splits preds of node at cut given by
    # ~ min thr-antecedents and max non-thr-antecedents
    # ~ think about alternative algorithmics
    # ~ thr expected scaled according to self.scale
    # ~ """
    # ~ yesants = [] # nearly predecessors
    # ~ notants = [] # far away predecessors
    # ~ for m in self.preds[node]:
        # ~ if higher_enough(node.supp, m.supp):
            # ~ yesants.append(m)
        # ~ else:
            # ~ notants.append(m)
    # ~ minants = []
    # ~ for m in yesants:
        # ~ "keep only minimal antecedents - candidate to separate program?"
        # ~ for mm in yesants:
            # ~ if mm < m:
                # ~ break
        # ~ else:
            # ~ minants.append(m)
    # ~ maxnonants = []
    # ~ for m in notants:
        # ~ "keep only maximal nonantecedents"
        # ~ for mm in notants:
            # ~ if m < mm:
                # ~ break
        # ~ else:
            # ~ maxnonants.append(m)
	# ~ return (minants,maxnonants)

