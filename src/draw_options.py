'''
Jose Luis Balcazar, balqui at GitHub
Late Floreal 2025
MIT License

Make a .gv representation from an .elist graph 
(then xdot can create a .png file).
 - if task is edge weights, formats floats to few decimal places;
 - if task is raw vertex weights, they are just additions of edge costs;
 - if task is vertex weights, vertex labels are intended to be supports:
   tool asks about log scale and assumes a diff-of-log-supp labeling 
   instead of a diff-of-supp edge labeling accordingly.
'''

import networkx as nx

def tr_elabel(g):
    "Copy costs as edge labels to be drawn"

    def auxstr(c):
        return f"{int(c):4d}" if c.is_integer() else f"{c:6.3f}"

    for u in g:
        for v in g.neighbors(u):
            g[u][v]['label'] = auxstr(g[u][v]['cost'])

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

def tr_rlabel(g, u):
    "dfs scheme to set up raw weights on vertices from the edge differences"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = g.nodes[u]['weight'] + g[u][v]['cost']
            tr_rlabel(g, v)

fnm = input("Graph filename? (.elist assumed) ")
g = nx.read_edgelist(fnm + '.elist',  create_using = nx.DiGraph)
g.graph['rankdir'] = 'LR'
task = input("Task? (e: Draw with edge labels, v: Draw with vertex labels, r: Raw vertex labels) ")
if task == 'e':
    tr_elabel(g)
if task == 'r':
    tr_elabel(g)
    g.nodes['__']['weight'] = 0
    tr_rlabel(g, '__')
    rl = dict()
    for u in g:
        rl[u] = f"{g.nodes[u]['weight']:6.3f}"
        # ~ rl[u] = u + '  ' + str(g.nodes[u]['weight'])
    g = nx.relabel.relabel_nodes(g, rl)
    fnm += "_vrlab"
if task == 'v':
    wlog = 'y' == input("Log scale? [y/n] ")
    g.nodes['__']['weight'] = int(input("Dataset length? "))
    tr_vlabel(g, '__', wlog)
    rl = dict()
    for u in g:
        rl[u] = u + '  ' + str(g.nodes[u]['weight'])
    g = nx.relabel.relabel_nodes(g, rl)
    fnm += "_vlab"
nx.nx_agraph.write_dot(g, fnm + ".gv")
print("Wrote", fnm + ".gv")
