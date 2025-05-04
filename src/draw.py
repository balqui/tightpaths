import networkx as nx

def tr_elabel(g):
  for u in g:
    for v in g.neighbors(u):
      g[u][v]['label'] = f"{g[u][v]['cost']:6.3f}"

def tr_vlabel(g, u):
    "dfs scheme to set up weights on vertices from the edge differences and relabel them"
    for v in g.neighbors(u):
        if 'weight' not in g.nodes[v]:
            g.nodes[v]['weight'] = round(g.nodes[u]['weight'] / g[u][v]['cost'])
            tr_vlabel(g, v)

# ~ fnm = "lenshort_24.dif.no_log"

fnm = '../examples/' + input("Graph filename? (.list assumed) ")
g = nx.read_edgelist(fnm + '.elist',  create_using = nx.DiGraph)
dslen = int(input("Dataset length? "))
g.nodes['__']['weight'] = dslen
tr_vlabel(g, '__')
rl = dict()
for u in g:
	rl[u] = u + ' / ' + str(g.nodes[u]['weight'])
print(rl)
g = nx.relabel.relabel_nodes(g, rl)
# ~ tr_elabel(g)
nx.nx_agraph.write_dot(g, fnm + "_relab.gv")
