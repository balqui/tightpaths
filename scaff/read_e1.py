import networkx as nx
g = nx.read_edgelist("e1.elist", create_using = nx.DiGraph)
print("dfs_edges:")
for e in nx.dfs_edges(g): print(e)
print("dfs_tree edges:")
print(nx.dfs_tree(g).edges)
print("edge_dfs from A:")
for e in nx.edge_dfs(g, 'A'): print(e)
for v in g:
    for u in g.predecessors(v):
        print(u, "pred of", v, "with cost", g[u][v]['cost'])
