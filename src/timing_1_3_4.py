from slatt import tpairs as tpairss, ClSpace, repack, setweights as setweightss, unpack
from tightpair import tight_pairs as tpairs
from tightpair_vw import setweights, tight_pairs as tpairsv

from time import time
from math import log

import networkx as nx
import matplotlib.pyplot as plt

def partprint(ls, gr, grcs):
	"skip single-vertex paths"
	cnt = 0
	for (s, t) in ls:
		if s != t: 
			cnt += 1
			print(f"{cnt}/ {s} {gr.nodes[s]['weight']} {grcs.supp[unpack(s)]} --  {t} {gr.nodes[t]['weight']} {grcs.supp[unpack(t)]}")

dlen = 1597 # number of transactions in dataset
gr = nx.read_edgelist("../graphs/fromdata/NOW1_logsupp.elist", 
# ~ dlen = 1000
# ~ gr = nx.read_edgelist("../graphs/fromdata/markbask_logsupp.elist", 
# ~ dlen = 13
# ~ gr = nx.read_edgelist("../graphs/fromdata/e13b_logsupp.elist", 
                     create_using = nx.DiGraph)
print(f"Graph read. It has {gr.number_of_nodes()} nodes.")

grcs = gr.copy()

gr.nodes['__']['weight'] = 0
setweights(gr, '__')    # weights are path costs

grcs.nodes['__']['weight'] = dlen
setweightss(grcs, '__') # weights are actual supports
grcs = ClSpace(grcs)

plotcol0 = list()
plotcol1 = list()
plotcol2 = list()

pts = 25
# ~ pts = 8
incr = log(dlen, 2)/pts

thrs = list()
thr = incr
for _ in range(pts - 1):
	thrs.append(thr)
	thr += incr

rep = 5

for thr in thrs:
	pth1 = list()
	pth2 = list()
	t0b = time()
	for _ in range(rep):
		pairs = tpairss(grcs, 2 ** -thr)
	t0e = time()
	pth0 = [ (repack(u), repack(v)) for v in pairs for u in pairs[v] ]
	t1 = time()
	for _ in range(rep):
		for v in gr:
			pth1 += tpairs(gr, v, thr)
	t2 = time()
	for _ in range(rep):
		for v in gr:
			pth2 += tpairsv(gr, v, thr)
	t3 = time()
	print(thr, len(pth0), len(pth1), len(pth2), t0e - t0b, t2 - t1, t3 - t2)
	# ~ print("---")
	# ~ print(pth0)
	# ~ print("---")
	# ~ print(pth1)
	# ~ print("---")
	# ~ print(pth2)
	# ~ print("---")
	plotcol0.append((t0e - t0b) / rep)
	plotcol1.append((t2 - t1) / rep)
	plotcol2.append((t3 - t2) / rep)

fig, ax = plt.subplots()
ax.plot(thrs, plotcol0, label = "Alg. 1")
ax.plot(thrs, plotcol1, label = "Alg. 3")
ax.plot(thrs, plotcol2, label = "Alg. 4")

ax.set(xlabel='threshold', ylabel='time (sec)',
       title='Tight pair algorithms: time comparison')
ax.grid()

fig.legend(loc='center right')
fig.savefig("timing_1_3_4_NOW1.png")
plt.show()

