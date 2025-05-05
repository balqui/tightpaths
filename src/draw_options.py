import networkx as nx

def tr_elabel(g, wlog):
    "Copy costs as edge labels to be drawn"

    def auxstr(c, wlog):
        return f"{c:6.3f}" if wlog else str(c)

    for u in g:
        for v in g.neighbors(u):
            g[u][v]['label'] = auxstr(g[u][v]['cost'], wlog)

def reweight(uw, vw, wlog):
    if wlog:
        return round(uw / 2 ** vw)
    else:
        return uw - vw

def tr_vlabel(g, u, wlog):
    "dfs scheme to set up weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = reweight(g.nodes[u]['weight'], g[u][v]['cost'], wlog)
            tr_vlabel(g, v, wlog)

fnm = input("Graph filename? (.list assumed) ")
g = nx.read_edgelist(fnm + '.elist',  create_using = nx.DiGraph)
g.graph['rankdir'] = 'LR'
task = input("Task? (e: Draw with edge labels, v: Draw with vertex labels) ")
wlog = 'y' == input("Log scale? [y/n] ")
if task == 'e':
    tr_elabel(g, wlog)
if task == 'v':
    g.nodes['__']['weight'] = int(input("Dataset length? "))
    tr_vlabel(g, '__', wlog)
    rl = dict()
    for u in g:
        rl[u] = u + '  ' + str(g.nodes[u]['weight'])
    g = nx.relabel.relabel_nodes(g, rl)
    fnm += "_relab"
nx.nx_agraph.write_dot(g, fnm + ".gv")
print("Wrote", fnm + ".gv")
