from tightpath import tight_paths as tpaths
from tightpair import tight_pairs as tpairs

from time import time
from math import log

import networkx as nx
import matplotlib.pyplot as plt

dlen = 1597
gr = nx.read_edgelist("../graphs/fromdata/NOW1_logsupp.elist", 
# ~ dlen = 13
# ~ gr = nx.read_edgelist("../graphs/fromdata/e13b_logsupp.elist", 
                     create_using = nx.DiGraph)

plotcol0 = list()
plotcol1 = list()

pts = 25
# ~ pts = 8
incr = log(dlen, 2)/pts

thrs = list()
thr = incr
for _ in range(pts - 1):
	thrs.append(thr)
	thr += incr

for thr in thrs:
	pth1 = list()
	pth2 = list()
	t0 = time()
	for v in gr:
		pth1 += tpaths(gr, v, thr)
	t1 = time()
	for v in gr:
		pth2 += tpairs(gr, v, thr)
	t2 = time()
	print(thr, len(pth1), len(pth2),  
		t1 - t0, t2 - t1)
	# ~ print("---")
	# ~ print(pth1)
	# ~ print("---")
	# ~ print(pth2)
	# ~ print("---")
	plotcol0.append(t1 - t0)
	plotcol1.append(t2 - t1)

fig, ax = plt.subplots()
# ~ ax.plot(thrs, plotcol0, label = "Paths (alg. 2)", marker = 'o')
# ~ ax.plot(thrs, plotcol1, label = "Pairs (alg. 3)", marker = '^')
ax.plot(thrs, plotcol0, label = "Paths (alg. 2)", dashes = [1, 1])
ax.plot(thrs, plotcol1, label = "Pairs (alg. 3)", dashes = [5, 1])

ax.set(xlabel='threshold', ylabel='time (sec)',
       title='Tight paths versus tight pairs: time comparison')
ax.grid()

fig.legend(loc='center right')
fig.savefig("timing_2_3_NOW1.png")
plt.show()

